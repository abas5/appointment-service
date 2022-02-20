# Retrevive Python image from DockerHub
FROM python:3.7.4

# Working Directory
WORKDIR /app


COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
COPY src/ .

# Run the container
CMD ["gunicorn"  , "-b", "0.0.0.0:82", "app:app"]
