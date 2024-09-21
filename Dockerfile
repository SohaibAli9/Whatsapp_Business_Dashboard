# Use an official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt ./

# Install the required Python packages.
RUN pip install -r requirements.txt

# Copy the rest of your app's code into the container.
COPY . .

# Expose the port that Cloud Run uses.
EXPOSE 8080

# Run your Streamlit app with dynamic port.
CMD ["streamlit", "run", "streamlit_frontend.py", "--server.port", "8080", "--server.address=0.0.0.0"]
