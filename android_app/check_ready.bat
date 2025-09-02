@echo off
echo 🎯 בדיקת מוכנות SmartAgent לפתיחה ב-Android Studio
echo =====================================================

cd /d "C:\Users\hnaki\OneDrive - Intel Corporation\Desktop\Smart Agent\android_app"

echo ✅ בודק קבצי פרוייקט חיוניים...
if exist "build.gradle" (
    echo ✅ build.gradle נמצא
) else (
    echo ❌ build.gradle חסר!
    goto :error
)

if exist "settings.gradle" (
    echo ✅ settings.gradle נמצא
) else (
    echo ❌ settings.gradle חסר!
    goto :error
)

if exist "app\build.gradle" (
    echo ✅ app\build.gradle נמצא
) else (
    echo ❌ app\build.gradle חסר!
    goto :error
)

if exist "app\src\main\AndroidManifest.xml" (
    echo ✅ AndroidManifest.xml נמצא
) else (
    echo ❌ AndroidManifest.xml חסר!
    goto :error
)

if exist "app\src\main\java\com\smartagent\technician\MainActivity.kt" (
    echo ✅ MainActivity.kt נמצא
) else (
    echo ❌ MainActivity.kt חסר!
    goto :error
)

echo.
echo 🎉 כל הקבצים החיוניים נמצאים!
echo 📂 נתיב הפרוייקט: %CD%
echo.
echo 🚀 מוכן לפתיחה ב-Android Studio!
echo.
echo השלבים הבאים:
echo 1. פתח Android Studio
echo 2. לחץ "Open"
echo 3. בחר: %CD%
echo 4. חכה ל-Gradle Sync
echo 5. חבר טלפון והרץ!
echo.
pause
goto :end

:error
echo.
echo ❌ נמצאו בעיות! אנא בדוק את התיקייה.
pause

:end
