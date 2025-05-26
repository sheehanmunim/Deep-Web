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
from modules.memory_optimizer import memory_optimizer

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
    
    # Run memory diagnostics to get optimal settings
    print("🔍 Analyzing system for optimal memory configuration...")
    sys_mem = memory_optimizer._get_system_memory_info()
    gpu_info = memory_optimizer._get_gpu_memory_info()
    
    print(f"💾 System RAM: {sys_mem['available']:.1f}GB available of {sys_mem['total']:.1f}GB total")
    if gpu_info:
        for gpu_id, info in gpu_info.items():
            print(f"🎮 GPU {gpu_id}: {info['name']} - {info['free']:.1f}GB available of {info['total']:.1f}GB total")
    
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
        
        # Enable memory optimization
        if '--enable-memory-optimization' not in sys.argv:
            sys.argv.append('--enable-memory-optimization')
            print("✅ Enabled advanced memory optimization")
        
        # Set optimal GPU memory fraction based on GPU capabilities
        if '--gpu-memory-fraction' not in sys.argv and gpu_info:
            primary_gpu = gpu_info[0]
            if primary_gpu['total'] < 8:
                gpu_fraction = 0.6  # Conservative for GPUs < 8GB
                print(f"🎮 GPU Memory: Using 60% of {primary_gpu['total']:.1f}GB VRAM (conservative for <8GB GPU)")
            else:
                gpu_fraction = 0.8  # More aggressive for larger GPUs
                print(f"🎮 GPU Memory: Using 80% of {primary_gpu['total']:.1f}GB VRAM")
            
            sys.argv.extend(['--gpu-memory-fraction', str(gpu_fraction)])
        
        # Set reasonable system memory limit
        if '--max-memory' not in sys.argv:
            if sys_mem['available'] < 8:
                recommended_memory = 4
                print(f"💾 System Memory: Limited to 4GB (system has {sys_mem['available']:.1f}GB available)")
            else:
                recommended_memory = min(8, int(sys_mem['available'] * 0.7))
                print(f"💾 System Memory: Limited to {recommended_memory}GB (70% of available)")
            
            sys.argv.extend(['--max-memory', str(recommended_memory)])
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
        print("🚀 GPU acceleration enabled with memory optimization!")
        print("💡 Memory settings automatically optimized for your hardware")
    else:
        print("🐌 Running on CPU with memory optimization")
    
    print("🔗 For Google Colab support, use: python run_web_colab.py")
    print("🔍 For manual optimization, run: python memory_diagnostics.py")
    print("=" * 40)
    
    # Start the core application
    core.run()

if __name__ == '__main__':
    main() 