#!/usr/bin/env python3
"""
Google Colab Web Interface with Ngrok Support
This script is specifically designed for users running Deep Live Cam in Google Colab.
It automatically sets up ngrok to expose the web interface to the internet.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pyngrok import ngrok
    print("✓ Ngrok is available")
except ImportError:
    print("❌ Error: pyngrok is not installed. Please run:")
    print("pip install pyngrok==7.0.5")
    sys.exit(1)

from modules import core
import modules.globals

def setup_ngrok(auth_token=None, port=5000):
    """
    Set up ngrok tunnel for Google Colab
    
    Args:
        auth_token (str): Your ngrok authtoken. Get it from https://dashboard.ngrok.com/get-started/your-authtoken
        port (int): Local port to expose (default: 5000)
    
    Returns:
        str: Public ngrok URL
    """
    try:
        # Set auth token if provided
        if auth_token:
            ngrok.set_auth_token(auth_token)
            print(f"✓ Ngrok auth token set")
        else:
            print("⚠️  Warning: No auth token provided. You may hit ngrok's rate limits.")
            print("   Get your free auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
        
        # Terminate any previous ngrok sessions
        ngrok.kill()
        print("✓ Cleared previous ngrok sessions")
        
        # Open a tunnel to the specified port
        public_url = ngrok.connect(port)
        print(f"🚀 Ngrok tunnel is active!")
        print(f"📱 Access your Deep Live Cam Web Interface at: {public_url}")
        print(f"🔗 Direct link: {public_url}")
        
        return str(public_url)
        
    except Exception as e:
        print(f"❌ Error setting up ngrok: {e}")
        print("Make sure you have:")
        print("1. Installed pyngrok: pip install pyngrok==7.0.5")
        print("2. Set a valid auth token (optional but recommended)")
        sys.exit(1)

def setup_gpu_acceleration():
    """Set up GPU acceleration for faster processing"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🚀 CUDA GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  CUDA GPU not available, falling back to CPU")
            return False
    except ImportError:
        print("⚠️  PyTorch not available, cannot detect GPU")
        return False

def main():
    """Main function to run Deep Live Cam with ngrok in Google Colab"""
    
    print("🎭 Deep Live Cam - Google Colab Edition")
    print("=" * 50)
    
    # Check GPU availability
    gpu_available = setup_gpu_acceleration()
    
    # Default ngrok auth token (replace with your own)
    # Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken
    DEFAULT_AUTH_TOKEN = "2xbuOdCZEZxqQGx2r77BMgijYAm_5CTUFPLuyB8FWXWCLAmm8"
    
    # You can also set the token via environment variable
    auth_token = os.getenv('NGROK_AUTH_TOKEN', DEFAULT_AUTH_TOKEN)
    
    # Set up ngrok tunnel
    port = 5000
    public_url = setup_ngrok(auth_token, port)
    
    # Add command line arguments for optimal performance
    if '--web' not in sys.argv:
        sys.argv.append('--web')
    
    # Add GPU acceleration if available
    if gpu_available:
        if '--execution-provider' not in sys.argv:
            sys.argv.extend(['--execution-provider', 'cuda'])
            print("✅ Enabled CUDA GPU acceleration")
        
        # Set reasonable memory limit (leave some for system)
        if '--max-memory' not in sys.argv:
            try:
                import torch
                gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
                # Use 80% of GPU memory to leave some for system
                recommended_memory = max(4, int(gpu_memory_gb * 0.8))
                sys.argv.extend(['--max-memory', str(recommended_memory)])
                print(f"✅ Set memory limit to {recommended_memory}GB")
            except:
                pass
    else:
        print("🐌 Running on CPU - processing will be slower")
    
    print("\n🌟 Starting Deep Live Cam Web Interface...")
    print("📋 Instructions:")
    print("1. Click the ngrok URL above to access the web interface")
    print("2. Upload your source face image")
    print("3. Upload your target image/video")
    print("4. Configure settings as needed")
    print("5. Click 'Process' to start face swapping")
    if gpu_available:
        print("🚀 GPU acceleration enabled for faster processing!")
    print("\n⚠️  Note: Keep this cell running to maintain the ngrok tunnel")
    print("=" * 50)
    
    # Start the core application
    core.run()

if __name__ == '__main__':
    main() 