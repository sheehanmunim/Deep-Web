#!/usr/bin/env python3
"""
Test script for web interface memory optimization
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the web interface
from run_web import setup_gpu_acceleration, check_onnx_runtime_gpu
from modules.memory_optimizer import memory_optimizer

def test_web_optimization():
    """Test the web interface memory optimization"""
    print("🧪 Testing Web Interface Memory Optimization")
    print("=" * 50)
    
    # Test memory analysis
    print("🔍 Analyzing system memory...")
    sys_mem = memory_optimizer._get_system_memory_info()
    gpu_info = memory_optimizer._get_gpu_memory_info()
    
    print(f"💾 System RAM: {sys_mem['available']:.1f}GB available of {sys_mem['total']:.1f}GB total")
    if gpu_info:
        for gpu_id, info in gpu_info.items():
            print(f"🎮 GPU {gpu_id}: {info['name']} - {info['free']:.1f}GB available of {info['total']:.1f}GB total")
    
    # Test GPU setup
    print("\n🚀 Testing GPU setup...")
    gpu_available = setup_gpu_acceleration()
    onnx_gpu_available = check_onnx_runtime_gpu() if gpu_available else False
    
    # Simulate argument setup
    test_argv = ['run_web.py', '--web']
    
    if gpu_available and onnx_gpu_available:
        print("\n✅ GPU acceleration would be enabled with these settings:")
        
        # GPU memory fraction
        if gpu_info:
            primary_gpu = gpu_info[0]
            if primary_gpu['total'] < 8:
                gpu_fraction = 0.6
                print(f"   --gpu-memory-fraction {gpu_fraction} (60% of {primary_gpu['total']:.1f}GB VRAM)")
            else:
                gpu_fraction = 0.8
                print(f"   --gpu-memory-fraction {gpu_fraction} (80% of {primary_gpu['total']:.1f}GB VRAM)")
        
        # System memory
        if sys_mem['available'] < 8:
            recommended_memory = 4
            print(f"   --max-memory {recommended_memory} (4GB limit)")
        else:
            recommended_memory = min(8, int(sys_mem['available'] * 0.7))
            print(f"   --max-memory {recommended_memory} (70% of available)")
        
        print("   --execution-provider cuda")
        print("   --enable-memory-optimization")
    else:
        print("\n⚠️  Would run on CPU with memory optimization")
    
    print("\n🌐 Web interface would start with optimized memory settings!")
    print("📍 Access URL: http://localhost:5000")

if __name__ == '__main__':
    test_web_optimization() 