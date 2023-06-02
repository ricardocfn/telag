# Use a base de imagem do Python 3.11
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o contêiner
COPY . /app

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando de inicialização para o bot
CMD [ "python", "app.py" ]
