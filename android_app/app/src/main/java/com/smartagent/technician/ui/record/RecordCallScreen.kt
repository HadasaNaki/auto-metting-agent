package com.smartagent.technician.ui.record

import android.Manifest
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.isGranted
import com.google.accompanist.permissions.rememberPermissionState
import kotlinx.coroutines.delay

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun RecordCallScreen(
    navController: NavController,
    viewModel: RecordCallViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsState()

    // הרשאות הקלטה
    val recordAudioPermission = rememberPermissionState(Manifest.permission.RECORD_AUDIO)

    LaunchedEffect(Unit) {
        if (!recordAudioPermission.status.isGranted) {
            recordAudioPermission.launchPermissionRequest()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("🎤 הקלטת שיחה") },
                navigationIcon = {
                    IconButton(onClick = { navController.navigateUp() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "חזור")
                    }
                }
            )
        }
    ) { paddingValues ->

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {

            Spacer(modifier = Modifier.height(32.dp))

            // סטטוס הקלטה
            RecordingStatusCard(
                isRecording = uiState.isRecording,
                isProcessing = uiState.isProcessing,
                duration = uiState.recordingDuration,
                customerName = uiState.detectedCustomerName
            )

            Spacer(modifier = Modifier.height(32.dp))

            // כפתור הקלטה
            RecordingButton(
                isRecording = uiState.isRecording,
                isProcessing = uiState.isProcessing,
                onStartRecord = { viewModel.startRecording() },
                onStopRecord = { viewModel.stopRecording() }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // טקסט הדרכה
            Text(
                text = when {
                    uiState.isProcessing -> "מעבד את השיחה באמצעות AI..."
                    uiState.isRecording -> "הקלטה פעילה - לחץ שוב כדי לסיים"
                    else -> "לחץ כדי להתחיל הקלטה"
                },
                style = MaterialTheme.typography.bodyLarge,
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            // תוצאות עיבוד
            if (uiState.transcription.isNotEmpty()) {
                ProcessingResultsCard(
                    transcription = uiState.transcription,
                    extractedInfo = uiState.extractedInfo,
                    onCreateAppointment = { viewModel.createAppointment() },
                    onSaveOnly = { viewModel.saveCallOnly() }
                )
            }

            // הודעות שגיאה
            if (uiState.errorMessage != null) {
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer
                    )
                ) {
                    Text(
                        text = uiState.errorMessage,
                        modifier = Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }
        }
    }
}

@Composable
fun RecordingStatusCard(
    isRecording: Boolean,
    isProcessing: Boolean,
    duration: Long,
    customerName: String?
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = when {
                isProcessing -> MaterialTheme.colorScheme.tertiaryContainer
                isRecording -> MaterialTheme.colorScheme.primaryContainer
                else -> MaterialTheme.colorScheme.surfaceVariant
            }
        )
    ) {
        Column(
            modifier = Modifier.padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // אייקון סטטוס
            Icon(
                imageVector = when {
                    isProcessing -> Icons.Default.Psychology
                    isRecording -> Icons.Default.Mic
                    else -> Icons.Default.MicNone
                },
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = when {
                    isProcessing -> MaterialTheme.colorScheme.onTertiaryContainer
                    isRecording -> MaterialTheme.colorScheme.onPrimaryContainer
                    else -> MaterialTheme.colorScheme.onSurfaceVariant
                }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // כותרת סטטוס
            Text(
                text = when {
                    isProcessing -> "🤖 מעבד באמצעות AI"
                    isRecording -> "🔴 מקליט שיחה"
                    else -> "⏸️ מוכן להקלטה"
                },
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )

            // זמן הקלטה
            if (isRecording || duration > 0) {
                Text(
                    text = formatDuration(duration),
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            // שם לקוח שזוהה
            if (customerName != null) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "לקוח: $customerName",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
fun RecordingButton(
    isRecording: Boolean,
    isProcessing: Boolean,
    onStartRecord: () -> Unit,
    onStopRecord: () -> Unit
) {
    val buttonColor = when {
        isProcessing -> MaterialTheme.colorScheme.tertiary
        isRecording -> MaterialTheme.colorScheme.error
        else -> MaterialTheme.colorScheme.primary
    }

    FloatingActionButton(
        onClick = {
            if (isProcessing) return@FloatingActionButton
            if (isRecording) onStopRecord() else onStartRecord()
        },
        modifier = Modifier.size(80.dp),
        shape = CircleShape,
        containerColor = buttonColor
    ) {
        Icon(
            imageVector = when {
                isProcessing -> Icons.Default.HourglassEmpty
                isRecording -> Icons.Default.Stop
                else -> Icons.Default.Mic
            },
            contentDescription = when {
                isProcessing -> "מעבד"
                isRecording -> "עצור הקלטה"
                else -> "התחל הקלטה"
            },
            modifier = Modifier.size(36.dp),
            tint = Color.White
        )
    }
}

@Composable
fun ProcessingResultsCard(
    transcription: String,
    extractedInfo: ExtractionResult?,
    onCreateAppointment: () -> Unit,
    onSaveOnly: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "🎯 תוצאות עיבוד",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(16.dp))

            // תמלול
            Text(
                text = "תמלול:",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = transcription,
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.padding(vertical = 8.dp)
            )

            if (extractedInfo != null) {
                Divider(modifier = Modifier.padding(vertical = 8.dp))

                // מידע מחולץ
                Text(
                    text = "מידע מחולץ:",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(8.dp))

                InfoRow("👤 לקוח", extractedInfo.customerName)
                InfoRow("📞 טלפון", extractedInfo.customerPhone)
                InfoRow("🔧 מכשיר", extractedInfo.deviceCategory ?: "לא זוהה")
                InfoRow("⚠️ בעיה", extractedInfo.issueDescription ?: "לא צוין")
                InfoRow("🚨 דחיפות", extractedInfo.urgencyLevel)

                if (extractedInfo.appointmentDate != null && extractedInfo.appointmentTime != null) {
                    InfoRow("📅 תור מוצע", "${extractedInfo.appointmentDate} ${extractedInfo.appointmentTime}")
                }

                Spacer(modifier = Modifier.height(16.dp))

                // כפתורי פעולה
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = onCreateAppointment,
                        modifier = Modifier.weight(1f)
                    ) {
                        Text("יצירת תור")
                    }

                    OutlinedButton(
                        onClick = onSaveOnly,
                        modifier = Modifier.weight(1f)
                    ) {
                        Text("שמירה בלבד")
                    }
                }
            }
        }
    }
}

@Composable
fun InfoRow(label: String, value: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 2.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium
        )
    }
}

private fun formatDuration(durationMs: Long): String {
    val seconds = (durationMs / 1000) % 60
    val minutes = (durationMs / (1000 * 60)) % 60
    val hours = (durationMs / (1000 * 60 * 60))

    return if (hours > 0) {
        String.format("%02d:%02d:%02d", hours, minutes, seconds)
    } else {
        String.format("%02d:%02d", minutes, seconds)
    }
}

// Data class for extraction results
data class ExtractionResult(
    val customerName: String,
    val customerPhone: String,
    val customerAddress: String? = null,
    val deviceCategory: String? = null,
    val issueDescription: String? = null,
    val urgencyLevel: String = "medium",
    val appointmentDate: String? = null,
    val appointmentTime: String? = null,
    val confidence: Float = 0.8f
)
