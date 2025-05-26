#!/usr/bin/env python3
"""
Deep Live Cam Web Interface
Local web interface with automatic GPU acceleration detection
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import core

def setup_gpu_acceleration():
    """Set up GPU acceleration for faster processing"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🚀 CUDA GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("💻 No CUDA GPU detected, using CPU")
            return False
    except ImportError:
        print("⚠️  PyTorch not available, cannot detect GPU")
        return False

def check_onnx_runtime_gpu():
    """Check if ONNX Runtime GPU is properly installed"""
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in providers:
            return True
        else:
            print("⚠️  ONNX Runtime GPU not available")
            print("   Run 'python fix_gpu_setup.py' to fix GPU acceleration")
            return False
    except ImportError:
        print("⚠️  ONNX Runtime not installed")
        return False

def main():
    """Main function to run Deep Live Cam web interface"""
    print("🎭 Deep Live Cam - Web Interface")
    print("=" * 40)
    
    # Check GPU availability
    gpu_available = setup_gpu_acceleration()
    onnx_gpu_available = check_onnx_runtime_gpu() if gpu_available else False
    
    # Add command line arguments for optimal performance
    if '--web' not in sys.argv:
        sys.argv.append('--web')
    
    # Add GPU acceleration if available and properly configured
    if gpu_available and onnx_gpu_available:
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
    elif gpu_available and not onnx_gpu_available:
        print("🔧 GPU detected but ONNX Runtime GPU not properly installed")
        print("   Run 'python fix_gpu_setup.py' or 'fix-gpu-setup.bat' to enable GPU acceleration")
    else:
        print("🐌 Running on CPU - processing will be slower")
        print("   For GPU acceleration, ensure you have:")
        print("   1. NVIDIA GPU with CUDA support")
        print("   2. CUDA toolkit installed")
        print("   3. ONNX Runtime GPU: pip install onnxruntime-gpu==1.16.3")
    
    print("\n🌐 Starting Deep Live Cam Web Interface...")
    print("📍 Access your interface at: http://localhost:5000")
    
    if gpu_available and onnx_gpu_available:
        print("🚀 GPU acceleration enabled for faster processing!")
    
    print("🔗 For Google Colab support, use: python run_web_colab.py")
    print("=" * 40)
    
    # Start the core application
    core.run()

if __name__ == '__main__':
    main() 