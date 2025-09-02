@echo off
echo 🚀 Building SmartAgent Android App...
echo ============================================

cd /d "c:\Users\hnaki\OneDrive - Intel Corporation\Desktop\Smart Agent\android_app"

echo 📱 Step 1: Cleaning previous builds...
call gradlew.bat clean

echo 🔧 Step 2: Building debug APK...
call gradlew.bat assembleDebug

if errorlevel 1 (
    echo ❌ Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Build successful!
echo 📦 APK location: app\build\outputs\apk\debug\app-debug.apk

echo.
echo 📱 Next steps to install on your phone:
echo 1. Enable Developer Options on your phone
echo 2. Enable USB Debugging
echo 3. Connect phone to computer
echo 4. Run: install_on_phone.bat

pause
