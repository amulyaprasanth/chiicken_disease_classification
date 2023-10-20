FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the local directory contents to the container at /app
COPY . .

# Install the Python dependencies from requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# Specify the command to run your application
CMD ["python3", "app.py"]