# Use the official Python 3.10 slim-buster image as the base image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the local directory contents to the container at /app
COPY . .

# Install the Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Specify the command to run your application
CMD ["python3", "app.py"]
