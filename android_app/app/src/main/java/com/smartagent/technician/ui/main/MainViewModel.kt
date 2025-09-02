package com.smartagent.technician.ui.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.smartagent.technician.data.repository.SmartAgentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor(
    private val repository: SmartAgentRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MainUiState())
    val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    private fun loadData() {
        viewModelScope.launch {
            // טעינת נתונים מהמאגר
            combine(
                repository.getAllCalls(),
                repository.getAllAppointments(),
                repository.getAllCustomers()
            ) { calls, appointments, customers ->

                val today = java.time.LocalDate.now().toString()
                val todayAppointments = appointments.filter { it.scheduledDate == today }
                val recentCalls = calls.take(5)
                val pendingCalls = calls.count { it.status == "pending" }
                val completedJobs = calls.count { it.status == "completed" }

                MainUiState(
                    totalCalls = calls.size,
                    pendingCalls = pendingCalls,
                    todayAppointments = todayAppointments.size,
                    completedJobs = completedJobs,
                    recentCalls = recentCalls.map { call ->
                        com.smartagent.technician.ui.main.CallEntity(
                            id = call.id,
                            customerName = call.customerName,
                            customerPhone = call.customerPhone,
                            deviceCategory = call.deviceCategory,
                            status = call.status,
                            timestamp = call.timestamp
                        )
                    },
                    todayAppointmentsList = todayAppointments.map { appointment ->
                        com.smartagent.technician.ui.main.AppointmentEntity(
                            id = appointment.id,
                            serviceType = appointment.serviceType,
                            scheduledTime = appointment.scheduledTime,
                            location = appointment.location,
                            status = appointment.status,
                            estimatedCost = appointment.estimatedCost
                        )
                    },
                    isLoading = false
                )
            }.collect { newState ->
                _uiState.value = newState
            }
        }
    }

    fun refreshData() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            loadData()
        }
    }
}

data class MainUiState(
    val totalCalls: Int = 0,
    val pendingCalls: Int = 0,
    val todayAppointments: Int = 0,
    val completedJobs: Int = 0,
    val recentCalls: List<com.smartagent.technician.ui.main.CallEntity> = emptyList(),
    val todayAppointmentsList: List<com.smartagent.technician.ui.main.AppointmentEntity> = emptyList(),
    val isLoading: Boolean = true,
    val errorMessage: String? = null
)
