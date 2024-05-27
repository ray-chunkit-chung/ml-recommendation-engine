
# Use a base image with Python and required dependencies
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install any required Python packages
RUN pip install tensorflow keras fastapi uvicorn python-multipart python-dotenv

# Copy your model-serving code and model files into the container
# COPY local/model.h5 /app/
ADD https://drive.google.com/uc?id=17ouuvFwKWuyQvFT4dmclKk8r3pf2tQmb&export=download /app/model.h5
COPY src/serve.py /app/

# Expose the port your REST API will run on
EXPOSE 5000

# Set model path as an environment variable
ENV MODEL_PATH=/app/model.h5

# Define the command to run your model-serving script
CMD ["python", "serve.py"]

# Build and run the container locally:
# docker build -t raychung/recommendation-engine-serving-container .
# docker run -p 5000:5000 raychung/recommendation-engine-serving-container