# Usando a imagem oficial do LaTeX como base
FROM texlive/texlive:latest

# Instalar Python e pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copiar o requirements.txt para o diretório de trabalho e instalar as dependências do Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código da aplicação para o diretório /app
COPY . /app
WORKDIR /app

# Verificar se o pdflatex está disponível no ambiente
RUN pdflatex --version

# Comando para rodar a aplicação Flask com Gunicorn
CMD ["gunicorn", "app:app"]
