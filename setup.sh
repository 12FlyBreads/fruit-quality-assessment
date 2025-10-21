#!/bin/bash

echo "=============================="
echo "🍏 Setting up Fruit & Veg Quality environment"
echo "=============================="

# Define environment name
VENV_DIR=".fnvq-env"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv $VENV_DIR

# Activate venv
echo "⚙️  Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "⬆️  Updating pip..."
pip install --upgrade pip

# Install core dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Detect platform
ARCH=$(uname -m)
DEVICE=$(uname -n)

echo "🔍 Detected architecture: $ARCH"
echo "🔍 Device name: $DEVICE"

# Check if running on Raspberry Pi (ARM architecture)
if [[ "$ARCH" == "armv7l" || "$ARCH" == "aarch64" ]]; then
    echo "🐍 Installing TensorFlow Lite Runtime for Raspberry Pi..."
    # Choose version based on architecture
    if [[ "$ARCH" == "aarch64" ]]; then
        pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.14.0-cp311-cp311-linux_aarch64.whl
    else
        pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.14.0-cp311-cp311-linux_armv7l.whl
    fi
else
    echo "💻 Non-ARM architecture detected. Installing full TensorFlow..."
    pip install tensorflow
fi

echo "✅ Environment setup complete!"
echo "To activate it later, run:"
echo "source $VENV_DIR/bin/activate"
