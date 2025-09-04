package com.smartagent.simple

import android.app.Activity
import android.os.Bundle
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Button
import android.view.ViewGroup
import android.graphics.Color

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(50, 100, 50, 50)
            setBackgroundColor(Color.WHITE)
        }
        
        val title = TextView(this).apply {
            text = "🚀 SmartAgent"
            textSize = 32f
            setTextColor(Color.BLACK)
            setPadding(0, 0, 0, 40)
        }
        
        val subtitle = TextView(this).apply {
            text = "האפליקציה לטכנאים חכמים"
            textSize = 18f
            setTextColor(Color.GRAY)
            setPadding(0, 0, 0, 60)
        }
        
        val startButton = Button(this).apply {
            text = "התחל עבודה"
            textSize = 16f
            setPadding(20, 20, 20, 20)
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
            setOnClickListener {
                // כאן יהיה הלוגיק של התחלת עבודה
            }
        }
        
        val settingsButton = Button(this).apply {
            text = "הגדרות"
            textSize = 16f
            setPadding(20, 20, 20, 20)
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
            setOnClickListener {
                // כאן יהיה הלוגיק של הגדרות
            }
        }
        
        layout.addView(title)
        layout.addView(subtitle)
        layout.addView(startButton)
        layout.addView(settingsButton)
        
        setContentView(layout)
    }
}
