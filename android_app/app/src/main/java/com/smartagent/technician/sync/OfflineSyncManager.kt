package com.smartagent.technician.sync

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.util.Log
import androidx.work.*
import com.smartagent.technician.data.database.SmartAgentDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class OfflineSyncManager @Inject constructor(
    private val context: Context,
    private val database: SmartAgentDatabase
) {
    
    companion object {
        private const val TAG = "OfflineSync"
        private const val SYNC_WORK_NAME = "smart_agent_sync"
    }
    
    private val workManager = WorkManager.getInstance(context)
    private val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    
    fun startPeriodicSync() {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()
        
        val syncWork = PeriodicWorkRequestBuilder<SyncWorker>(
            15, TimeUnit.MINUTES
        )
            .setConstraints(constraints)
            .setBackoffCriteria(
                BackoffPolicy.LINEAR,
                WorkRequest.MIN_BACKOFF_MILLIS,
                TimeUnit.MILLISECONDS
            )
            .build()
        
        workManager.enqueueUniquePeriodicWork(
            SYNC_WORK_NAME,
            ExistingPeriodicWorkPolicy.KEEP,
            syncWork
        )
        
        Log.d(TAG, "Periodic sync scheduled")
    }
    
    fun forceSyncNow() {
        val syncWork = OneTimeWorkRequestBuilder<SyncWorker>()
            .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
            .build()
        
        workManager.enqueue(syncWork)
        Log.d(TAG, "Force sync triggered")
    }
    
    fun isOnline(): Boolean {
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        
        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
    }
    
    suspend fun syncPendingData(): SyncResult {
        return withContext(Dispatchers.IO) {
            try {
                if (!isOnline()) {
                    return@withContext SyncResult.noConnection()
                }
                
                val pendingCalls = database.callDao().getPendingSync()
                val pendingCustomers = database.customerDao().getPendingSync()
                val pendingAppointments = database.appointmentDao().getPendingSync()
                
                var syncedItems = 0
                var failedItems = 0
                
                // Sync calls
                for (call in pendingCalls) {
                    try {
                        // Simulate API call
                        syncCallToServer(call)
                        database.callDao().markSynced(call.id)
                        syncedItems++
                    } catch (e: Exception) {
                        Log.e(TAG, "Failed to sync call ${call.id}", e)
                        failedItems++
                    }
                }
                
                // Sync customers
                for (customer in pendingCustomers) {
                    try {
                        syncCustomerToServer(customer)
                        database.customerDao().markSynced(customer.id)
                        syncedItems++
                    } catch (e: Exception) {
                        Log.e(TAG, "Failed to sync customer ${customer.id}", e)
                        failedItems++
                    }
                }
                
                // Sync appointments
                for (appointment in pendingAppointments) {
                    try {
                        syncAppointmentToServer(appointment)
                        database.appointmentDao().markSynced(appointment.id)
                        syncedItems++
                    } catch (e: Exception) {
                        Log.e(TAG, "Failed to sync appointment ${appointment.id}", e)
                        failedItems++
                    }
                }
                
                SyncResult.success(syncedItems, failedItems)
            } catch (e: Exception) {
                Log.e(TAG, "Sync failed", e)
                SyncResult.error(e.message ?: "Unknown error")
            }
        }
    }
    
    private suspend fun syncCallToServer(call: Any) {
        // Simulate API call to server
        kotlinx.coroutines.delay(200)
        Log.d(TAG, "Call synced to server")
    }
    
    private suspend fun syncCustomerToServer(customer: Any) {
        // Simulate API call to server
        kotlinx.coroutines.delay(150)
        Log.d(TAG, "Customer synced to server")
    }
    
    private suspend fun syncAppointmentToServer(appointment: Any) {
        // Simulate API call to server
        kotlinx.coroutines.delay(100)
        Log.d(TAG, "Appointment synced to server")
    }
}

class SyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    override suspend fun doWork(): Result {
        return try {
            // Get sync manager through DI
            val syncManager = (applicationContext as SmartAgentApplication)
                .applicationComponent
                .syncManager()
            
            val result = syncManager.syncPendingData()
            
            if (result.isSuccess) {
                Log.d("SyncWorker", "Sync completed: ${result.syncedItems} items")
                Result.success()
            } else {
                Log.w("SyncWorker", "Sync failed: ${result.errorMessage}")
                Result.retry()
            }
        } catch (e: Exception) {
            Log.e("SyncWorker", "Sync worker failed", e)
            Result.failure()
        }
    }
}

data class SyncResult(
    val isSuccess: Boolean,
    val syncedItems: Int = 0,
    val failedItems: Int = 0,
    val errorMessage: String? = null
) {
    companion object {
        fun success(synced: Int, failed: Int) = SyncResult(
            isSuccess = true,
            syncedItems = synced,
            failedItems = failed
        )
        
        fun error(message: String) = SyncResult(
            isSuccess = false,
            errorMessage = message
        )
        
        fun noConnection() = SyncResult(
            isSuccess = false,
            errorMessage = "No internet connection"
        )
    }
}