package com.smartagent.technician.assistant

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import kotlinx.coroutines.*
import java.util.*
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class VoiceAssistant @Inject constructor(
    private val context: Context
) : TextToSpeech.OnInitListener {
    
    private var tts: TextToSpeech? = null
    private var isInitialized = false
    
    companion object {
        private const val TAG = "VoiceAssistant"
    }
    
    init {
        tts = TextToSpeech(context, this)
    }
    
    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = tts?.setLanguage(Locale("he", "IL"))
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                // Fallback to English
                tts?.setLanguage(Locale.US)
            }
            isInitialized = true
            Log.d(TAG, "Voice Assistant initialized")
        }
    }
    
    fun speak(text: String, priority: Int = TextToSpeech.QUEUE_FLUSH) {
        if (isInitialized) {
            tts?.speak(text, priority, null, null)
        }
    }
    
    // Smart voice commands
    suspend fun processVoiceCommand(command: String): VoiceResponse {
        return withContext(Dispatchers.Default) {
            when {
                command.contains("התחל הקלטה") || command.contains("record") -> {
                    VoiceResponse.action("start_recording", "מתחיל הקלטה...")
                }
                command.contains("עצור הקלטה") || command.contains("stop") -> {
                    VoiceResponse.action("stop_recording", "עוצר הקלטה...")
                }
                command.contains("הצג לקוחות") || command.contains("customers") -> {
                    VoiceResponse.navigation("customers", "מציג רשימת לקוחות")
                }
                command.contains("הצג תורים") || command.contains("appointments") -> {
                    VoiceResponse.navigation("appointments", "מציג תורים")
                }
                command.contains("סטטיסטיקות") || command.contains("stats") -> {
                    VoiceResponse.navigation("statistics", "מציג סטטיסטיקות")
                }
                command.contains("תור חדש") || command.contains("new appointment") -> {
                    VoiceResponse.action("new_appointment", "יוצר תור חדש...")
                }
                command.contains("חפש") || command.contains("search") -> {
                    val searchTerm = extractSearchTerm(command)
                    VoiceResponse.search(searchTerm, "מחפש: $searchTerm")
                }
                command.contains("התקשר") || command.contains("call") -> {
                    val phoneNumber = extractPhoneNumber(command)
                    VoiceResponse.call(phoneNumber, "מתקשר ל: $phoneNumber")
                }
                command.contains("עזרה") || command.contains("help") -> {
                    VoiceResponse.help(getHelpText())
                }
                else -> {
                    VoiceResponse.unknown("לא הבנתי את הפקודה. נסה שוב או אמור 'עזרה'")
                }
            }
        }
    }
    
    // Voice guidance for technicians
    fun provideGuidance(problemType: String, step: Int): String {
        return when (problemType) {
            "מזגן" -> getAirConditioningGuidance(step)
            "דוד חשמל" -> getWaterHeaterGuidance(step)
            "חשמל" -> getElectricalGuidance(step)
            "אינסטלציה" -> getPlumbingGuidance(step)
            else -> "בצע בדיקה כללית של המערכת"
        }
    }
    
    // Safety alerts
    fun provideSafetyAlert(riskLevel: String): String {
        return when (riskLevel) {
            "high" -> "⚠️ זהירות! סכנה גבוהה - נתק חשמל לפני העבודה"
            "medium" -> "⚠️ שים לב - ודא בטיחות לפני המשך"
            "low" -> "בצע בדיקת בטיחות בסיסית"
            else -> "עבוד בזהירות"
        }
    }
    
    private fun extractSearchTerm(command: String): String {
        val searchPattern = Regex("חפש (.+)")
        return searchPattern.find(command)?.groupValues?.get(1) ?: ""
    }
    
    private fun extractPhoneNumber(command: String): String {
        val phonePattern = Regex("(0\d{1,2}-?\d{7}|0\d{9})")
        return phonePattern.find(command)?.value ?: ""
    }
    
    private fun getAirConditioningGuidance(step: Int): String {
        return when (step) {
            1 -> "שלב 1: בדוק מתח חשמלי ונתיכים"
            2 -> "שלב 2: בדוק פילטר אוויר וחיישני טמפרטורה"
            3 -> "שלב 3: בדוק רמת גז ודליפות"
            4 -> "שלב 4: בדוק מדחס ומאוורר"
            else -> "בדיקה הושלמה בהצלחה"
        }
    }
    
    private fun getWaterHeaterGuidance(step: Int): String {
        return when (step) {
            1 -> "שלב 1: נתק חשמל ובדוק מתח"
            2 -> "שלב 2: בדוק אלמנט חימום"
            3 -> "שלב 3: בדוק תרמוסטט ובקרת טמפרטורה"
            4 -> "שלב 4: בדוק בידוד ואטמים"
            else -> "בדיקה הושלמה בהצלחה"
        }
    }
    
    private fun getElectricalGuidance(step: Int): String {
        return when (step) {
            1 -> "שלב 1: בדוק לוח חשמל ונתיכים"
            2 -> "שלב 2: בדוק חיבורים ובידוד"
            3 -> "שלב 3: בדוק הארקה ופח"ד"
            4 -> "שלב 4: בדוק עומסים ותקנות"
            else -> "בדיקה הושלמה בהצלחה"
        }
    }
    
    private fun getPlumbingGuidance(step: Int): String {
        return when (step) {
            1 -> "שלב 1: בדוק דליפות ולחץ מים"
            2 -> "שלב 2: בדוק צינורות וחיבורים"
            3 -> "שלב 3: בדוק ברזים ושסתומים"
            4 -> "שלב 4: בדוק ניקוז וסתימות"
            else -> "בדיקה הושלמה בהצלחה"
        }
    }
    
    private fun getHelpText(): String {
        return """
            פקודות זמינות:
            • התחל הקלטה - להתחלת הקלטת שיחה
            • עצור הקלטה - לעצירת הקלטה
            • הצג לקוחות - לצפייה ברשימת לקוחות
            • הצג תורים - לצפייה בתורים
            • תור חדש - ליצירת תור חדש
            • חפש [מילה] - לחיפוש
            • התקשר [מספר] - להתקשרות
        """.trimIndent()
    }
    
    fun destroy() {
        tts?.stop()
        tts?.shutdown()
    }
}

data class VoiceResponse(
    val type: String,
    val action: String?,
    val message: String,
    val data: Any? = null
) {
    companion object {
        fun action(action: String, message: String) = VoiceResponse("action", action, message)
        fun navigation(screen: String, message: String) = VoiceResponse("navigation", screen, message)
        fun search(term: String, message: String) = VoiceResponse("search", "search", message, term)
        fun call(number: String, message: String) = VoiceResponse("call", "call", message, number)
        fun help(helpText: String) = VoiceResponse("help", null, helpText)
        fun unknown(message: String) = VoiceResponse("unknown", null, message)
    }
}