#!/usr/bin/env python3
"""
Deep Live Cam - One-Click Colab Launcher
This script handles everything needed to run Deep Live Cam in Google Colab
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🎭 Deep Live Cam - Google Colab Launcher")
    print("=" * 50)
    print("Real-time face swap with a single click!")
    print("=" * 50)

def check_environment():
    """Check if we're running in Google Colab"""
    try:
        import google.colab
        print("✅ Running in Google Colab environment")
        return True
    except ImportError:
        print("⚠️  Not running in Google Colab")
        return False

def run_command(cmd, description="", live_output=True):
    """Execute a command with optional live output"""
    if description:
        print(f"\n{description}")
    
    if live_output:
        process = subprocess.Popen(
            cmd, shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True,
            bufsize=1
        )
        
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
        
        process.wait()
        return process.returncode == 0
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0

def check_gpu():
    """Check GPU availability"""
    print("\n🔍 Checking GPU availability...")
    
    if run_command("nvidia-smi", live_output=False):
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"✅ GPU detected: {gpu_name}")
                print(f"💾 GPU Memory: {gpu_memory:.1f} GB")
                return True
            else:
                print("⚠️  PyTorch cannot access GPU")
                return False
        except ImportError:
            print("⚠️  PyTorch not available yet")
            return True  # Assume GPU is available, will install PyTorch later
    else:
        print("❌ No GPU detected")
        print("📝 To enable GPU: Runtime → Change runtime type → Hardware accelerator: GPU")
        return False

def install_system_dependencies():
    """Install system-level dependencies"""
    print("\n📦 Installing system dependencies...")
    
    commands = [
        ("apt update -qq", "Updating package lists..."),
        ("apt install -y ffmpeg", "Installing FFmpeg...")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc, live_output=False):
            print(f"❌ Failed to run: {cmd}")
            return False
    
    print("✅ System dependencies installed!")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n🐍 Installing Python dependencies...")
    
    # Install core dependencies
    if not run_command("pip install -r requirements.txt", 
                      "Installing core dependencies..."):
        print("❌ Failed to install core dependencies")
        return False
    
    # Setup GPU acceleration
    print("\n🚀 Setting up GPU acceleration...")
    run_command("pip uninstall -y onnxruntime onnxruntime-gpu", 
               "Removing existing ONNX Runtime...", live_output=False)
    
    if not run_command("pip install onnxruntime-gpu==1.16.3", 
                      "Installing GPU-optimized ONNX Runtime..."):
        print("⚠️  Failed to install GPU ONNX Runtime, falling back to CPU")
        run_command("pip install onnxruntime", live_output=False)
    
    # Install ngrok for tunneling
    if not run_command("pip install pyngrok==7.0.5", 
                      "Installing ngrok..."):
        print("❌ Failed to install ngrok")
        return False
    
    print("✅ Python dependencies installed!")
    return True

def verify_installation():
    """Verify that everything is installed correctly"""
    print("\n🔍 Verifying installation...")
    
    # Check PyTorch GPU
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ PyTorch GPU support: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  PyTorch GPU support not available")
    except ImportError:
        print("❌ PyTorch not available")
        return False
    
    # Check ngrok
    try:
        from pyngrok import ngrok
        print("✅ Ngrok is available")
    except ImportError:
        print("❌ Ngrok not available")
        return False
    
    # Check if main modules exist
    if os.path.exists('modules') and os.path.exists('run_web_colab.py'):
        print("✅ Deep Live Cam modules found")
        return True
    else:
        print("❌ Deep Live Cam modules not found")
        return False

def start_deep_live_cam(ngrok_token=None):
    """Start Deep Live Cam with ngrok"""
    print("\n🌟 Starting Deep Live Cam...")
    
    # Set ngrok token if provided
    if ngrok_token and ngrok_token.strip():
        os.environ['NGROK_AUTH_TOKEN'] = ngrok_token.strip()
        print("🔑 Ngrok auth token configured")
    else:
        print("⚠️  No ngrok auth token provided")
        print("   Get a free token at: https://dashboard.ngrok.com/get-started/your-authtoken")
    
    print("\n" + "=" * 50)
    print("🎬 Deep Live Cam is starting...")
    print("📋 Instructions:")
    print("  1. Wait for the ngrok URL to appear below")
    print("  2. Click the URL to access the web interface")
    print("  3. Upload your source face image")
    print("  4. Upload your target image/video")
    print("  5. Configure settings and start processing!")
    print("\n⚠️  Keep this cell running to maintain the web interface")
    print("=" * 50)
    
    # Start the web interface
    return run_command("python run_web_colab.py", "Launching web interface...")

def main(ngrok_token=""):
    """Main launcher function"""
    print_banner()
    
    # Check environment
    in_colab = check_environment()
    
    # Check GPU
    gpu_available = check_gpu()
    
    # Install dependencies
    if not install_system_dependencies():
        print("❌ Failed to install system dependencies")
        return False
    
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return False
    
    # Verify installation
    if not verify_installation():
        print("❌ Installation verification failed")
        return False
    
    # Start the application
    if not start_deep_live_cam(ngrok_token):
        print("❌ Failed to start Deep Live Cam")
        return False
    
    return True

if __name__ == "__main__":
    # Extract ngrok token from command line args if provided
    ngrok_token = ""
    if len(sys.argv) > 1:
        ngrok_token = sys.argv[1]
    
    try:
        main(ngrok_token)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Deep Live Cam...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're using a GPU runtime")
        print("2. Restart the runtime and try again")
        print("3. Check the GitHub repository for updates") 