package com.smartagent.technician;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.LinearLayout;
import android.view.Gravity;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Create layout programmatically (no XML needed)
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        
        TextView title = new TextView(this);
        title.setText("🔧 SmartAgent טכנאי");
        title.setTextSize(24);
        title.setGravity(Gravity.CENTER);
        
        TextView subtitle = new TextView(this);
        subtitle.setText("אפליקציית טכנאי חכם");
        subtitle.setTextSize(16);
        subtitle.setGravity(Gravity.CENTER);
        
        layout.addView(title);
        layout.addView(subtitle);
        setContentView(layout);
    }
}
