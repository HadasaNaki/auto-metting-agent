#!/bin/bash

echo "🔍 Checking SmartAgent Build Status..."
echo "======================================"
echo ""

# בדיקת חיבור אינטרנט
echo "📡 Testing internet connection..."
if ping -c 1 github.com &> /dev/null; then
    echo "✅ Internet connection: OK"
else
    echo "❌ No internet connection"
    exit 1
fi

echo ""
echo "🚀 GitHub Actions Build Status:"
echo "🔗 Direct link: https://github.com/HadasaNaki/auto-metting-agent/actions"
echo ""
echo "📱 When build completes:"
echo "1. Download APK from GitHub Actions artifacts"
echo "2. Follow PHONE_INSTALLATION_FINAL.md guide"
echo "3. Install on your phone and enjoy SmartAgent!"
echo ""
echo "⏱️  Build typically takes 5-10 minutes"
echo "🎯 Watch for the green checkmark ✅"
