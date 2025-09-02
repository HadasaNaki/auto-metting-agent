package com.smartagent.technician.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material.MaterialTheme
import androidx.compose.material.darkColors
import androidx.compose.material.lightColors
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorPalette = darkColors(
    primary = Color(0xFF2196F3),
    primaryVariant = Color(0xFF1976D2),
    secondary = Color(0xFFFF9800)
)

private val LightColorPalette = lightColors(
    primary = Color(0xFF2196F3),
    primaryVariant = Color(0xFF1976D2),
    secondary = Color(0xFFFF9800)
)

@Composable
fun SmartAgentTechnicianTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (darkTheme) {
        DarkColorPalette
    } else {
        LightColorPalette
    }

    MaterialTheme(
        colors = colors,
        content = content
    )
}
