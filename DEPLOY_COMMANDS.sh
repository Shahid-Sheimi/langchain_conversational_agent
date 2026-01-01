#!/bin/bash
# Commands for deploying to Hugging Face Spaces
# Usage: Follow these commands step by step

echo "=========================================="
echo "Hugging Face Spaces Deployment Commands"
echo "=========================================="
echo ""

# Step 1: Create Space on Hugging Face (do this in browser first)
echo "STEP 1: Create Space on Hugging Face"
echo "  1. Go to: https://huggingface.co/spaces"
echo "  2. Click 'Create new Space'"
echo "  3. Choose name, select 'Docker' SDK, choose hardware"
echo "  4. Click 'Create Space'"
echo ""
read -p "Press Enter after creating your Space..."

# Step 2: Get Space repository URL
echo ""
echo "STEP 2: Clone your Space repository"
echo "  Replace YOUR_USERNAME and YOUR_SPACE_NAME below:"
echo ""
SPACE_URL="https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME"
echo "  Space URL format: $SPACE_URL"
echo ""
read -p "Enter your Space repository URL (or username/space-name): " SPACE_INPUT

# Parse input
if [[ $SPACE_INPUT == *"huggingface.co"* ]]; then
    SPACE_REPO=$(echo $SPACE_INPUT | sed 's|https://huggingface.co/spaces/||')
else
    SPACE_REPO=$SPACE_INPUT
fi

SPACE_USER=$(echo $SPACE_REPO | cut -d'/' -f1)
SPACE_NAME=$(echo $SPACE_REPO | cut -d'/' -f2)

echo ""
echo "Detected: User=$SPACE_USER, Space=$SPACE_NAME"
echo ""

# Step 3: Clone repository
echo "STEP 3: Cloning Space repository..."
CLONE_URL="https://huggingface.co/spaces/$SPACE_REPO"
echo "  Clone URL: $CLONE_URL"
echo ""

if [ -d "$SPACE_NAME" ]; then
    echo "  Directory $SPACE_NAME already exists. Removing..."
    rm -rf "$SPACE_NAME"
fi

git clone $CLONE_URL
cd "$SPACE_NAME"

# Step 4: Copy files
echo ""
echo "STEP 4: Copying files to Space repository..."
echo ""

# Copy Dockerfile (rename from Dockerfile.hf)
cp ../Dockerfile.hf ./Dockerfile
echo "  ✓ Copied Dockerfile.hf → Dockerfile"

# Copy startup script
cp ../start_hf.sh ./
chmod +x ./start_hf.sh
echo "  ✓ Copied start_hf.sh (made executable)"

# Copy requirements
cp ../requirements.txt ./
echo "  ✓ Copied requirements.txt"

# Copy application code
cp -r ../api ./
echo "  ✓ Copied api/ directory"

cp -r ../frontend ./
echo "  ✓ Copied frontend/ directory"

# Copy README template
cp ../README_HF.md ./README.md
echo "  ✓ Copied README_HF.md → README.md"

echo ""
echo "STEP 5: Files ready! Now configure environment variables:"
echo "  1. Go to: https://huggingface.co/spaces/$SPACE_REPO/settings"
echo "  2. Navigate to 'Variables and secrets'"
echo "  3. Add Secret: OPENAI_API_KEY = your_api_key_here"
echo "  4. Optionally add Variable: API_BASE_URL = http://localhost:8000"
echo ""
read -p "Press Enter after configuring environment variables..."

# Step 6: Commit and push
echo ""
echo "STEP 6: Committing and pushing to Space..."
echo ""

git add .
git commit -m "Initial deployment of PDF Chatbot"
echo ""
echo "Pushing to Hugging Face Spaces..."
git push

echo ""
echo "=========================================="
echo "Deployment initiated!"
echo "=========================================="
echo ""
echo "Monitor build progress at:"
echo "  https://huggingface.co/spaces/$SPACE_REPO"
echo ""
echo "Your app will be available at:"
echo "  https://$SPACE_USER-$SPACE_NAME.hf.space"
echo ""

