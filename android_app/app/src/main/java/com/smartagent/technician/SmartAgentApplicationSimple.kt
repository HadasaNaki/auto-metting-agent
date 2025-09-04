package com.smartagent.technician

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class SmartAgentApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
