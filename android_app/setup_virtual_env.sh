#!/bin/bash

# Virtual Environment Setup Script for Android Development
# Usage: ./setup_virtual_env.sh

echo "🔧 Setting up Virtual Android Development Environment..."

# Create virtual directory structure
mkdir -p ./virtual_env
cd ./virtual_env

# Download portable OpenJDK
echo "📥 Downloading OpenJDK..."
wget -O openjdk.tar.gz https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
tar -xzf openjdk.tar.gz
export JAVA_HOME=$(pwd)/jdk-17.0.2
export PATH=$JAVA_HOME/bin:$PATH

# Download Android Command Line Tools
echo "📥 Downloading Android SDK..."
wget -O cmdtools.zip https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip cmdtools.zip
mkdir -p android-sdk/cmdline-tools
mv cmdline-tools android-sdk/cmdline-tools/latest
export ANDROID_SDK_ROOT=$(pwd)/android-sdk
export PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH

# Accept licenses and install components
echo "📦 Installing Android SDK components..."
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

echo "✅ Virtual environment ready!"
echo "🚀 To use: source ./virtual_env/activate.sh"

# Create activation script
cat > activate.sh << 'EOF'
#!/bin/bash
export JAVA_HOME=$(pwd)/jdk-17.0.2
export ANDROID_SDK_ROOT=$(pwd)/android-sdk
export PATH=$JAVA_HOME/bin:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH
echo "✅ Virtual Android environment activated!"
echo "Java: $(java -version 2>&1 | head -1)"
echo "SDK: $ANDROID_SDK_ROOT"
EOF

chmod +x activate.sh
echo "📋 Created activation script: ./virtual_env/activate.sh"
