# 🌐 פתרון בעיית רשת - Failed to download plugins.gradle.org

## 🎯 הבעיה:
Android Studio לא יכול להוריד קבצי Gradle בגלל בעיית רשת/firewall

## 🚀 פתרונות (נסה לפי הסדר):

### פתרון 1: שינוי repositories (הכי מהיר)
1. **ב-Android Studio**: **File** → **Settings**
2. **Build, Execution, Deployment** → **Build Tools** → **Gradle**
3. **בחר "Use Gradle from: specified location"**
4. **Gradle home**: הכנס נתיב ל-Gradle אם יש, או השאר ריק
5. **לחץ Apply** ו-**OK**

### פתרון 2: שינוי Gradle Repositories
1. **פתח את הקובץ**: `build.gradle` (Project level)
2. **נוסיף repositories חלופיים**

### פתרון 3: Offline Mode (זמני)
1. **File** → **Settings**
2. **Build, Execution, Deployment** → **Build Tools** → **Gradle**
3. **✅ סמן "Offline work"**
4. **Apply** → **OK**
5. **נסה Sync שוב**

### פתרון 4: נקה Cache
1. **File** → **Invalidate Caches and Restart**
2. **Invalidate and Restart**

### פתרון 5: בדיקת אינטרנט
- וודא שיש חיבור אינטרנט
- נסה לגלוש לאתר אחר
- אם יש firewall תאגידי - זה יכול לחסום

## 🛠️ בואו ננסה הכי פשוט:

### שלב 1: Offline Mode
זה יעבוד עם הקבצים שכבר יש:
1. **File** → **Settings** (Ctrl+Alt+S)
2. **Build, Execution, Deployment** → **Build Tools** → **Gradle**
3. **✅ סמן "Offline work"**
4. **לחץ OK**
5. **נסה Sync שוב**

### שלב 2: אם זה לא עוזר
נעדכן את repositories להשתמש במראות מקומיות

## 📞 ספר לי:
1. **האם יש firewall/proxy** בחברה?
2. **האם אתה יכול לגלוש באופן רגיל?**
3. **נסית Offline Mode?** מה קרה?

## 🎯 המטרה:
**לעקוף את בעיית הרשת ולהגיע ל-Gradle Sync מוצלח!**
