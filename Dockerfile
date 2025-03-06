FROM python:3.9-slim

# Install essential build tools, Git, plus clean up
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install your own dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone roop from GitHub
RUN git clone --depth 1 https://github.com/s0md3v/roop.git roop

# Comment out GPU dependencies in roop's requirements
RUN sed -i 's/onnxruntime-gpu==1.15.1/# onnxruntime-gpu==1.15.1/' roop/requirements.txt

# Install roop's dependencies
RUN pip install --no-cache-dir -r roop/requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "main.py"]