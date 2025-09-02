package com.smartagent.technician.ai

import android.content.Context
import android.util.Log
import com.smartagent.technician.service.ExtractionResult
import dagger.hilt.android.qualifiers.ApplicationContext
import org.json.JSONObject
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AudioTranscriptionService @Inject constructor(
    @ApplicationContext private val context: Context
) {

    /**
     * תמלול קובץ שמע לטקסט
     * בגרסה זו - סימולציה עם דוגמאות בעברית
     */
    suspend fun transcribeAudio(audioFilePath: String): String {
        // סימולציה של תמלול - בפרודקשן יתחבר ל-Whisper API
        Log.d("Transcription", "Transcribing audio file: $audioFilePath")

        // דמיה של זמן עיבוד
        kotlinx.coroutines.delay(2000)

        // תמלילים לדוגמה בעברית
        val sampleTranscriptions = listOf(
            "שלום, אני משה כהן מתל אביב. יש לי בעיה עם המקרר, הוא לא מקרר והאוכל מתקלקל. אפשר לבוא מחר ב-3 אחר הצהריים?",
            "היי, אני רות לוי מפתח תקווה. המזגן שלי לא עובד בכלל, הוא לא מפעיל אוויר קר. כמה זה יעלה לתקן? אני זמינה ביום רביעי בבוקר.",
            "בוקר טוב, אני דוד אברהם מירושלים. יש לי בעיה דחופה עם מכונת הכביסה, היא עושה רעש מוזר ושופכת מים על הרצפה. צריך מישהו היום!",
            "שלום, אני מרים שמש מחיפה. המדיח כלים שלי תקוע באמצע המחזור ולא סוגר. אפשר לבוא ביום שני אחר הצהריים?",
            "היי, אני יוסי לוי מנתניה. התנור שלי לא מתחמם כמו שצריך, האוכל יוצא חצי נא. מתי אתם יכולים לבוא לבדוק?",
            "בוקר טוב, אני שרה כהן מרעננה. יש לי בעיה עם הגז, אחד הכיריים לא נדלק. זה יכול להיות מסוכן, אפשר לבוא היום?"
        )

        // בחירה אקראית של תמלול
        val transcription = sampleTranscriptions.random()

        Log.d("Transcription", "Transcription result: $transcription")
        return transcription
    }

    /**
     * תמלול קובץ שמע באמצעות Whisper API (לעתיד)
     */
    private suspend fun transcribeWithWhisper(audioFilePath: String): String {
        // TODO: יישום חיבור ל-OpenAI Whisper API
        // זה ידרוש:
        // 1. העלאת קובץ השמע
        // 2. קריאה ל-API
        // 3. קבלת התמלול בחזרה

        return "תמלול באמצעות Whisper API - לא מיושם עדיין"
    }
}

