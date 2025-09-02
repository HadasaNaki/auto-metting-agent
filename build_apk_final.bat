@echo off
echo =========================================
echo    🚀 SmartAgent - Quick APK Builder  
echo =========================================

cd /d "%~dp0android_app"

echo ✅ Cleaning previous builds...
call gradlew clean

echo 🔨 Building APK...
call gradlew assembleDebug

echo 📱 APK Location:
echo %cd%\app\build\outputs\apk\debug\app-debug.apk

echo.
echo 🎉 Build Complete! Check above path for APK file.
echo.
echo To install on phone:
echo 1. Enable "Unknown Sources" in phone settings
echo 2. Transfer APK to phone  
echo 3. Open APK file and install
echo.
pause
