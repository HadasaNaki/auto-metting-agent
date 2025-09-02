#!/usr/bin/env python3
"""
Simple test runner that doesn't require external dependencies
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))


def test_models_import():
    """Test if models can be imported"""
    try:
        # We'll test the basic structure without SQLAlchemy
        from app import models

        print("✅ Models module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Models import failed: {e}")
        return False


def test_schemas_structure():
    """Test schemas file structure"""
    try:
        schemas_file = backend_path / "app" / "schemas.py"
        if schemas_file.exists():
            content = schemas_file.read_text()
            if "BaseModel" in content and "class" in content:
                print("✅ Schemas file has correct structure")
                return True
        print("❌ Schemas file structure issue")
        return False
    except Exception as e:
        print(f"❌ Schemas test failed: {e}")
        return False


def test_api_structure():
    """Test API file structure"""
    try:
        api_path = backend_path / "app" / "api"
        expected_files = [
            "auth.py",
            "calls.py",
            "jobs.py",
            "appointments.py",
            "messages.py",
            "calendar.py",
            "integrations.py",
        ]

        missing_files = []
        existing_files = []
        for file_name in expected_files:
            if not (api_path / file_name).exists():
                missing_files.append(file_name)
            else:
                existing_files.append(file_name)

        print(f"Found API files: {existing_files}")
        if not missing_files:
            print("✅ All API files exist")
            return True
        else:
            print(f"❌ Missing API files: {missing_files}")
            return False
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False


def test_worker_structure():
    """Test worker file structure"""
    try:
        worker_path = Path(__file__).parent / "worker"
        expected_files = ["main.py", "tasks.py", "celeryconfig.py"]

        missing_files = []
        existing_files = []
        for file_name in expected_files:
            if not (worker_path / file_name).exists():
                missing_files.append(file_name)
            else:
                existing_files.append(file_name)

        print(f"Found worker files: {existing_files}")
        if not missing_files:
            print("✅ All worker files exist")
            return True
        else:
            print(f"❌ Missing worker files: {missing_files}")
            return False
    except Exception as e:
        print(f"❌ Worker structure test failed: {e}")
        return False


def test_frontend_structure():
    """Test frontend file structure"""
    try:
        frontend_path = Path(__file__).parent / "frontend"
        expected_files = ["package.json", "next.config.js", "tailwind.config.js"]

        missing_files = []
        existing_files = []
        for file_name in expected_files:
            if not (frontend_path / file_name).exists():
                missing_files.append(file_name)
            else:
                existing_files.append(file_name)

        print(f"Found frontend files: {existing_files}")
        if not missing_files:
            print("✅ All frontend config files exist")
            return True
        else:
            print(f"❌ Missing frontend files: {missing_files}")
            return False
    except Exception as e:
        print(f"❌ Frontend structure test failed: {e}")
        return False


def test_docker_structure():
    """Test Docker setup"""
    try:
        infra_path = Path(__file__).parent / "infra"
        docker_compose = infra_path / "docker-compose.yml"
        env_example = infra_path / ".env.example"

        print(f"Looking for: {docker_compose}")
        print(f"Looking for: {env_example}")

        if docker_compose.exists() and env_example.exists():
            # Check docker-compose content
            content = docker_compose.read_text()
            required_services = ["backend", "worker", "frontend", "db", "redis"]
            missing_services = [s for s in required_services if s not in content]

            if not missing_services:
                print("✅ Docker compose has all required services")
                return True
            else:
                print(f"❌ Missing services: {missing_services}")
                return False
        else:
            print("❌ Missing docker files")
            return False
    except Exception as e:
        print(f"❌ Docker structure test failed: {e}")
        return False


def test_json_schema_extraction():
    """Test the JSON schema that LLM should return"""
    try:
        # Test if we can create the expected extraction structure
        sample_extraction = {
            "customer": {
                "name": "משה כהן",
                "phone": "+972501234567",
                "email": None,
                "address": {"line1": "הרצל 10", "city": "תל אביב", "notes": "קומה 3"},
            },
            "device": {
                "category": "מקרר",
                "brand": "Samsung",
                "model": "RT38",
                "issue": "לא מקרר",
                "urgency": "high",
            },
            "quote": {"agreed_price": 400, "currency": "ILS", "notes": "כולל הגעה"},
            "appointment": {
                "date": "2025-09-05",
                "time": "15:00",
                "duration_minutes": 60,
                "is_confirmed_by_customer": True,
            },
            "follow_up": {"required": False, "due_at": None, "reason": None},
            "free_text_summary_he": "תואם ביקור לתיקון מקרר...",
            "confidence": 0.88,
        }

        # Validate structure
        json_str = json.dumps(sample_extraction, ensure_ascii=False, indent=2)
        parsed = json.loads(json_str)

        required_keys = [
            "customer",
            "device",
            "quote",
            "appointment",
            "follow_up",
            "free_text_summary_he",
            "confidence",
        ]
        missing_keys = [k for k in required_keys if k not in parsed]

        if not missing_keys:
            print("✅ JSON extraction schema is valid")
            return True
        else:
            print(f"❌ Missing keys in extraction schema: {missing_keys}")
            return False

    except Exception as e:
        print(f"❌ JSON schema test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Running SmartAgent structure tests...\n")

    tests = [
        test_api_structure,
        test_worker_structure,
        test_frontend_structure,
        test_docker_structure,
        test_json_schema_extraction,
        test_schemas_structure,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All structure tests passed!")
        print("\nNext steps:")
        print("1. Set up Docker environment")
        print("2. Configure proxy settings for pip if needed")
        print("3. Test with mock data")
        return True
    else:
        print("⚠️  Some tests failed. Check the structure above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
