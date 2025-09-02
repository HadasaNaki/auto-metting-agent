#!/usr/bin/env python3
"""
SmartAgent Android App Validator
כלי בדיקה מקיף לאפליקציית Android
"""

import os
import json
import re
from pathlib import Path


class AndroidAppValidator:
    def __init__(self, app_path):
        self.app_path = Path(app_path)
        self.test_results = []
        self.issues_found = []
        self.total_tests = 0
        self.passed_tests = 0

    def run_all_tests(self):
        """הרצת כל הבדיקות"""
        print("🚀 Starting Android App Validation...")
        print("=" * 60)

        # בדיקות מבנה
        self.test_project_structure()
        self.test_gradle_configuration()
        self.test_manifest_configuration()

        # בדיקות קוד
        self.test_kotlin_files()
        self.test_database_structure()
        self.test_ui_components()

        # בדיקות משאבים
        self.test_resources()
        self.test_strings_localization()

        # דוח סיכום
        self.generate_report()

    def test_project_structure(self):
        """בדיקת מבנה הפרוייקט"""
        print("\n📁 Testing Project Structure...")

        required_dirs = [
            "app",
            "app/src",
            "app/src/main",
            "app/src/main/java",
            "app/src/main/java/com",
            "app/src/main/java/com/smartagent",
            "app/src/main/java/com/smartagent/technician",
            "app/src/main/res",
            "app/src/main/res/values",
            "app/src/main/res/layout",
        ]

        for dir_path in required_dirs:
            full_path = self.app_path / dir_path
            if full_path.exists():
                print(f"  ✅ {dir_path}")
                self.passed_tests += 1
            else:
                print(f"  ❌ {dir_path} - Missing")
                self.issues_found.append(f"Missing directory: {dir_path}")
            self.total_tests += 1

        required_files = [
            "build.gradle",
            "app/build.gradle",
            "app/src/main/AndroidManifest.xml",
            "README.md",
        ]

        for file_path in required_files:
            full_path = self.app_path / file_path
            if full_path.exists():
                print(f"  ✅ {file_path}")
                self.passed_tests += 1
            else:
                print(f"  ❌ {file_path} - Missing")
                self.issues_found.append(f"Missing file: {file_path}")
            self.total_tests += 1

    def test_gradle_configuration(self):
        """בדיקת קונפיגורציית Gradle"""
        print("\n🔧 Testing Gradle Configuration...")

        gradle_file = self.app_path / "app" / "build.gradle"
        if not gradle_file.exists():
            print("  ❌ app/build.gradle not found")
            self.issues_found.append("Missing app/build.gradle")
            self.total_tests += 1
            return

        try:
            content = gradle_file.read_text(encoding="utf-8")

            # בדיקת dependencies חיוניות
            required_deps = [
                "androidx.core:core-ktx",
                "androidx.compose.ui:ui",
                "androidx.room:room-runtime",
                "com.google.dagger:hilt-android",
                "androidx.navigation:navigation-compose",
            ]

            for dep in required_deps:
                if dep in content:
                    print(f"  ✅ Dependency: {dep}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing dependency: {dep}")
                    self.issues_found.append(f"Missing dependency: {dep}")
                self.total_tests += 1

            # בדיקת הגדרות חיוניות
            required_configs = [
                "compileSdk",
                "minSdk",
                "targetSdk",
                "compose true",
                "kotlin-kapt",
            ]

            for config in required_configs:
                if config in content:
                    print(f"  ✅ Configuration: {config}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing configuration: {config}")
                    self.issues_found.append(f"Missing configuration: {config}")
                self.total_tests += 1

        except Exception as e:
            print(f"  ❌ Error reading build.gradle: {e}")
            self.issues_found.append(f"Error reading build.gradle: {e}")
            self.total_tests += 1

    def test_manifest_configuration(self):
        """בדיקת AndroidManifest.xml"""
        print("\n📋 Testing Android Manifest...")

        manifest_file = self.app_path / "app" / "src" / "main" / "AndroidManifest.xml"
        if not manifest_file.exists():
            print("  ❌ AndroidManifest.xml not found")
            self.issues_found.append("Missing AndroidManifest.xml")
            self.total_tests += 1
            return

        try:
            content = manifest_file.read_text(encoding="utf-8")

            # בדיקת הרשאות חיוניות
            required_permissions = [
                "android.permission.INTERNET",
                "android.permission.RECORD_AUDIO",
                "android.permission.ACCESS_FINE_LOCATION",
                "android.permission.CALL_PHONE",
            ]

            for permission in required_permissions:
                if permission in content:
                    print(f"  ✅ Permission: {permission}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing permission: {permission}")
                    self.issues_found.append(f"Missing permission: {permission}")
                self.total_tests += 1

            # בדיקת רכיבים חיוניים
            required_components = [
                "MainActivity",
                "SmartAgentApplication",
                "android.intent.action.MAIN",
                "android.intent.category.LAUNCHER",
            ]

            for component in required_components:
                if component in content:
                    print(f"  ✅ Component: {component}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing component: {component}")
                    self.issues_found.append(f"Missing component: {component}")
                self.total_tests += 1

        except Exception as e:
            print(f"  ❌ Error reading AndroidManifest.xml: {e}")
            self.issues_found.append(f"Error reading AndroidManifest.xml: {e}")
            self.total_tests += 1

    def test_kotlin_files(self):
        """בדיקת קבצי Kotlin"""
        print("\n🔷 Testing Kotlin Files...")

        kotlin_files = [
            "app/src/main/java/com/smartagent/technician/MainActivity.kt",
            "app/src/main/java/com/smartagent/technician/SmartAgentApplication.kt",
            "app/src/main/java/com/smartagent/technician/data/database/Database.kt",
            "app/src/main/java/com/smartagent/technician/service/AudioProcessingService.kt",
            "app/src/main/java/com/smartagent/technician/ai/AIServices.kt",
            "app/src/main/java/com/smartagent/technician/ui/main/MainScreen.kt",
            "app/src/main/java/com/smartagent/technician/ui/main/MainViewModel.kt",
            "app/src/main/java/com/smartagent/technician/ui/record/RecordCallScreen.kt",
        ]

        for file_path in kotlin_files:
            full_path = self.app_path / file_path
            if full_path.exists():
                # בדיקת תוכן הקובץ
                try:
                    content = full_path.read_text(encoding="utf-8")
                    if (
                        len(content) > 100
                        and "package com.smartagent.technician" in content
                    ):
                        print(f"  ✅ {file_path}")
                        self.passed_tests += 1
                    else:
                        print(f"  ⚠️  {file_path} - Content incomplete")
                        self.issues_found.append(f"Incomplete content: {file_path}")
                        self.total_tests += 1
                        continue
                except Exception as e:
                    print(f"  ❌ {file_path} - Read error: {e}")
                    self.issues_found.append(f"Read error: {file_path}")
            else:
                print(f"  ❌ {file_path} - Missing")
                self.issues_found.append(f"Missing file: {file_path}")

            self.total_tests += 1

    def test_database_structure(self):
        """בדיקת מבנה מסד הנתונים"""
        print("\n🗄️  Testing Database Structure...")

        db_file = (
            self.app_path
            / "app/src/main/java/com/smartagent/technician/data/database/Database.kt"
        )
        if not db_file.exists():
            print("  ❌ Database.kt not found")
            self.issues_found.append("Missing Database.kt")
            self.total_tests += 1
            return

        try:
            content = db_file.read_text(encoding="utf-8")

            # בדיקת Entities
            required_entities = [
                "CallEntity",
                "CustomerEntity",
                "AppointmentEntity",
                "CompletedJobEntity",
            ]

            for entity in required_entities:
                if f"data class {entity}" in content:
                    print(f"  ✅ Entity: {entity}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing entity: {entity}")
                    self.issues_found.append(f"Missing entity: {entity}")
                self.total_tests += 1

            # בדיקת DAOs
            required_daos = [
                "CallDao",
                "CustomerDao",
                "AppointmentDao",
                "CompletedJobDao",
            ]

            for dao in required_daos:
                if f"interface {dao}" in content:
                    print(f"  ✅ DAO: {dao}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing DAO: {dao}")
                    self.issues_found.append(f"Missing DAO: {dao}")
                self.total_tests += 1

        except Exception as e:
            print(f"  ❌ Error reading Database.kt: {e}")
            self.issues_found.append(f"Error reading Database.kt: {e}")
            self.total_tests += 1

    def test_ui_components(self):
        """בדיקת רכיבי UI"""
        print("\n🎨 Testing UI Components...")

        ui_files = [
            (
                "app/src/main/java/com/smartagent/technician/ui/main/MainScreen.kt",
                ["MainScreen", "@Composable"],
            ),
            (
                "app/src/main/java/com/smartagent/technician/ui/record/RecordCallScreen.kt",
                ["RecordCallScreen", "RecordingButton"],
            ),
        ]

        for file_path, required_components in ui_files:
            full_path = self.app_path / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding="utf-8")

                    for component in required_components:
                        if component in content:
                            print(f"  ✅ {file_path} - {component}")
                            self.passed_tests += 1
                        else:
                            print(f"  ❌ {file_path} - Missing {component}")
                            self.issues_found.append(
                                f"Missing component {component} in {file_path}"
                            )
                        self.total_tests += 1

                except Exception as e:
                    print(f"  ❌ Error reading {file_path}: {e}")
                    self.issues_found.append(f"Error reading {file_path}: {e}")
                    self.total_tests += 1
            else:
                print(f"  ❌ {file_path} - Missing")
                self.issues_found.append(f"Missing UI file: {file_path}")
                self.total_tests += len(required_components)

    def test_resources(self):
        """בדיקת משאבים"""
        print("\n📦 Testing Resources...")

        resource_files = ["app/src/main/res/values/strings.xml"]

        for file_path in resource_files:
            full_path = self.app_path / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding="utf-8")
                    if len(content) > 100 and "app_name" in content:
                        print(f"  ✅ {file_path}")
                        self.passed_tests += 1
                    else:
                        print(f"  ⚠️  {file_path} - Content incomplete")
                        self.issues_found.append(f"Incomplete content: {file_path}")
                except Exception as e:
                    print(f"  ❌ Error reading {file_path}: {e}")
                    self.issues_found.append(f"Error reading {file_path}: {e}")
            else:
                print(f"  ❌ {file_path} - Missing")
                self.issues_found.append(f"Missing resource: {file_path}")

            self.total_tests += 1

    def test_strings_localization(self):
        """בדיקת לוקליזציה בעברית"""
        print("\n🌐 Testing Hebrew Localization...")

        strings_file = self.app_path / "app/src/main/res/values/strings.xml"
        if not strings_file.exists():
            print("  ❌ strings.xml not found")
            self.issues_found.append("Missing strings.xml")
            self.total_tests += 1
            return

        try:
            content = strings_file.read_text(encoding="utf-8")

            # בדיקת מחרוזות בעברית
            hebrew_strings = [
                "SmartAgent טכנאי",
                "הקלטת שיחה",
                "תורים",
                "לקוחות",
                "שיחות",
            ]

            for hebrew_str in hebrew_strings:
                if hebrew_str in content:
                    print(f"  ✅ Hebrew string: {hebrew_str}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Missing Hebrew string: {hebrew_str}")
                    self.issues_found.append(f"Missing Hebrew string: {hebrew_str}")
                self.total_tests += 1

        except Exception as e:
            print(f"  ❌ Error reading strings.xml: {e}")
            self.issues_found.append(f"Error reading strings.xml: {e}")
            self.total_tests += 1

    def generate_report(self):
        """יצירת דוח בדיקה"""
        print("\n" + "=" * 60)
        print("📊 ANDROID APP VALIDATION REPORT")
        print("=" * 60)

        success_rate = (
            (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        )

        print(f"\n🎯 SUMMARY:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")

        if success_rate >= 90:
            print("\n🎉 EXCELLENT! App structure is complete and ready!")
        elif success_rate >= 75:
            print("\n✅ GOOD! App structure is mostly complete with minor issues.")
        elif success_rate >= 50:
            print("\n⚠️  NEEDS WORK! App structure has several issues.")
        else:
            print("\n❌ CRITICAL! App structure has major issues.")

        if self.issues_found:
            print(f"\n🔍 ISSUES FOUND ({len(self.issues_found)}):")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"   {i}. {issue}")

        # יצירת דוח JSON
        report_data = {
            "timestamp": "2025-09-01",
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "success_rate": success_rate,
            "issues": self.issues_found,
        }

        try:
            report_file = self.app_path / "validation_report.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Detailed report saved: {report_file}")
        except Exception as e:
            print(f"\n❌ Could not save report: {e}")

        return success_rate >= 75


def main():
    """הרצת הבדיקה הראשית"""
    app_path = (
        r"c:\Users\hnaki\OneDrive - Intel Corporation\Desktop\Smart Agent\android_app"
    )

    validator = AndroidAppValidator(app_path)
    success = validator.run_all_tests()

    print("\n" + "=" * 60)
    if success:
        print("🚀 Android app is ready for testing!")
        print("\nNext steps:")
        print("1. Open in Android Studio")
        print("2. Sync Gradle dependencies")
        print("3. Run on emulator or device")
        print("4. Test core functionality")
    else:
        print("🔧 Please fix the issues found before testing.")
        print("\nRecommended actions:")
        print("1. Review the issues list above")
        print("2. Fix missing files and configurations")
        print("3. Re-run this validation")

    return success


if __name__ == "__main__":
    main()
