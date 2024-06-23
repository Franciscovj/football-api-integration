#football-api-integration

# Instalação de Dependências

Este guia explica como instalar as dependências do projeto usando o arquivo `requirements.txt`.

## Requisitos

Certifique-se de ter o Python instalado. Este projeto foi testado com Python 3.x.

## Passos para Instalar as Dependências

### 1. Criar um Ambiente Virtual (Recomendado)

É altamente recomendado criar um ambiente virtual para isolar as dependências do projeto. Use os comandos abaixo para criar e ativar um ambiente virtual:

```sh
# Criar o ambiente virtual
python -m venv env

# Ativar o ambiente virtual
# No Windows
env\Scripts\activate

# No macOS/Linux
source env/bin/activate


pip freeze > requirements.txt
