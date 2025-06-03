# Use the official Streamlit image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local files to the container
COPY dashboard dashboard
COPY app.py app.py


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


# Install any necessary Python dependencies
RUN pip install --no-cache-dir streamlit pandas plotly 

# Expose the Streamlit default port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]