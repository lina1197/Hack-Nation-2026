#!/bin/bash

echo "=========================================="
echo "Virtue Foundation IDP Agent Setup"
echo "GitHub Codespaces Edition"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3 first."
    exit 1
fi
echo "✓ pip3 found"
echo ""

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Check for ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY environment variable not set"
    echo ""
    echo "To set it in GitHub Codespaces:"
    echo "  1. Go to https://github.com/settings/codespaces"
    echo "  2. Click 'New secret'"
    echo "  3. Name: ANTHROPIC_API_KEY"
    echo "  4. Value: your API key from https://console.anthropic.com/"
    echo "  5. Restart your Codespace"
    echo ""
    echo "Or set it temporarily in this session:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
else
    echo "✓ ANTHROPIC_API_KEY is set"
    echo ""
fi

# Check if dataset exists
if [ -f "Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv" ]; then
    echo "✓ Dataset found in root folder"
elif [ -f "/mnt/user-data/uploads/Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv" ]; then
    echo "✓ Dataset found in uploads folder"
    echo "  Copying to root folder for easier access..."
    cp /mnt/user-data/uploads/Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv .
    echo "✓ Dataset copied to root folder"
else
    echo "⚠️  Dataset not found!"
    echo "  Please ensure Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv is in the root folder"
    echo ""
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  python3 app.py"
echo ""
echo "The Gradio interface will be available at the forwarded port."
echo "Look for the 'Ports' tab in VS Code to access it."
echo ""
echo "To view MLflow experiments:"
echo "  mlflow ui"
echo "  Then access via the forwarded port 5000"
echo ""