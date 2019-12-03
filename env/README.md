## Base Image 
python:3.7-stretch

## Base Packages
apt-get install -y \
    bzip2 \
    ca-certificates \
    curl \
    gcc \
    git \
    libc-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    wget \
    libevent-dev \
    build-essential \
    tmux \
    vim

## Requirements
numpy==1.17.4
pandas==0.25.2
scipy==1.3.2
joblib==0.14.0
scikit-learn==0.21.3
jupyterlab==1.2.3

