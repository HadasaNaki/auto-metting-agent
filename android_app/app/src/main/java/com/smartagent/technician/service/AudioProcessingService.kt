package com.smartagent.technician.service

import android.app.Service
import android.content.Intent
import android.media.MediaRecorder
import android.os.IBinder
import android.util.Log
import com.smartagent.technician.data.repository.SmartAgentRepository
import com.smartagent.technician.ai.AudioTranscriptionService
import com.smartagent.technician.ai.InformationExtractionService
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.*
import java.io.File
import javax.inject.Inject

@AndroidEntryPoint
class AudioProcessingService : Service() {

    @Inject
    lateinit var repository: SmartAgentRepository

    @Inject
    lateinit var transcriptionService: AudioTranscriptionService

    @Inject
    lateinit var extractionService: InformationExtractionService

    private val serviceJob = SupervisorJob()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)

    companion object {
        const val ACTION_PROCESS_AUDIO = "process_audio"
        const val EXTRA_AUDIO_FILE_PATH = "audio_file_path"
        const val EXTRA_CALL_ID = "call_id"
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_PROCESS_AUDIO -> {
                val audioFilePath = intent.getStringExtra(EXTRA_AUDIO_FILE_PATH)
                val callId = intent.getLongExtra(EXTRA_CALL_ID, -1)

                if (audioFilePath != null && callId != -1L) {
                    processAudioFile(audioFilePath, callId)
                }
            }
        }
        return START_NOT_STICKY
    }

    private fun processAudioFile(audioFilePath: String, callId: Long) {
        serviceScope.launch {
            try {
                Log.d("AudioProcessing", "Starting audio processing for call $callId")

                // שלב 1: תמלול השמע
                val transcription = transcriptionService.transcribeAudio(audioFilePath)
                Log.d("AudioProcessing", "Transcription completed: $transcription")

                // עדכון הקריאה עם התמלול
                val call = repository.getCallById(callId)
                if (call != null) {
                    repository.updateCall(
                        call.copy(
                            transcription = transcription,
                            status = "transcribed"
                        )
                    )
                }

                // שלב 2: חילוץ מידע מהתמלול
                val extractedInfo = extractionService.extractInformation(transcription)
                Log.d("AudioProcessing", "Information extracted: $extractedInfo")

                // עדכון הקריאה עם המידע המחולץ
                if (call != null) {
                    repository.updateCall(
                        call.copy(
                            deviceCategory = extractedInfo.deviceCategory,
                            issueDescription = extractedInfo.issueDescription,
                            urgencyLevel = extractedInfo.urgencyLevel,
                            confidence = extractedInfo.confidence,
                            status = "processed",
                            processedAt = System.currentTimeMillis()
                        )
                    )
                }

                // שלב 3: יצירת/עדכון לקוח
                handleCustomerCreation(extractedInfo, callId)

                // שלב 4: יצירת תור אוטומטי
                scheduleAppointment(extractedInfo, callId)

                Log.d("AudioProcessing", "Audio processing completed successfully")

            } catch (e: Exception) {
                Log.e("AudioProcessing", "Error processing audio", e)

                // עדכון סטטוס שגיאה
                val call = repository.getCallById(callId)
                if (call != null) {
                    repository.updateCall(
                        call.copy(status = "error")
                    )
                }
            } finally {
                stopSelf(startId)
            }
        }
    }

    private suspend fun handleCustomerCreation(extractedInfo: ExtractionResult, callId: Long) {
        // בדיקה אם הלקוח קיים
        var customer = repository.getCustomerByPhone(extractedInfo.customerPhone)

        if (customer == null) {
            // יצירת לקוח חדש
            val customerId = repository.insertCustomer(
                CustomerEntity(
                    name = extractedInfo.customerName,
                    phone = extractedInfo.customerPhone,
                    address = extractedInfo.customerAddress,
                    city = extractedInfo.customerCity,
                    notes = "נוצר אוטומטית מקריאה $callId"
                )
            )
            customer = repository.getCustomerById(customerId)
        } else {
            // עדכון זמן קשר אחרון
            repository.updateLastContact(customer.id, System.currentTimeMillis())
        }
    }

    private suspend fun scheduleAppointment(extractedInfo: ExtractionResult, callId: Long) {
        val customer = repository.getCustomerByPhone(extractedInfo.customerPhone)

        if (customer != null && extractedInfo.appointmentDate != null && extractedInfo.appointmentTime != null) {
            repository.insertAppointment(
                AppointmentEntity(
                    callId = callId,
                    customerId = customer.id,
                    scheduledDate = extractedInfo.appointmentDate,
                    scheduledTime = extractedInfo.appointmentTime,
                    serviceType = extractedInfo.deviceCategory ?: "שירות כללי",
                    description = extractedInfo.issueDescription ?: "בעיה לא מוגדרת",
                    location = extractedInfo.customerAddress ?: customer.address ?: "",
                    notes = "נוצר אוטומטית מקריאה",
                    estimatedCost = calculateEstimatedCost(extractedInfo)
                )
            )

            Log.d("AudioProcessing", "Appointment scheduled successfully")
        }
    }

    private fun calculateEstimatedCost(extractedInfo: ExtractionResult): Double {
        // לוגיקה פשוטה לחישוב עלות משוערת
        return when (extractedInfo.deviceCategory?.lowercase()) {
            "מקרר" -> 250.0
            "מזגן" -> 300.0
            "מכונת כביסה" -> 200.0
            "מדיח כלים" -> 180.0
            else -> 150.0
        }.let { baseCost ->
            when (extractedInfo.urgencyLevel) {
                "high" -> baseCost * 1.5
                "medium" -> baseCost
                "low" -> baseCost * 0.8
                else -> baseCost
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        serviceJob.cancel()
    }
}

// מחלקת נתונים לתוצאות חילוץ מידע
data class ExtractionResult(
    val customerName: String,
    val customerPhone: String,
    val customerAddress: String? = null,
    val customerCity: String? = null,
    val deviceCategory: String? = null,
    val issueDescription: String? = null,
    val urgencyLevel: String = "medium",
    val appointmentDate: String? = null,
    val appointmentTime: String? = null,
    val confidence: Float = 0.8f
)
