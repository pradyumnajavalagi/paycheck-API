# Dockerfile

# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy the requirements file and install dependencies first
# This takes advantage of Docker's layer caching
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 4. Copy the rest of the application code into the container
COPY . .

# 5. Expose the port the app runs on
EXPOSE 8000

# 6. Define the command to run your app
# Use 0.0.0.0 to make the server accessible from outside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]