package com.smartagent.technician.ui.components

import androidx.compose.animation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EnhancedCallCard(
    call: CallEntity,
    onCallClick: (CallEntity) -> Unit,
    onTranscriptClick: (CallEntity) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        onClick = { onCallClick(call) }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            // Header with customer name and time
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = call.customerName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Start
                )
                
                Text(
                    text = SimpleDateFormat("HH:mm", Locale.getDefault())
                        .format(Date(call.timestamp)),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Problem type chip
            AssistChip(
                onClick = { },
                label = { 
                    Text(
                        text = call.extractedInfo["problem_type"] ?: "כללי",
                        style = MaterialTheme.typography.bodySmall
                    )
                },
                leadingIcon = {
                    Icon(
                        imageVector = when(call.extractedInfo["problem_type"]) {
                            "מזגן" -> Icons.Default.AcUnit
                            "דוד חשמל" -> Icons.Default.WaterDrop
                            "חשמל" -> Icons.Default.ElectricBolt
                            else -> Icons.Default.Build
                        },
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                }
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Transcript preview
            if (call.transcript.isNotEmpty()) {
                Text(
                    text = call.transcript.take(100) + if (call.transcript.length > 100) "..." else "",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Start
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                TextButton(
                    onClick = { onTranscriptClick(call) },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("הצג תמלול מלא")
                    Icon(
                        imageVector = Icons.Default.ArrowForward,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
            
            // Urgency indicator
            call.extractedInfo["urgency"]?.let { urgency ->
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.Default.Warning,
                        contentDescription = null,
                        tint = when(urgency) {
                            "גבוהה" -> Color.Red
                            "בינונית" -> Color.Orange
                            else -> Color.Green
                        },
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "דחיפות: $urgency",
                        style = MaterialTheme.typography.bodySmall,
                        color = when(urgency) {
                            "גבוהה" -> Color.Red
                            "בינונית" -> Color.Orange
                            else -> Color.Green
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun StatisticsCards(
    totalCalls: Int,
    totalCustomers: Int,
    pendingAppointments: Int,
    todayRevenue: Double,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(16.dp)
    ) {
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                StatCard(
                    title = "שיחות היום",
                    value = totalCalls.toString(),
                    icon = Icons.Default.Call,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.weight(1f)
                )
                
                StatCard(
                    title = "לקוחות",
                    value = totalCustomers.toString(),
                    icon = Icons.Default.People,
                    color = MaterialTheme.colorScheme.secondary,
                    modifier = Modifier.weight(1f)
                )
            }
        }
        
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                StatCard(
                    title = "תורים ממתינים",
                    value = pendingAppointments.toString(),
                    icon = Icons.Default.Schedule,
                    color = MaterialTheme.colorScheme.tertiary,
                    modifier = Modifier.weight(1f)
                )
                
                StatCard(
                    title = "הכנסות היום",
                    value = "₪${String.format("%.0f", todayRevenue)}",
                    icon = Icons.Default.AttachMoney,
                    color = Color(0xFF4CAF50),
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
fun StatCard(
    title: String,
    value: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    color: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(
            containerColor = color.copy(alpha = 0.1f)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(32.dp)
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = color,
                textAlign = TextAlign.Center
            )
            
            Text(
                text = title,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
        }
    }
}

@Composable
fun RecordingWaveAnimation(
    isRecording: Boolean,
    modifier: Modifier = Modifier
) {
    val animatedAlpha by animateFloatAsState(
        targetValue = if (isRecording) 1f else 0f,
        animationSpec = tween(300)
    )
    
    Box(
        modifier = modifier.size(200.dp),
        contentAlignment = Alignment.Center
    ) {
        // Animated circles
        repeat(3) { index ->
            val delay = index * 200
            val animatedScale by animateFloatAsState(
                targetValue = if (isRecording) 1.5f else 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(1000, delayMillis = delay),
                    repeatMode = RepeatMode.Reverse
                )
            )
            
            Box(
                modifier = Modifier
                    .size((60 + index * 20).dp)
                    .scale(animatedScale)
                    .alpha(animatedAlpha * (0.6f - index * 0.2f))
                    .background(
                        color = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f),
                        shape = CircleShape
                    )
            )
        }
        
        // Center recording button
        FloatingActionButton(
            onClick = { },
            modifier = Modifier.size(80.dp),
            containerColor = if (isRecording) Color.Red else MaterialTheme.colorScheme.primary
        ) {
            Icon(
                imageVector = if (isRecording) Icons.Default.Stop else Icons.Default.Mic,
                contentDescription = if (isRecording) "עצור הקלטה" else "התחל הקלטה",
                tint = Color.White,
                modifier = Modifier.size(32.dp)
            )
        }
    }
}