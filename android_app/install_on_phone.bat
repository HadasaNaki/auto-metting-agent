@echo off
echo 📱 Installing SmartAgent on your phone...
echo ==========================================

cd /d "c:\Users\hnaki\OneDrive - Intel Corporation\Desktop\Smart Agent\android_app"

echo 🔍 Checking connected devices...
adb devices

echo.
echo 📱 Installing APK...
adb install -r app\build\outputs\apk\debug\app-debug.apk

if errorlevel 1 (
    echo ❌ Installation failed!
    echo.
    echo 🔧 Troubleshooting:
    echo 1. Make sure USB Debugging is enabled
    echo 2. Make sure you authorized the computer on your phone
    echo 3. Try running: adb devices
    echo 4. If no devices shown, check USB cable and phone settings
    pause
    exit /b 1
)

echo ✅ Installation successful!
echo.
echo 🚀 Starting the app...
adb shell am start -n com.smartagent.technician.debug/com.smartagent.technician.MainActivity

echo.
echo 🎉 App should now be running on your phone!
echo 📱 Look for "SmartAgent טכנאי" app on your phone

pause
