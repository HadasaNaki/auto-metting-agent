package com.smartagent.technician

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.smartagent.technician.ui.main.MainScreenSimple
import com.smartagent.technician.ui.record.RecordCallScreenSimple
import com.smartagent.technician.ui.theme.SmartAgentTechnicianTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SmartAgentTechnicianTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colors.background
                ) {
                    val navController = rememberNavController()

                    NavHost(
                        navController = navController,
                        startDestination = "main"
                    ) {
                        composable("main") {
                            MainScreenSimple(navController)
                        }

                        composable("record_call") {
                            RecordCallScreenSimple(navController)
                        }

                        composable("calls") {
                            // TODO: CallsListScreen
                            MainScreenSimple(navController)
                        }

                        composable("appointments") {
                            // TODO: AppointmentsScreen
                            MainScreenSimple(navController)
                        }

                        composable("customers") {
                            // TODO: CustomersScreen
                            MainScreenSimple(navController)
                        }

                        composable("call_details/{callId}") { backStackEntry ->
                            val callId = backStackEntry.arguments?.getString("callId")
                            // TODO: CallDetailsScreen
                            MainScreenSimple(navController)
                        }

                        composable("appointment_details/{appointmentId}") { backStackEntry ->
                            val appointmentId = backStackEntry.arguments?.getString("appointmentId")
                            // TODO: AppointmentDetailsScreen
                            MainScreen(navController)
                        }

                        composable("add_customer") {
                            // TODO: AddCustomerScreen
                            MainScreen(navController)
                        }
                    }
                }
            }
        }
    }
}
