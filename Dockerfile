FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git zip unzip sudo wget curl \
    openjdk-11-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    cmake libffi-dev libssl-dev \
    build-essential ccache \
    lld \
    && rm -rf /var/lib/apt/lists/*

# Install buildozer and cython
RUN pip install --no-cache-dir buildozer cython virtualenv

# Set Java home
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Create working directory
WORKDIR /app

# Copy app source
COPY . /app/

# Build APK
CMD ["buildozer", "android", "debug"]
