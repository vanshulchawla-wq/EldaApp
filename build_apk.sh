#!/bin/bash
# Build Elda APK using Docker
# Usage: ./build_apk.sh [onboard|directory]

APP_MODE=${1:-onboard}

echo "🔨 Building Elda APK ($APP_MODE mode)..."

# Set the correct main file
if [ "$APP_MODE" = "directory" ]; then
    cp main.py _main_backup.py 2>/dev/null
    echo "Building Directory app..."
else
    # For onboard, rename onboard.py to main.py (buildozer expects main.py)
    cp main.py _main_backup.py 2>/dev/null
    cp onboard.py main.py
    echo "Building Onboard app..."
fi

# Build Docker image
docker build -t elda-builder .

# Run the build
docker run --rm -v "$(pwd)/bin:/app/bin" -v "$(pwd)/.buildozer:/app/.buildozer" elda-builder

# Restore original main.py
if [ -f _main_backup.py ]; then
    mv _main_backup.py main.py
fi

echo ""
echo "✅ Done! APK should be in ./bin/"
ls -la bin/*.apk 2>/dev/null || echo "❌ No APK found. Check build logs above."
