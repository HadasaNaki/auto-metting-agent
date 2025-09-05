package com.smartagent.simple

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val textView = TextView(this)
        textView.text = "🚀 SmartAgent - האפליקציה לטכנאים חכמים"
        textView.textSize = 24f
        
        setContentView(textView)
    }
}
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