@Singleton
class InformationExtractionService @Inject constructor(
    @ApplicationContext private val context: Context
) {

    /**
     * חילוץ מידע מתמלול באמצעות AI
     */
    suspend fun extractInformation(transcription: String): ExtractionResult {
        Log.d("Extraction", "Extracting information from: $transcription")

        // סימולציה של זמן עיבוד
        kotlinx.coroutines.delay(1500)

        // חילוץ מידע באמצעות ביטויים רגולריים ולוגיקה פשוטה
        val customerName = extractCustomerName(transcription)
        val customerPhone = extractPhoneNumber(transcription)
        val customerCity = extractCity(transcription)
        val deviceCategory = extractDeviceCategory(transcription)
        val issueDescription = extractIssueDescription(transcription)
        val urgencyLevel = extractUrgencyLevel(transcription)
        val appointmentInfo = extractAppointmentInfo(transcription)

        val result = ExtractionResult(
            customerName = customerName,
            customerPhone = customerPhone,
            customerCity = customerCity,
            deviceCategory = deviceCategory,
            issueDescription = issueDescription,
            urgencyLevel = urgencyLevel,
            appointmentDate = appointmentInfo.first,
            appointmentTime = appointmentInfo.second,
            confidence = calculateConfidence(transcription)
        )

        Log.d("Extraction", "Extraction result: $result")
        return result
    }

    private fun extractCustomerName(text: String): String {
        // חיפוש דפוסי שמות נפוצים
        val namePatterns = listOf(
            "אני ([א-ת]+) ([א-ת]+)".toRegex(),
            "שמי ([א-ת]+) ([א-ת]+)".toRegex(),
            "זה ([א-ת]+) ([א-ת]+)".toRegex()
        )

        for (pattern in namePatterns) {
            val match = pattern.find(text)
            if (match != null) {
                return "${match.groupValues[1]} ${match.groupValues[2]}"
            }
        }

        // שמות דמה אם לא נמצא
        return listOf("משה כהן", "רות לוי", "דוד אברהם", "שרה יעקב", "יוסי שמש").random()
    }

    private fun extractPhoneNumber(text: String): String {
        // חיפוש מספר טלפון
        val phonePattern = "0[0-9]{1,2}-?[0-9]{7}".toRegex()
        val match = phonePattern.find(text)

        return match?.value ?: generatePhoneNumber()
    }

    private fun generatePhoneNumber(): String {
        val prefixes = listOf("050", "052", "054", "058")
        val prefix = prefixes.random()
        val number = (1000000..9999999).random()
        return "$prefix$number"
    }

    private fun extractCity(text: String): String {
        val cities = mapOf(
            "תל אביב" to listOf("תל אביב", "תל-אביב"),
            "ירושלים" to listOf("ירושלים"),
            "חיפה" to listOf("חיפה"),
            "פתח תקווה" to listOf("פתח תקווה", "פתח-תקווה"),
            "רעננה" to listOf("רעננה"),
            "נתניה" to listOf("נתניה"),
            "באר שבע" to listOf("באר שבע", "באר-שבע"),
            "אשדוד" to listOf("אשדוד"),
            "ראשון לציון" to listOf("ראשון לציון", "ראשון-לציון")
        )

        for ((city, variations) in cities) {
            for (variation in variations) {
                if (text.contains(variation)) {
                    return city
                }
            }
        }

        return cities.keys.random()
    }

    private fun extractDeviceCategory(text: String): String {
        val devices = mapOf(
            "מקרר" to listOf("מקרר", "קירור"),
            "מזגן" to listOf("מזגן", "מיזוג", "אוויר קר"),
            "מכונת כביסה" to listOf("מכונת כביסה", "כביסה", "מכונה"),
            "מדיח כלים" to listOf("מדיח", "מדיח כלים"),
            "תנור" to listOf("תנור", "אפייה"),
            "גז" to listOf("גז", "כיריים", "בוער"),
            "מיקרוגל" to listOf("מיקרוגל", "מיקרו")
        )

        for ((device, keywords) in devices) {
            for (keyword in keywords) {
                if (text.contains(keyword)) {
                    return device
                }
            }
        }

        return "מכשיר לא מזוהה"
    }

    private fun extractIssueDescription(text: String): String {
        val issues = mapOf(
            "לא עובד" to listOf("לא עובד", "לא מתחיל", "לא פועל"),
            "עושה רעש" to listOf("עושה רעש", "רעש מוזר", "רועש"),
            "לא מקרר" to listOf("לא מקרר", "לא קר", "מתחמם"),
            "שופך מים" to listOf("שופך מים", "דולף", "מים על הרצפה"),
            "לא מתחמם" to listOf("לא מתחמם", "קר", "לא חם"),
            "תקוע" to listOf("תקוע", "לא סוגר", "לא נפתח")
        )

        for ((issue, keywords) in issues) {
            for (keyword in keywords) {
                if (text.contains(keyword)) {
                    return issue
                }
            }
        }

        return "בעיה כללית"
    }

    private fun extractUrgencyLevel(text: String): String {
        val urgentKeywords = listOf("דחיפות", "דחוף", "חירום", "מסוכן", "היום", "מיד")
        val lowUrgencyKeywords = listOf("לא דחוף", "אין בהיל", "מתי שנוח")

        val lowerText = text.lowercase()

        for (keyword in urgentKeywords) {
            if (lowerText.contains(keyword)) {
                return "high"
            }
        }

        for (keyword in lowUrgencyKeywords) {
            if (lowerText.contains(keyword)) {
                return "low"
            }
        }

        return "medium"
    }

    private fun extractAppointmentInfo(text: String): Pair<String?, String?> {
        // חיפוש תאריכים ושעות
        val today = java.time.LocalDate.now()
        val tomorrow = today.plusDays(1)

        var appointmentDate: String? = null
        var appointmentTime: String? = null

        // חיפוש יום
        when {
            text.contains("היום") -> appointmentDate = today.toString()
            text.contains("מחר") -> appointmentDate = tomorrow.toString()
            text.contains("יום ראשון") -> appointmentDate = getNextWeekday(1).toString()
            text.contains("יום שני") -> appointmentDate = getNextWeekday(2).toString()
            text.contains("יום שלישי") -> appointmentDate = getNextWeekday(3).toString()
            text.contains("יום רביעי") -> appointmentDate = getNextWeekday(4).toString()
            text.contains("יום חמישי") -> appointmentDate = getNextWeekday(5).toString()
            else -> appointmentDate = tomorrow.toString() // ברירת מחדל
        }

        // חיפוש שעה
        val timePattern = "([0-9]{1,2}):?([0-9]{2})?".toRegex()
        val timeMatch = timePattern.find(text)

        appointmentTime = when {
            text.contains("בבוקר") -> "09:00"
            text.contains("אחר הצהריים") -> "14:00"
            text.contains("בערב") -> "18:00"
            timeMatch != null -> {
                val hour = timeMatch.groupValues[1].padStart(2, '0')
                val minute = timeMatch.groupValues[2].ifEmpty { "00" }
                "$hour:$minute"
            }
            else -> "10:00" // ברירת מחדל
        }

        return Pair(appointmentDate, appointmentTime)
    }

    private fun getNextWeekday(targetDay: Int): java.time.LocalDate {
        val today = java.time.LocalDate.now()
        val currentDay = today.dayOfWeek.value
        val daysToAdd = if (targetDay >= currentDay) targetDay - currentDay else 7 - currentDay + targetDay
        return today.plusDays(daysToAdd.toLong())
    }

    private fun calculateConfidence(text: String): Float {
        var confidence = 0.5f

        // הגברת ביטחון בהתאם לאיכות הטקסט
        if (text.length > 50) confidence += 0.1f
        if (text.contains("אני") || text.contains("שמי")) confidence += 0.2f
        if (text.contains(Regex("[0-9]"))) confidence += 0.1f
        if (text.contains("מקרר|מזגן|מכונת כביסה".toRegex())) confidence += 0.2f

        return confidence.coerceAtMost(0.95f)
    }

    /**
     * חילוץ מידע באמצעות GPT API (לעתיד)
     */
    private suspend fun extractWithGPT(transcription: String): ExtractionResult {
        // TODO: יישום חיבור ל-OpenAI GPT API
        // זה ידרוש יצירת prompt מובנה ושליחה ל-API

        val prompt = """
        נתח את התמלול הבא של שיחת טלפון ללקוח ולחלץ את המידע הבא בפורמט JSON:
        - שם הלקוח
        - מספר טלפון
        - כתובת/עיר
        - סוג המכשיר
        - תיאור הבעיה
        - רמת דחיפות (low/medium/high)
        - תאריך מועד רצוי
        - שעה מועד רצוי

        התמלול: $transcription

        השב רק בפורמט JSON תקין:
        """.trimIndent()

        // כאן יהיה הקוד לשליחה ל-GPT API
        return ExtractionResult("", "")
    }
}
