# 📊 Relatório Automático de Vendas Mensais

Este projeto realiza a **extração automática de dados de vendas mensais** a partir de um banco de dados **PostgreSQL**, gera um **relatório em formato HTML** e envia o resultado por **e-mail via SMTP (Gmail)**.

O sistema foi desenvolvido em **Python**, seguindo boas práticas de segurança, utilizando variáveis de ambiente (`.env`) para proteção de credenciais.

---

## 🚀 Funcionalidades

* ✔ Conexão com banco de dados PostgreSQL
* ✔ Consulta dinâmica de vendas do mês corrente
* ✔ Geração automática de relatório em tabela HTML
* ✔ Envio de e-mail com layout estilizado (CSS embutido)
* ✔ Uso de `.env` para segurança de credenciais
* ✔ Suporte a múltiplos destinatários
* ✔ Totalmente automatizável (cron / Task Scheduler)

---

## 🛠️ Tecnologias Utilizadas

* Python 3.9+
* PostgreSQL
* Pandas
* SQLAlchemy
* pg8000
* SMTP (Gmail)
* python-dotenv

---

## 📦 Estrutura do Projeto

```
📁 relatorio-vendas
 ├── relatorio_vendas.py
 ├── .env
 ├── .gitignore
 └── README.md
```

---

## 🔐 Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
# SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_SENDER=seuemail@gmail.com
EMAIL_PASSWORD=senha_de_app_gmail

# Banco de Dados
DB_HOST=192.168.0.100
DB_PORT=38561
DB_NAME=database
DB_USER=usuario
DB_PASSWORD=senha

# Email
EMAIL_SUBJECT=Relatório Mensal de Vendas
EMAIL_RECEIVERS=destino1@gmail.com,destino2@gmail.com
```

⚠️ **Nunca versionar o `.env` no GitHub.**

---

## 📌 Pré-requisitos

* Python 3.9 ou superior
* Acesso a um banco PostgreSQL
* Conta Gmail com **senha de aplicativo** habilitada

---

## 📥 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/relatorio-vendas.git
cd relatorio-vendas
```

Instale as dependências:

```bash
pip install pandas sqlalchemy pg8000 python-dotenv
```

---

## ▶️ Execução

Execute o script:

```bash
python relatorio_vendas.py
```

Ao finalizar:

* O relatório será gerado automaticamente
* O e-mail será enviado para os destinatários configurados

---

## 📧 Relatório Gerado

* ✔ Tabela HTML com valores formatados
* ✔ Percentual de participação mensal
* ✔ Layout simples e compatível com clientes de e-mail
* ✔ Mensagem automática padronizada

---

## 🔄 Automação

### Windows — Agendador de Tarefas

* Criar tarefa diária, semanal ou mensal
* Executar o Python apontando para o script

### Linux — cron

```bash
0 8 1 * * python /caminho/relatorio_vendas.py
```

---

## 🔒 Segurança

* ✔ Credenciais protegidas por variáveis de ambiente
* ✔ Código seguro para versionamento público
* ✔ Fácil adaptação para ambientes DEV / PROD

---

## 👨‍💻 Autor

**Ernando Freitas**

---

## 📄 Licença

Este projeto é destinado a uso interno ou educacional.
A redistribuição pode ser feita conforme necessidade do projeto.

Só avisar 🚀
