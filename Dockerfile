# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Exponer el puerto donde corre Flask
EXPOSE 8000

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]