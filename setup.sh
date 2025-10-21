#!/bin/bash

echo "=============================="
echo "🍏 Setting up Fruit & Veg Quality environment"
echo "=============================="

# Define environment name
VENV_DIR=".fnvq-env"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv $VENV_DIR --system-site-packages

# Activate venv
echo "⚙️  Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "⬆️  Updating pip..."
pip install --upgrade pip

# Install core dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✅ Dependencies installed."

# Detect platform
ARCH=$(uname -m)
DEVICE=$(uname -n)

echo "🔍 Detected architecture: $ARCH"
echo "🔍 Device name: $DEVICE"

echo "📥 Checking Installations..."

pip list

echo "✅ Environment setup complete!"
echo "To activate it later, run:"
echo "source $VENV_DIR/bin/activate"
echo "deactivate to exit the environment."
