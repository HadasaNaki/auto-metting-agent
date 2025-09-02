# 🛠️ מדריך פיתוח - SmartAgent Android

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
