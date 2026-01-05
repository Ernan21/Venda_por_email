import smtplib
import time
from datetime import datetime, timedelta
import pandas as pd
import pg8000
from sqlalchemy import create_engine
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# =====================================================
# Carrega variáveis do .env
# =====================================================
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SUBJECT = os.getenv("EMAIL_SUBJECT")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVERS").split(",")

# =====================================================
# Datas
# =====================================================
data = datetime.today().date()
data_atual = data - timedelta(days=1)
dataold = data - timedelta(days=data.day - 1)

print(data_atual)
print(dataold)

# =====================================================
# URL do banco
# =====================================================
url = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

message = ""

# =====================================================
# Consulta ao banco
# =====================================================
def ProdutosLoja():
    global message

    print('Iniciando Busca de produtos no banco de dados')
    print('Por favor, aguarde ...')

    try:
        conn = pg8000.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )

        engine = create_engine(url)

        consulta = f"""
        SELECT 
            TO_CHAR(v.data, 'dd-mm-yyyy') AS "Data", 
            TO_CHAR(
                SUM(v.valortotal + v.valoracrescimocupom - v.valorcancelado - v.valordesconto - v.valordescontocupom),
                'L9G999G990D99'
            ) AS "Venda",
            TO_CHAR(
                (
                    SELECT SUM(valortotal + valoracrescimocupom - valorcancelado - valordesconto - valordescontocupom)
                    FROM pdv.vendaitem
                    WHERE data BETWEEN '{dataold.strftime("%Y-%m-%d")}'
                    AND '{data_atual.strftime("%Y-%m-%d")}'
                ),
                'L9G999G990D99'
            ) AS "Total Mensal",
            TO_CHAR(
                SUM(v.valortotal + v.valoracrescimocupom - v.valorcancelado - v.valordesconto - v.valordescontocupom) /
                (
                    SELECT SUM(valortotal + valoracrescimocupom - valorcancelado - valordesconto - valordescontocupom)
                    FROM pdv.vendaitem
                    WHERE data BETWEEN '{dataold.strftime("%Y-%m-%d")}'
                    AND '{data_atual.strftime("%Y-%m-%d")}'
                ) * 100,
                '9G999G990D99 %'
            ) AS "Part (% Mensal)"
        FROM pdv.vendaitem v
        WHERE v.data BETWEEN '{dataold.strftime("%Y-%m-%d")}'
        AND '{data_atual.strftime("%Y-%m-%d")}'
        GROUP BY v.data;
        """

        df = pd.read_sql_query(consulta, engine)
        message = df.to_html(index=False, justify='center', classes='table table-bordered table-striped')

        conn.close()
        engine.dispose()

    except Exception as error:
        print("Erro ao conectar ou executar a consulta:", error)

# =====================================================
# Envio de Email
# =====================================================
def enviar_Relatorio():
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ",".join(RECEIVER_EMAIL)
        msg['Subject'] = SUBJECT

        msg.attach(MIMEText(f"""
        <html>
            <head>
                <style>
                    .table {{
                        border-collapse: collapse;
                        width: 100%;
                        font-size: 14px;
                    }}
                    .table th, .table td {{
                        padding: 8px;
                        text-align: center;
                        border: 1px solid #ccc;
                    }}
                    .table th {{
                        background-color: #f2f2f2;
                    }}
                    tr:hover {{
                        background-color: skyblue;
                    }}
                </style>
            </head>
            <body>
                <p>Bom dia, segue o relatório de venda mensal da Loja do JOJA</p>
                <p>Email enviado automaticamente, por favor não responder!</p>
                <p>Atenciosamente,<br>Ernando</p>
                <p>Relatório criado de {dataold.strftime('%d-%m-%Y')} até {data_atual.strftime('%d-%m-%Y')}</p>
                {message}
            </body>
        </html>
        """, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")

# =====================================================
# Execução
# =====================================================
ProdutosLoja()
enviar_Relatorio()
time.sleep(10)
print('Macro terminada')