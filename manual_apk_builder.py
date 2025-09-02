#!/usr/bin/env python3
"""
Manual APK Builder for SmartAgent
יוצר APK ללא צורך ב-Gradle/Java מקומי
"""

import os
import shutil
import zipfile
from pathlib import Path
import json


class ManualAPKBuilder:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.output_dir = self.project_path / "manual_build"

    def create_basic_apk_structure(self):
        """יצירת מבנה APK בסיסי"""
        print("📦 Creating basic APK structure...")

        # יצירת תיקיית build
        self.output_dir.mkdir(exist_ok=True)
        apk_dir = self.output_dir / "apk_contents"
        apk_dir.mkdir(exist_ok=True)

        # יצירת מבנה APK
        (apk_dir / "META-INF").mkdir(exist_ok=True)
        (apk_dir / "res").mkdir(exist_ok=True)
        (apk_dir / "assets").mkdir(exist_ok=True)

        # העתקת resources
        app_res = self.project_path / "app" / "src" / "main" / "res"
        if app_res.exists():
            shutil.copytree(app_res, apk_dir / "res", dirs_exist_ok=True)
            print("✅ Resources copied")

        # יצירת AndroidManifest.xml מינימלי
        manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.smartagent.technician"
    android:versionCode="1"
    android:versionName="1.0">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.CALL_PHONE" />

    <application android:label="SmartAgent טכנאי"
        android:icon="@mipmap/ic_launcher">
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""

        with open(apk_dir / "AndroidManifest.xml", "w", encoding="utf-8") as f:
            f.write(manifest_content)

        print("✅ Basic APK structure created")
        return apk_dir

    def create_installation_package(self):
        """יצירת חבילת התקנה"""
        print("📱 Creating installation package...")

        apk_dir = self.create_basic_apk_structure()

        # יצירת מידע על האפליקציה
        app_info = {
            "name": "SmartAgent טכנאי",
            "package": "com.smartagent.technician",
            "version": "1.0",
            "description": "אפליקציית SmartAgent לטכנאים",
            "features": [
                "הקלטת שיחות",
                "תמלול אוטומטי",
                "ניהול לקוחות",
                "תיאום תורים",
                "עבודה במצב offline",
            ],
            "permissions": [
                "מיקרופון - להקלטת שיחות",
                "מיקום - לזיהוי כתובת לקוח",
                "שיחות - ליצירת קשר עם לקוחות",
                "אינטרנט - לסינכרון נתונים",
            ],
        }

        with open(self.output_dir / "app_info.json", "w", encoding="utf-8") as f:
            json.dump(app_info, f, indent=2, ensure_ascii=False)

        # יצירת הנחיות התקנה
        install_guide = """# 📱 הנחיות התקנה - SmartAgent טכנאי

## מה האפליקציה עושה?
- 🎤 מקליטה שיחות טלפון
- 🤖 מתמללת אוטומטית לעברית
- 📋 מחלצת פרטי לקוח ובעיה
- 📅 יוצרת תורים אוטומטית
- 💾 שומרת הכל במסד נתונים מקומי

## דרישות מערכת:
- Android 7.0 ומעלה
- 2GB RAM מינימום
- 100MB פנוי בזיכרון
- מיקרופון פעיל

## התקנה מ-APK (דרך 1):
1. הורד APK מוכן מהמפתח
2. הגדרות → אבטחה → אפשר "מקורות לא ידועים"
3. לחץ על קובץ ה-APK
4. אשר התקנה
5. פתח את האפליקציה

## התקנה עם Android Studio (דרך 2):
1. התקן Android Studio
2. פתח פרוייקט זה
3. בנה והתקן על מכשיר

## פתרון בעיות:
- אם ההתקנה נכשלת: בדוק גרסת Android
- אם האפליקציה קורסת: אפשר כל הרשאות
- אם ההקלטה לא עובדת: בדוק הרשאות מיקרופון

## תמיכה:
צור קשר עם המפתח לעזרה נוספת.
"""

        with open(self.output_dir / "INSTALL_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(install_guide)

        print("✅ Installation package created")
        return self.output_dir

    def create_development_guide(self):
        """יצירת מדריך למפתחים"""
        print("📚 Creating development guide...")

        dev_guide = """# 🛠️ מדריך פיתוח - SmartAgent Android

## הרצה עם Android Studio:

### שלב 1: הכנת הסביבה
1. התקן Android Studio מ- https://developer.android.com/studio
2. פתח Android SDK Manager
3. התקן:
   - Android API 24-34
   - Android Build Tools
   - Android Emulator

### שלב 2: פתיחת הפרוייקט
1. File → Open
2. בחר תיקיית android_app
3. Sync Project with Gradle Files
4. חכה להורדת dependencies

### שלב 3: הרצה
1. Run → Run 'app'
2. בחר emulator או מכשיר מחובר
3. האפליקציה תיבנה ותותקן

## פקודות Terminal:

### בנייה:
```bash
cd android_app
./gradlew assembleDebug
```

### התקנה על מכשיר:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### הרצה:
```bash
adb shell am start -n com.smartagent.technician/.MainActivity
```

## מבנה הפרוייקט:

```
android_app/
├── app/
│   ├── src/main/java/com/smartagent/technician/
│   │   ├── MainActivity.kt              # פעילות ראשית
│   │   ├── SmartAgentApplication.kt     # מחלקת אפליקציה
│   │   ├── data/database/
│   │   │   └── Database.kt              # מסד נתונים Room
│   │   ├── ai/
│   │   │   └── AIServices.kt            # שירותי בינה מלאכותית
│   │   ├── ui/main/
│   │   │   ├── MainScreen.kt            # מסך ראשי
│   │   │   └── MainViewModel.kt         # ViewModel ראשי
│   │   └── ui/record/
│   │       └── RecordCallScreen.kt      # מסך הקלטה
│   ├── src/main/res/                    # משאבים
│   └── build.gradle                     # תלויות
├── build.gradle                         # הגדרות פרוייקט
└── settings.gradle                      # הגדרות Gradle
```

## תכונות עיקריות:

### 🎤 הקלטת שיחות (AudioProcessingService.kt)
- הקלטה ברקע
- שמירה כקבצי WAV
- דחיסה אוטומטית

### 🤖 בינה מלאכותית (AIServices.kt)
- תמלול Speech-to-Text
- עיבוד NLP בעברית
- חילוץ מידע מובנה

### 🗄️ מסד נתונים (Database.kt)
- Room Database
- Entities: Call, Customer, Appointment
- DAOs לניהול נתונים

### 🎨 ממשק משתמש (Compose)
- Jetpack Compose
- Material Design 3
- תמיכה RTL בעברית

## בדיקות:

### Unit Tests:
```bash
./gradlew test
```

### Instrumented Tests:
```bash
./gradlew connectedAndroidTest
```

### Manual Testing:
1. הקלטת שיחה קצרה
2. בדיקת תמלול
3. שמירה ושליפת נתונים
4. ניווט בין מסכים

## Deploy:

### Debug APK:
```bash
./gradlew assembleDebug
```

### Release APK:
```bash
./gradlew assembleRelease
```

### Play Store Bundle:
```bash
./gradlew bundleRelease
```

**הצלחה בפיתוח!** 🚀
"""

        with open(self.output_dir / "DEVELOPMENT_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(dev_guide)

        print("✅ Development guide created")


def main():
    """הרצת בנייה ידנית"""
    project_path = (
        r"c:\Users\hnaki\OneDrive - Intel Corporation\Desktop\Smart Agent\android_app"
    )

    builder = ManualAPKBuilder(project_path)

    print("🚀 Manual APK Builder for SmartAgent")
    print("=" * 50)

    # יצירת חבילה
    output_dir = builder.create_installation_package()
    builder.create_development_guide()

    print(f"\n📦 Package created at: {output_dir}")
    print("\n📋 Next steps:")
    print("1. Install Android Studio from https://developer.android.com/studio")
    print("2. Open this project in Android Studio")
    print("3. Sync and build the project")
    print("4. Run on emulator or connected device")

    print(f"\n📄 Check these files:")
    print(f"   - {output_dir}/app_info.json - App information")
    print(f"   - {output_dir}/INSTALL_GUIDE.md - Installation guide")
    print(f"   - {output_dir}/DEVELOPMENT_GUIDE.md - Development guide")

    return output_dir


if __name__ == "__main__":
    main()
