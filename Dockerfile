# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar archivos al contenedor
COPY . .

# Exponer el puerto donde corre Flask
EXPOSE 8000

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]