package com.smartagent.technician

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.smartagent.technician.ui.main.MainScreen
import com.smartagent.technician.ui.record.RecordCallScreen
import com.smartagent.technician.ui.theme.SmartAgentTechnicianTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SmartAgentTechnicianTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()

                    NavHost(
                        navController = navController,
                        startDestination = "main"
                    ) {
                        composable("main") {
                            MainScreen(navController)
                        }

                        composable("record_call") {
                            RecordCallScreen(navController)
                        }

                        composable("calls") {
                            MainScreen(navController)
                        }

                        composable("appointments") {
                            MainScreen(navController)
                        }

                        composable("customers") {
                            MainScreen(navController)
                        }

                        composable("call_details/{callId}") { backStackEntry ->
                            val callId = backStackEntry.arguments?.getString("callId")
                            MainScreen(navController)
                        }

                        composable("appointment_details/{appointmentId}") { backStackEntry ->
                            val appointmentId = backStackEntry.arguments?.getString("appointmentId")
                            MainScreen(navController)
                        }

                        composable("add_customer") {
                            MainScreen(navController)
                        }
                    }
                }
            }
        }
    }
}
