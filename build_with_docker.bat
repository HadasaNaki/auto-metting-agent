@echo off
echo 🐳 בניית SmartAgent APK עם Docker
echo =====================================

echo 📦 שלב 1: בניית Docker image...
docker build -f Dockerfile.android -t smartagent-builder .

if errorlevel 1 (
    echo ❌ בניית Docker image נכשלה!
    echo 💡 וודא ש-Docker Desktop מותקן ופועל
    pause
    exit /b 1
)

echo 🚀 שלב 2: בניית APK בתוך Container...
docker run --rm -v "%CD%\android_app\app\build\outputs:/app/app/build/outputs" smartagent-builder

if errorlevel 1 (
    echo ❌ בניית APK נכשלה!
    pause
    exit /b 1
)

echo ✅ בניה הושלמה בהצלחה!
echo 📱 APK נמצא ב: android_app\app\build\outputs\apk\debug\app-debug.apk

echo.
echo 🎯 השלבים הבאים:
echo 1. העבר את app-debug.apk לטלפון
echo 2. אפשר "מקורות לא ידועים" בהגדרות
echo 3. התקן את האפליקציה
echo.

pause
