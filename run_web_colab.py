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

import subprocess
import time

print("✓ Cloudflare tunnel will be set up automatically")

from modules import core
import modules.globals
from modules.memory_optimizer import memory_optimizer

def setup_cloudflare_tunnel(port=5000):
    """
    Set up Cloudflare tunnel for Google Colab with optimized settings
    
    Args:
        port (int): Local port to expose (default: 5000)
    
    Returns:
        str: Status message
    """
    try:
        # Download and setup cloudflared
        print("📦 Setting up Cloudflare tunnel...")
        subprocess.run(["wget", "-q", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "-O", "cloudflared"], check=True)
        subprocess.run(["chmod", "+x", "cloudflared"], check=True)
        
        # Start cloudflared tunnel with optimized settings for better download performance
        print("🚀 Starting Cloudflare Tunnel with optimized settings...")
        tunnel_process = subprocess.Popen([
            "./cloudflared", "tunnel", 
            "--url", f"http://localhost:{port}",
            "--no-autoupdate",
            "--protocol", "http2",  # Use HTTP/2 for better performance
            "--http2-origin",       # Enable HTTP/2 to origin
            "--compression-quality", "2",  # Lower compression for faster downloads
            "--no-chunked-encoding"  # Disable chunked encoding for large files
        ])
        
        # Give time for the tunnel to connect
        print("⏳ Initializing tunnel...")
        time.sleep(5)
        
        print("🌐 Cloudflare tunnel is active!")
        print("📱 Look for your public URL in the output above")
        print("🔗 It will look like: https://random-subdomain.trycloudflare.com")
        print("✅ Optimized for faster downloads with HTTP/2 and reduced compression!")
        
        return "tunnel_active"
        
    except Exception as e:
        print(f"❌ Error setting up Cloudflare tunnel: {e}")
        print("Make sure you have:")
        print("1. Internet connection to download cloudflared")
        print("2. Proper permissions in the Colab environment")
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
    """Main function to run Deep Live Cam with Cloudflare tunnel in Google Colab"""
    
    print("🎭 Deep Live Cam - Google Colab Edition")
    print("=" * 50)
    
    # Check GPU availability
    gpu_available = setup_gpu_acceleration()
    
    # Set up Cloudflare tunnel
    port = 5000
    tunnel_status = setup_cloudflare_tunnel(port)
    
    # Add command line arguments for optimal performance
    if '--web' not in sys.argv:
        sys.argv.append('--web')
    
    # Apply memory optimizations
    print("🔍 Optimizing memory configuration for Google Colab...")
    sys_mem = memory_optimizer._get_system_memory_info()
    gpu_info = memory_optimizer._get_gpu_memory_info()
    
    # Add GPU acceleration if available
    if gpu_available:
        if '--execution-provider' not in sys.argv:
            sys.argv.extend(['--execution-provider', 'cuda'])
            print("✅ Enabled CUDA GPU acceleration")
        
        # Enable advanced memory optimization
        if '--enable-memory-optimization' not in sys.argv:
            sys.argv.append('--enable-memory-optimization')
            print("✅ Enabled advanced memory optimization")
        
        # Set optimal GPU memory fraction for Colab (usually has good GPUs)
        if '--gpu-memory-fraction' not in sys.argv and gpu_info:
            primary_gpu = gpu_info[0]
            # Colab typically has good GPUs, use aggressive settings
            gpu_fraction = 0.85
            sys.argv.extend(['--gpu-memory-fraction', str(gpu_fraction)])
            print(f"🎮 GPU Memory: Using 85% of {primary_gpu['total']:.1f}GB VRAM (optimized for Colab)")
        
        # Set system memory limit for Colab
        if '--max-memory' not in sys.argv:
            # Colab typically has 12-13GB RAM, use most of it
            recommended_memory = min(10, int(sys_mem['available'] * 0.8))
            sys.argv.extend(['--max-memory', str(recommended_memory)])
            print(f"💾 System Memory: Limited to {recommended_memory}GB (optimized for Colab)")
    else:
        print("🐌 Running on CPU - processing will be slower")
    
    print("\n🌟 Starting Deep Live Cam Web Interface...")
    print("📋 Instructions:")
    print("1. Look for the Cloudflare tunnel URL in the output above")
    print("2. Click the https://xxxxx.trycloudflare.com URL")
    print("3. Upload your source face image")
    print("4. Upload your target image/video")
    print("5. Configure settings as needed")
    print("6. Click 'Process' to start face swapping")
    if gpu_available:
        print("🚀 GPU acceleration enabled for faster processing!")
    print("\n⚠️  Note: Keep this cell running to maintain the Cloudflare tunnel")
    print("=" * 50)
    
    # Start the core application
    core.run()

if __name__ == '__main__':
    main() 