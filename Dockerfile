# Use the official Python image with the specific version
FROM python:3.12.5-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt if you have one
COPY requirements.txt ./

# Install dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the source code into the container
COPY src/ .

# Expose Streamlit's default port
EXPOSE 8501

# # Set the entry point command
# CMD ["python", "main.py"]

# Set the entry point command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
