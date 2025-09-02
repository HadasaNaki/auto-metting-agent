# 🔥 פתרון שגיאת Java Version - Java 21 לא נתמך!

## 🎯 הבעיה:
- **Java 21** (major version 65) מותקן במחשב
- **Gradle 8.0** לא תומך ב-Java 21
- צריך Java 17 או Java 11

## 🚀 פתרונות (לפי סדר קלות):

### פתרון 1: שינוי Java ב-Android Studio (הכי מהיר)
1. **File** → **Settings** (Ctrl+Alt+S)
2. **Build, Execution, Deployment** → **Build Tools** → **Gradle**
3. **Gradle JVM**: בחר **"Project SDK"** או **"Embedded JDK"**
4. **לחץ Apply** ו-**OK**

### פתרון 2: עדכון ל-Gradle חדש יותר
נעבור ל-Gradle 8.4 שתומך ב-Java 21

### פתרון 3: שימוש ב-Java 17 Embedded של Android Studio
Android Studio מגיע עם Java 17 מובנה

## 🎯 בואו ננסה הפתרון הכי מהיר:

### שלב 1: שינוי Gradle JVM
1. **ב-Android Studio**: **File** → **Settings**
2. **Build, Execution, Deployment** → **Build Tools** → **Gradle**
3. **Gradle JVM**: בחר אחת מהאפשרויות:
   - **"Embedded JDK"** (מומלץ)
   - **"Project SDK"**
   - או Java 17 אם יש

### שלב 2: עדכון Gradle ל-8.4
אם זה לא עוזר, נעדכן את Gradle

## 💪 זה יפתור את הבעיה מיד!

**הסיבה**: Java 21 חדש מדי עבור Gradle 8.0
**הפתרון**: השתמש ב-Java הנכון או עדכן Gradle

### 📞 נסה שלב 1 ותספר לי מה קורה!
