package com.smartagent.technician.ui.main

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
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    navController: NavController,
    viewModel: MainViewModel = hiltViewModel()
) {
    // כיוון RTL לעברית
    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {

        val uiState by viewModel.uiState.collectAsState()

        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(
                            text = "🔧 SmartAgent טכנאי",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        titleContentColor = Color.White
                    ),
                    actions = {
                        IconButton(onClick = { viewModel.refreshData() }) {
                            Icon(
                                Icons.Default.Refresh,
                                contentDescription = "רענן",
                                tint = Color.White
                            )
                        }
                    }
                )
            },
            bottomBar = {
                NavigationBar {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Home, contentDescription = null) },
                        label = { Text("בית") },
                        selected = true,
                        onClick = { }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Phone, contentDescription = null) },
                        label = { Text("שיחות") },
                        selected = false,
                        onClick = { navController.navigate("calls") }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Event, contentDescription = null) },
                        label = { Text("תורים") },
                        selected = false,
                        onClick = { navController.navigate("appointments") }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.People, contentDescription = null) },
                        label = { Text("לקוחות") },
                        selected = false,
                        onClick = { navController.navigate("customers") }
                    )
                }
            },
            floatingActionButton = {
                FloatingActionButton(
                    onClick = { navController.navigate("record_call") },
                    containerColor = MaterialTheme.colorScheme.secondary
                ) {
                    Icon(
                        Icons.Default.Mic,
                        contentDescription = "הקלט שיחה",
                        tint = Color.White
                    )
                }
            }
        ) { paddingValues ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // כרטיס סטטיסטיקות
                item {
                    StatsCard(
                        totalCalls = uiState.totalCalls,
                        pendingCalls = uiState.pendingCalls,
                        todayAppointments = uiState.todayAppointments,
                        completedJobs = uiState.completedJobs
                    )
                }

                // כרטיס פעולות מהירות
                item {
                    QuickActionsCard(
                        onRecordCall = { navController.navigate("record_call") },
                        onViewCalls = { navController.navigate("calls") },
                        onViewAppointments = { navController.navigate("appointments") },
                        onAddCustomer = { navController.navigate("add_customer") }
                    )
                }

                // רשימת שיחות אחרונות
                item {
                    Text(
                        text = "שיחות אחרונות",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }

                items(uiState.recentCalls) { call ->
                    CallCard(
                        call = call,
                        onClick = { navController.navigate("call_details/${call.id}") }
                    )
                }

                // רשימת תורים להיום
                item {
                    Text(
                        text = "תורים להיום",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }

                items(uiState.todayAppointmentsList) { appointment ->
                    AppointmentCard(
                        appointment = appointment,
                        onClick = { navController.navigate("appointment_details/${appointment.id}") }
                    )
                }
            }
        }
    }
}

@Composable
fun StatsCard(
    totalCalls: Int,
    pendingCalls: Int,
    todayAppointments: Int,
    completedJobs: Int
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "📊 סטטיסטיקות היום",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem("📞", "שיחות", totalCalls)
                StatItem("⏳", "ממתינות", pendingCalls)
                StatItem("📅", "תורים היום", todayAppointments)
                StatItem("✅", "הושלמו", completedJobs)
            }
        }
    }
}

@Composable
fun StatItem(
    icon: String,
    label: String,
    value: Int
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = icon,
            fontSize = 24.sp
        )
        Text(
            text = value.toString(),
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = label,
            fontSize = 12.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun QuickActionsCard(
    onRecordCall: () -> Unit,
    onViewCalls: () -> Unit,
    onViewAppointments: () -> Unit,
    onAddCustomer: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "🚀 פעולות מהירות",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                QuickActionButton(
                    icon = Icons.Default.Mic,
                    text = "הקלט שיחה",
                    onClick = onRecordCall,
                    modifier = Modifier.weight(1f)
                )
                QuickActionButton(
                    icon = Icons.Default.Phone,
                    text = "שיחות",
                    onClick = onViewCalls,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                QuickActionButton(
                    icon = Icons.Default.Event,
                    text = "תורים",
                    onClick = onViewAppointments,
                    modifier = Modifier.weight(1f)
                )
                QuickActionButton(
                    icon = Icons.Default.PersonAdd,
                    text = "לקוח חדש",
                    onClick = onAddCustomer,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
fun QuickActionButton(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Button(
        onClick = onClick,
        modifier = modifier.height(60.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.secondary
        )
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                icon,
                contentDescription = null,
                modifier = Modifier.size(20.dp)
            )
            Text(
                text = text,
                fontSize = 10.sp,
                textAlign = TextAlign.Center
            )
        }
    }
}

@Composable
fun CallCard(
    call: CallEntity,
    onClick: () -> Unit
) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                Icons.Default.Phone,
                contentDescription = null,
                tint = when(call.status) {
                    "completed" -> Color.Green
                    "processing" -> Color.Orange
                    else -> Color.Gray
                },
                modifier = Modifier.size(24.dp)
            )

            Spacer(modifier = Modifier.width(12.dp))

            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = call.customerName,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp
                )
                Text(
                    text = call.deviceCategory ?: "מכשיר לא מזוהה",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 14.sp
                )
                Text(
                    text = formatTimestamp(call.timestamp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 12.sp
                )
            }

            StatusChip(call.status)
        }
    }
}

@Composable
fun AppointmentCard(
    appointment: AppointmentEntity,
    onClick: () -> Unit
) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                Icons.Default.Event,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(24.dp)
            )

            Spacer(modifier = Modifier.width(12.dp))

            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = "${appointment.scheduledTime} - ${appointment.serviceType}",
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp
                )
                Text(
                    text = appointment.location,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 14.sp
                )
                if (appointment.estimatedCost != null) {
                    Text(
                        text = "עלות משוערת: ₪${appointment.estimatedCost.toInt()}",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 12.sp
                    )
                }
            }

            StatusChip(appointment.status)
        }
    }
}

@Composable
fun StatusChip(status: String) {
    val (text, color) = when(status) {
        "pending" -> "ממתין" to Color.Orange
        "processing" -> "מעבד" to Color.Blue
        "completed" -> "הושלם" to Color.Green
        "scheduled" -> "מתוזמן" to Color.Blue
        "in_progress" -> "בביצוע" to Color.Orange
        "cancelled" -> "בוטל" to Color.Red
        else -> status to Color.Gray
    }

    Surface(
        color = color.copy(alpha = 0.2f),
        shape = MaterialTheme.shapes.small,
        modifier = Modifier.padding(4.dp)
    ) {
        Text(
            text = text,
            color = color,
            fontSize = 12.sp,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
        )
    }
}

private fun formatTimestamp(timestamp: Long): String {
    val now = System.currentTimeMillis()
    val diff = now - timestamp

    return when {
        diff < 60000 -> "עכשיו"
        diff < 3600000 -> "${diff / 60000} דקות"
        diff < 86400000 -> "${diff / 3600000} שעות"
        else -> "${diff / 86400000} ימים"
    }
}

// Data classes
data class CallEntity(
    val id: Long,
    val customerName: String,
    val customerPhone: String,
    val deviceCategory: String?,
    val status: String,
    val timestamp: Long
)

data class AppointmentEntity(
    val id: Long,
    val serviceType: String,
    val scheduledTime: String,
    val location: String,
    val status: String,
    val estimatedCost: Double?
)
