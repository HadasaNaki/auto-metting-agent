@echo off
echo 🔍 Quick Android Development Check...
echo =====================================

echo 📍 Current directory:
cd

echo.
echo ☕ Checking Java installation...
java -version
if errorlevel 1 (
    echo ❌ Java not found! Please install Java JDK 11 or higher
    echo Download from: https://adoptium.net/
    pause
    exit /b 1
)

echo.
echo 📱 Checking Android SDK (if installed)...
if defined ANDROID_HOME (
    echo ✅ ANDROID_HOME: %ANDROID_HOME%
    if exist "%ANDROID_HOME%\platform-tools\adb.exe" (
        echo ✅ ADB found
        "%ANDROID_HOME%\platform-tools\adb.exe" version
    ) else (
        echo ⚠️ ADB not found in platform-tools
    )
) else (
    echo ⚠️ ANDROID_HOME not set
    echo 💡 For phone installation, install Android Studio or SDK tools
)

echo.
echo 📁 Checking project structure...
if exist "app\build.gradle" (
    echo ✅ app\build.gradle found
) else (
    echo ❌ app\build.gradle missing
)

if exist "gradlew.bat" (
    echo ✅ gradlew.bat found
) else (
    echo ❌ gradlew.bat missing
)

echo.
echo 🚀 Ready to build? Choose option:
echo 1. Build APK for manual installation
echo 2. Build and install on connected phone (requires ADB)
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo Starting APK build...
    call build_apk.bat
) else if "%choice%"=="2" (
    echo Building and installing...
    call build_apk.bat
    if not errorlevel 1 call install_on_phone.bat
) else (
    echo Goodbye!
)

pause
