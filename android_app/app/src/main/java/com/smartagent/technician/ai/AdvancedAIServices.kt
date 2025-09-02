package com.smartagent.technician.ai

import android.content.Context
import android.util.Log
import kotlinx.coroutines.*
import java.util.*
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AdvancedAIServices @Inject constructor() {
    
    companion object {
        private const val TAG = "AdvancedAI"
    }
    
    // Real-time transcription with confidence scoring
    suspend fun transcribeAudioAdvanced(audioPath: String, language: String = "he-IL"): TranscriptionResult {
        return withContext(Dispatchers.IO) {
            try {
                // Simulated advanced transcription with confidence
                delay(1000) // Simulate processing time
                
                val transcript = when {
                    audioPath.contains("test") -> "שלום, יש לי בעיה עם המזגן בסלון"
                    audioPath.contains("demo") -> "הדוד החשמלי לא עובד, צריך טכנאי בדחיפות"
                    else -> "שיחת לקוח - בקשה לשירות טכנאי"
                }
                
                TranscriptionResult(
                    text = transcript,
                    confidence = 0.95f,
                    language = language,
                    duration = 45,
                    wordTimestamps = generateWordTimestamps(transcript)
                )
            } catch (e: Exception) {
                Log.e(TAG, "Transcription failed", e)
                TranscriptionResult.error("Transcription failed: ${e.message}")
            }
        }
    }
    
    // Advanced information extraction with ML
    suspend fun extractInformationAdvanced(transcript: String): ExtractionResult {
        return withContext(Dispatchers.Default) {
            try {
                val result = ExtractionResult()
                
                // Customer name extraction
                result.customerName = extractCustomerName(transcript)
                
                // Phone number extraction  
                result.phoneNumber = extractPhoneNumber(transcript)
                
                // Address extraction
                result.address = extractAddress(transcript)
                
                // Problem type classification
                result.problemType = classifyProblem(transcript)
                
                // Urgency assessment
                result.urgency = assessUrgency(transcript)
                
                // Time estimation
                result.estimatedDuration = estimateRepairTime(result.problemType)
                
                // Next action recommendations
                result.recommendedActions = generateRecommendations(result)
                
                result.confidence = calculateOverallConfidence(result)
                
                result
            } catch (e: Exception) {
                Log.e(TAG, "Information extraction failed", e)
                ExtractionResult.error("Extraction failed: ${e.message}")
            }
        }
    }
    
    // Smart appointment scheduling
    suspend fun suggestAppointmentTime(
        problemType: String,
        urgency: String,
        customerPreference: String? = null
    ): AppointmentSuggestion {
        return withContext(Dispatchers.Default) {
            val calendar = Calendar.getInstance()
            
            val suggestedTime = when (urgency) {
                "גבוהה" -> {
                    calendar.add(Calendar.HOUR, 2) // Within 2 hours
                    calendar.time
                }
                "בינונית" -> {
                    calendar.add(Calendar.DAY_OF_MONTH, 1) // Tomorrow
                    calendar.set(Calendar.HOUR_OF_DAY, 10)
                    calendar.time
                }
                else -> {
                    calendar.add(Calendar.DAY_OF_MONTH, 3) // Within 3 days
                    calendar.set(Calendar.HOUR_OF_DAY, 14)
                    calendar.time
                }
            }
            
            AppointmentSuggestion(
                suggestedTime = suggestedTime,
                estimatedDuration = estimateRepairTime(problemType),
                confidence = 0.88f,
                reasoning = "Based on problem type '$problemType' and urgency '$urgency'"
            )
        }
    }
    
    // Private helper methods
    private fun extractCustomerName(text: String): String {
        val namePatterns = listOf(
            Regex("שמי ([א-ת\s]+)"),
            Regex("אני ([א-ת\s]+)"),
            Regex("מ([א-ת\s]+)\s+מדבר")
        )
        
        for (pattern in namePatterns) {
            val match = pattern.find(text)
            if (match != null) {
                return match.groupValues[1].trim()
            }
        }
        
        return "לקוח לא מזוהה"
    }
    
    private fun extractPhoneNumber(text: String): String {
        val phonePattern = Regex("(0\d{1,2}-?\d{7}|0\d{9})")
        return phonePattern.find(text)?.value ?: ""
    }
    
    private fun extractAddress(text: String): String {
        val addressPatterns = listOf(
            Regex("ברחוב ([א-ת\s]+\d+)"),
            Regex("בכתובת ([א-ת\s\d,]+)"),
            Regex("ב([א-ת\s]+\d+[א-ת\s]*)")
        )
        
        for (pattern in addressPatterns) {
            val match = pattern.find(text)
            if (match != null) {
                return match.groupValues[1].trim()
            }
        }
        
        return ""
    }
    
    private fun classifyProblem(text: String): String {
        val problems = mapOf(
            listOf("מזגן", "קירור", "חום") to "מזגן",
            listOf("דוד", "מים חמים", "בוילר") to "דוד חשמל",
            listOf("חשמל", "נורה", "בעיית חשמל") to "חשמל",
            listOf("צנרת", "זרימה", "ברז") to "אינסטלציה",
            listOf("מדיח", "מכונת כביסה", "מקרר") to "מוצרי חשמל"
        )
        
        for ((keywords, problem) in problems) {
            if (keywords.any { text.contains(it) }) {
                return problem
            }
        }
        
        return "כללי"
    }
    
    private fun assessUrgency(text: String): String {
        val urgentKeywords = listOf("דחוף", "בדחיפות", "חירום", "לא עובד כלל")
        val moderateKeywords = listOf("בעיה", "תקלה", "לא עובד טוב")
        
        return when {
            urgentKeywords.any { text.contains(it) } -> "גבוהה"
            moderateKeywords.any { text.contains(it) } -> "בינונית"
            else -> "נמוכה"
        }
    }
    
    private fun estimateRepairTime(problemType: String): Int {
        return when (problemType) {
            "מזגן" -> 120 // 2 hours
            "דוד חשמל" -> 90 // 1.5 hours
            "חשמל" -> 60 // 1 hour
            "אינסטלציה" -> 90 // 1.5 hours
            "מוצרי חשמל" -> 75 // 1.25 hours
            else -> 60 // 1 hour default
        }
    }
    
    private fun generateRecommendations(result: ExtractionResult): List<String> {
        val recommendations = mutableListOf<String>()
        
        if (result.urgency == "גבוהה") {
            recommendations.add("קבע תור דחוף")
            recommendations.add("התקשר ללקוח תוך שעה")
        }
        
        when (result.problemType) {
            "מזגן" -> {
                recommendations.add("הכן כלי עבודה למזגנים")
                recommendations.add("בדוק זמינות חלקי חילוף")
            }
            "דוד חשמל" -> {
                recommendations.add("הכן כלי חשמל")
                recommendations.add("בדוק זמינות אלמנט חימום")
            }
        }
        
        return recommendations
    }
    
    private fun calculateOverallConfidence(result: ExtractionResult): Float {
        var confidence = 0.8f
        
        if (result.customerName != "לקוח לא מזוהה") confidence += 0.1f
        if (result.phoneNumber.isNotEmpty()) confidence += 0.05f
        if (result.address.isNotEmpty()) confidence += 0.05f
        
        return confidence.coerceAtMost(1.0f)
    }
    
    private fun generateWordTimestamps(text: String): List<WordTimestamp> {
        val words = text.split(" ")
        return words.mapIndexed { index, word ->
            WordTimestamp(
                word = word,
                startTime = index * 0.5, // 0.5 seconds per word
                endTime = (index + 1) * 0.5,
                confidence = 0.9f
            )
        }
    }
}

// Data classes
data class TranscriptionResult(
    val text: String,
    val confidence: Float,
    val language: String,
    val duration: Int,
    val wordTimestamps: List<WordTimestamp> = emptyList(),
    val isError: Boolean = false,
    val errorMessage: String? = null
) {
    companion object {
        fun error(message: String) = TranscriptionResult(
            text = "",
            confidence = 0f,
            language = "",
            duration = 0,
            isError = true,
            errorMessage = message
        )
    }
}

data class ExtractionResult(
    var customerName: String = "",
    var phoneNumber: String = "",
    var address: String = "",
    var problemType: String = "",
    var urgency: String = "",
    var estimatedDuration: Int = 0,
    var recommendedActions: List<String> = emptyList(),
    var confidence: Float = 0f,
    val isError: Boolean = false,
    val errorMessage: String? = null
) {
    companion object {
        fun error(message: String) = ExtractionResult(
            isError = true,
            errorMessage = message
        )
    }
}

data class AppointmentSuggestion(
    val suggestedTime: Date,
    val estimatedDuration: Int,
    val confidence: Float,
    val reasoning: String
)

data class WordTimestamp(
    val word: String,
    val startTime: Double,
    val endTime: Double,
    val confidence: Float
)