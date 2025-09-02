package com.smartagent.technician.data.database

import androidx.room.*
import kotlinx.coroutines.flow.Flow

// Entity - שיחה
@Entity(tableName = "calls")
data class CallEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val customerName: String,
    val customerPhone: String,
    val audioFilePath: String? = null,
    val transcription: String? = null,
    val deviceCategory: String? = null,
    val issueDescription: String? = null,
    val urgencyLevel: String = "medium",
    val status: String = "pending", // pending, processed, scheduled, completed
    val timestamp: Long = System.currentTimeMillis(),
    val processedAt: Long? = null,
    val confidence: Float? = null
)

// Entity - לקוח
@Entity(tableName = "customers")
data class CustomerEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val name: String,
    val phone: String,
    val email: String? = null,
    val address: String? = null,
    val city: String? = null,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val notes: String? = null,
    val isVip: Boolean = false,
    val preferredTimeSlot: String? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val lastContactAt: Long? = null
)

// Entity - תור
@Entity(
    tableName = "appointments",
    foreignKeys = [
        ForeignKey(
            entity = CallEntity::class,
            parentColumns = ["id"],
            childColumns = ["callId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = CustomerEntity::class,
            parentColumns = ["id"],
            childColumns = ["customerId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class AppointmentEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val callId: Long?,
    val customerId: Long,
    val scheduledDate: String, // YYYY-MM-DD
    val scheduledTime: String, // HH:MM
    val estimatedDuration: Int = 60, // minutes
    val serviceType: String,
    val description: String,
    val status: String = "scheduled", // scheduled, in_progress, completed, cancelled
    val location: String,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val notes: String? = null,
    val estimatedCost: Double? = null,
    val actualCost: Double? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val completedAt: Long? = null
)

// Entity - עבודה שהושלמה
@Entity(
    tableName = "completed_jobs",
    foreignKeys = [
        ForeignKey(
            entity = AppointmentEntity::class,
            parentColumns = ["id"],
            childColumns = ["appointmentId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class CompletedJobEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val appointmentId: Long,
    val workDescription: String,
    val partsUsed: String? = null,
    val timeSpent: Int, // minutes
    val finalCost: Double,
    val customerRating: Int? = null, // 1-5 stars
    val customerFeedback: String? = null,
    val photos: String? = null, // JSON array of photo paths
    val technicianNotes: String? = null,
    val completedAt: Long = System.currentTimeMillis()
)

// DAO - גישה לנתונים
@Dao
interface CallDao {
    @Query("SELECT * FROM calls ORDER BY timestamp DESC")
    fun getAllCalls(): Flow<List<CallEntity>>

    @Query("SELECT * FROM calls WHERE status = :status ORDER BY timestamp DESC")
    fun getCallsByStatus(status: String): Flow<List<CallEntity>>

    @Query("SELECT * FROM calls WHERE id = :id")
    suspend fun getCallById(id: Long): CallEntity?

    @Insert
    suspend fun insertCall(call: CallEntity): Long

    @Update
    suspend fun updateCall(call: CallEntity)

    @Delete
    suspend fun deleteCall(call: CallEntity)
}

@Dao
interface CustomerDao {
    @Query("SELECT * FROM customers ORDER BY name ASC")
    fun getAllCustomers(): Flow<List<CustomerEntity>>

    @Query("SELECT * FROM customers WHERE phone = :phone LIMIT 1")
    suspend fun getCustomerByPhone(phone: String): CustomerEntity?

    @Query("SELECT * FROM customers WHERE id = :id")
    suspend fun getCustomerById(id: Long): CustomerEntity?

    @Insert
    suspend fun insertCustomer(customer: CustomerEntity): Long

    @Update
    suspend fun updateCustomer(customer: CustomerEntity)

    @Query("UPDATE customers SET lastContactAt = :timestamp WHERE id = :id")
    suspend fun updateLastContact(id: Long, timestamp: Long)
}

@Dao
interface AppointmentDao {
    @Query("SELECT * FROM appointments ORDER BY scheduledDate ASC, scheduledTime ASC")
    fun getAllAppointments(): Flow<List<AppointmentEntity>>

    @Query("SELECT * FROM appointments WHERE status = :status ORDER BY scheduledDate ASC")
    fun getAppointmentsByStatus(status: String): Flow<List<AppointmentEntity>>

    @Query("SELECT * FROM appointments WHERE scheduledDate = :date ORDER BY scheduledTime ASC")
    fun getAppointmentsByDate(date: String): Flow<List<AppointmentEntity>>

    @Query("SELECT * FROM appointments WHERE id = :id")
    suspend fun getAppointmentById(id: Long): AppointmentEntity?

    @Insert
    suspend fun insertAppointment(appointment: AppointmentEntity): Long

    @Update
    suspend fun updateAppointment(appointment: AppointmentEntity)

    @Delete
    suspend fun deleteAppointment(appointment: AppointmentEntity)
}

@Dao
interface CompletedJobDao {
    @Query("SELECT * FROM completed_jobs ORDER BY completedAt DESC")
    fun getAllCompletedJobs(): Flow<List<CompletedJobEntity>>

    @Query("SELECT * FROM completed_jobs WHERE appointmentId = :appointmentId")
    suspend fun getJobByAppointmentId(appointmentId: Long): CompletedJobEntity?

    @Insert
    suspend fun insertCompletedJob(job: CompletedJobEntity): Long

    @Update
    suspend fun updateCompletedJob(job: CompletedJobEntity)
}

// מסד הנתונים הראשי
@Database(
    entities = [
        CallEntity::class,
        CustomerEntity::class,
        AppointmentEntity::class,
        CompletedJobEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class SmartAgentDatabase : RoomDatabase() {
    abstract fun callDao(): CallDao
    abstract fun customerDao(): CustomerDao
    abstract fun appointmentDao(): AppointmentDao
    abstract fun completedJobDao(): CompletedJobDao
}

// ממירי טיפוסים
class Converters {
    @TypeConverter
    fun fromStringList(value: List<String>): String {
        return value.joinToString(",")
    }

    @TypeConverter
    fun toStringList(value: String): List<String> {
        return if (value.isEmpty()) emptyList() else value.split(",")
    }
}
