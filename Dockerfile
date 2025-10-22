# Use a small official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy all local files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Start the Streamlit app
CMD ["streamlit", "run", "wine_recommender.py", "--server.port=8080", "--server.address=0.0.0.0"]
