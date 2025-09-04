package com.smartagent.simple

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                SmartAgentApp()
            }
        }
    }
}

@Composable
fun SmartAgentApp() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "🚀 SmartAgent",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "האפליקציה לטכנאים חכמים",
            fontSize = 18.sp
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Button(
            onClick = { },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("התחל עבודה")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedButton(
            onClick = { },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("הגדרות")
        }
    }
}
