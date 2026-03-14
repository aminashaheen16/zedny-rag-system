# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g., for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container at /app
COPY . .

# Create a non-root user and switch to it for security (Optional but recommended for HF)
RUN useradd -m myuser
USER myuser

# Make port 7860 available to the world outside this container
# Hugging Face Spaces uses port 7860 by default
EXPOSE 7860

# Define environment variables (These should ideally be set in HF Space Settings as Secrets)
# ENV OPENROUTER_API_KEY=your_key_here
# ENV COHERE_API_KEY=your_key_here
# ENV SUPABASE_URL=your_url_here
# ENV SUPABASE_KEY=your_key_here

# Run uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
