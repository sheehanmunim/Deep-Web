#!/usr/bin/env python3
"""
Test script to verify ngrok integration works correctly
"""

import sys
import os

def test_pyngrok_installation():
    """Test if pyngrok is properly installed"""
    try:
        from pyngrok import ngrok
        print("✅ pyngrok is installed and importable")
        return True
    except ImportError as e:
        print(f"❌ pyngrok import failed: {e}")
        print("Install with: pip install pyngrok==7.0.5")
        return False

def test_ngrok_basic_functionality():
    """Test basic ngrok functionality"""
    try:
        from pyngrok import ngrok
        
        # Kill any existing tunnels
        ngrok.kill()
        print("✅ ngrok.kill() works")
        
        # Test tunnel creation (we'll terminate it immediately)
        tunnel = ngrok.connect(8000)
        print(f"✅ Tunnel creation works: {tunnel}")
        
        # Terminate tunnel
        ngrok.disconnect(tunnel.public_url)
        print("✅ Tunnel termination works")
        
        return True
        
    except Exception as e:
        print(f"❌ ngrok functionality test failed: {e}")
        return False

def test_flask_integration():
    """Test if Flask dependencies are available"""
    try:
        from flask import Flask
        from flask_cors import CORS
        print("✅ Flask and CORS are available")
        return True
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    # Test setting and getting ngrok auth token
    test_token = "test_token_123"
    os.environ['NGROK_AUTH_TOKEN'] = test_token
    
    retrieved_token = os.getenv('NGROK_AUTH_TOKEN')
    if retrieved_token == test_token:
        print("✅ Environment variable handling works")
        return True
    else:
        print("❌ Environment variable handling failed")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Testing ngrok integration...")
    print("=" * 50)
    
    tests = [
        ("pyngrok Installation", test_pyngrok_installation),
        ("Flask Integration", test_flask_integration),
        ("Environment Variables", test_environment_variables),
        ("Ngrok Basic Functionality", test_ngrok_basic_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"   ⚠️  {test_name} failed")
        except Exception as e:
            print(f"   ❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ngrok integration is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 