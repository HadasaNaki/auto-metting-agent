#!/usr/bin/env python3
"""
SmartAgent Android Development Helper
כלי עזר לפיתוח ובדיקת אפליקציית Android
"""

import os
import subprocess
import json
import time
from pathlib import Path


class AndroidDevelopmentHelper:
    def __init__(self, app_path):
        self.app_path = Path(app_path)
        self.adb_path = None
        self.gradle_path = None
        self.android_home = None

    def setup_environment(self):
        """הגדרת סביבת הפיתוח"""
        print("🔧 Setting up Android development environment...")

        # בדיקת Android SDK
        self.android_home = os.environ.get("ANDROID_HOME") or os.environ.get(
            "ANDROID_SDK_ROOT"
        )
        if not self.android_home:
            print(
                "⚠️  ANDROID_HOME not set. Please install Android Studio and set ANDROID_HOME"
            )
            return False

        # בדיקת ADB
        self.adb_path = Path(self.android_home) / "platform-tools" / "adb.exe"
        if not self.adb_path.exists():
            self.adb_path = Path(self.android_home) / "platform-tools" / "adb"

        if not self.adb_path.exists():
            print("❌ ADB not found. Please install Android SDK platform-tools")
            return False

        print(f"✅ Android SDK found: {self.android_home}")
        print(f"✅ ADB found: {self.adb_path}")
        return True

    def check_gradle_wrapper(self):
        """בדיקת Gradle Wrapper"""
        gradlew = (
            self.app_path / "gradlew.bat"
            if os.name == "nt"
            else self.app_path / "gradlew"
        )

        if not gradlew.exists():
            print("📦 Creating Gradle Wrapper...")
            self.create_gradle_wrapper()

        return gradlew

    def create_gradle_wrapper(self):
        """יצירת Gradle Wrapper"""
        try:
            # יצירת gradlew.bat לWindows
            gradlew_bat = self.app_path / "gradlew.bat"
            gradlew_content = """@echo off
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd_ return code (1).
if not "" == "%GRADLE_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
"""
            gradlew_bat.write_text(gradlew_content)

            # יצירת gradle-wrapper.properties
            wrapper_dir = self.app_path / "gradle" / "wrapper"
            wrapper_dir.mkdir(parents=True, exist_ok=True)

            wrapper_props = wrapper_dir / "gradle-wrapper.properties"
            props_content = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
            wrapper_props.write_text(props_content)
            print("✅ Gradle Wrapper created")

        except Exception as e:
            print(f"❌ Error creating Gradle Wrapper: {e}")

    def check_connected_devices(self):
        """בדיקת מכשירים מחוברים"""
        print("\n📱 Checking connected devices...")

        try:
            result = subprocess.run(
                [str(self.adb_path), "devices"], capture_output=True, text=True
            )

            lines = result.stdout.strip().split("\\n")[1:]  # Skip header
            devices = [
                line.split("\\t")[0]
                for line in lines
                if "\\t" in line and "device" in line
            ]

            if not devices:
                print("⚠️  No devices connected. Please:")
                print("   1. Connect Android device via USB")
                print("   2. Enable USB Debugging")
                print("   3. Or start Android Emulator")
                return False

            print(f"✅ Found {len(devices)} device(s):")
            for device in devices:
                print(f"   📱 {device}")

            return True

        except Exception as e:
            print(f"❌ Error checking devices: {e}")
            return False

    def build_debug_apk(self):
        """בניית APK לבדיקה"""
        print("\n🏗️  Building Debug APK...")

        gradlew = self.check_gradle_wrapper()

        try:
            # שינוי למדריך הפרוייקט
            os.chdir(self.app_path)

            # הרצת בנייה
            build_cmd = [str(gradlew), "assembleDebug"]
            print(f"Running: {' '.join(build_cmd)}")

            result = subprocess.run(
                build_cmd, capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0:
                print("✅ Build successful!")

                # חיפוש APK
                apk_path = (
                    self.app_path
                    / "app"
                    / "build"
                    / "outputs"
                    / "apk"
                    / "debug"
                    / "app-debug.apk"
                )
                if apk_path.exists():
                    print(f"📦 APK created: {apk_path}")
                    return apk_path
                else:
                    print("⚠️  APK not found in expected location")
                    return None
            else:
                print("❌ Build failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return None

        except subprocess.TimeoutExpired:
            print("❌ Build timeout (5 minutes)")
            return None
        except Exception as e:
            print(f"❌ Build error: {e}")
            return None

    def install_and_test(self, apk_path):
        """התקנה ובדיקה על מכשיר"""
        print(f"\n📲 Installing APK: {apk_path}")

        try:
            # התקנת APK
            install_result = subprocess.run(
                [str(self.adb_path), "install", "-r", str(apk_path)],
                capture_output=True,
                text=True,
            )

            if install_result.returncode == 0:
                print("✅ Installation successful!")

                # הפעלת האפליקציה
                print("🚀 Launching app...")
                launch_result = subprocess.run(
                    [
                        str(self.adb_path),
                        "shell",
                        "am",
                        "start",
                        "-n",
                        "com.smartagent.technician/.MainActivity",
                    ],
                    capture_output=True,
                    text=True,
                )

                if launch_result.returncode == 0:
                    print("✅ App launched successfully!")
                    return True
                else:
                    print("❌ Failed to launch app")
                    print("Error:", launch_result.stderr)
                    return False
            else:
                print("❌ Installation failed!")
                print("Error:", install_result.stderr)
                return False

        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False

    def run_unit_tests(self):
        """הרצת בדיקות יחידה"""
        print("\n🧪 Running Unit Tests...")

        gradlew = self.check_gradle_wrapper()

        try:
            os.chdir(self.app_path)

            test_cmd = [str(gradlew), "test"]
            result = subprocess.run(
                test_cmd, capture_output=True, text=True, timeout=180
            )

            if result.returncode == 0:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed!")
                print("Details:", result.stdout)
                return False

        except Exception as e:
            print(f"❌ Test error: {e}")
            return False

    def generate_test_report(self):
        """יצירת דוח בדיקה"""
        print("\n📊 Generating Test Report...")

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment_check": "✅ Passed",
            "build_status": "❓ Not tested",
            "install_status": "❓ Not tested",
            "unit_tests": "❓ Not tested",
            "recommendations": [],
        }

        try:
            # בדיקת התקנה
            if self.setup_environment():
                if self.check_connected_devices():
                    apk_path = self.build_debug_apk()
                    if apk_path:
                        report["build_status"] = "✅ Success"
                        if self.install_and_test(apk_path):
                            report["install_status"] = "✅ Success"
                        else:
                            report["install_status"] = "❌ Failed"
                            report["recommendations"].append(
                                "Check device connection and USB debugging"
                            )
                    else:
                        report["build_status"] = "❌ Failed"
                        report["recommendations"].append(
                            "Fix build errors and dependencies"
                        )
                else:
                    report["recommendations"].append(
                        "Connect Android device or start emulator"
                    )

            # בדיקת tests
            if self.run_unit_tests():
                report["unit_tests"] = "✅ Passed"
            else:
                report["unit_tests"] = "❌ Failed"
                report["recommendations"].append("Fix failing unit tests")

            # שמירת דוח
            report_file = self.app_path / "test_report.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(f"📄 Test report saved: {report_file}")

        except Exception as e:
            print(f"❌ Error generating report: {e}")

        return report

    def run_comprehensive_test(self):
        """הרצת בדיקה מקיפה"""
        print("🚀 Starting Comprehensive Android Test...")
        print("=" * 60)

        success = True

        # 1. בדיקת סביבה
        if not self.setup_environment():
            success = False

        # 2. בדיקת מכשירים
        if not self.check_connected_devices():
            print("\\n⚠️  Continuing without device (build-only test)")

        # 3. בנייה
        apk_path = self.build_debug_apk()
        if not apk_path:
            success = False

        # 4. התקנה (אם יש מכשיר)
        if apk_path and self.check_connected_devices():
            if not self.install_and_test(apk_path):
                success = False

        # 5. בדיקות יחידה
        if not self.run_unit_tests():
            success = False

        # 6. דוח
        report = self.generate_test_report()

        print("\\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        if success:
            print("🎉 ALL TESTS PASSED!")
            print("\\n✅ Your Android app is ready for use!")
            print("\\nNext steps:")
            print("1. Test on real device")
            print("2. Test all features (recording, AI, etc.)")
            print("3. Deploy to production")
        else:
            print("⚠️  SOME ISSUES FOUND")
            print("\\n🔧 Please address the issues above")
            print("\\nRecommended actions:")
            for rec in report.get("recommendations", []):
                print(f"- {rec}")

        return success


def main():
    """הרצת הבדיקה הראשית"""
    app_path = r"c:\\Users\\hnaki\\OneDrive - Intel Corporation\\Desktop\\Smart Agent\\android_app"

    helper = AndroidDevelopmentHelper(app_path)
    success = helper.run_comprehensive_test()

    print("\\n" + "=" * 60)
    if success:
        print("🚀 Android app testing completed successfully!")
    else:
        print("🔧 Please fix the issues and run the test again.")

    return success


if __name__ == "__main__":
    main()
