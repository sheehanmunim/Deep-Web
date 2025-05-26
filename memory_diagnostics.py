#!/usr/bin/env python3
"""
Memory Diagnostics Script for Deep Live Cam
Analyze system and GPU memory and provide optimization recommendations
"""

import sys
import os
import psutil
import platform
from modules.memory_optimizer import memory_optimizer

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_system_info():
    """Print basic system information"""
    print_header("SYSTEM INFORMATION")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    print(f"Python Version: {sys.version.split()[0]}")

def print_memory_info():
    """Print detailed memory information"""
    print_header("MEMORY ANALYSIS")
    
    # System RAM
    sys_mem = memory_optimizer._get_system_memory_info()
    print(f"System RAM:")
    print(f"  Total: {sys_mem['total']:.1f} GB")
    print(f"  Available: {sys_mem['available']:.1f} GB")
    print(f"  Used: {sys_mem['used']:.1f} GB ({sys_mem['percentage']:.1f}%)")
    
    # Virtual memory
    vmem = psutil.virtual_memory()
    print(f"  Free: {vmem.free / (1024**3):.1f} GB")
    
    # Only show buffers and cached on Linux/Unix systems
    if hasattr(vmem, 'buffers') and hasattr(vmem, 'cached'):
        print(f"  Buffers: {vmem.buffers / (1024**3):.1f} GB")
        print(f"  Cached: {vmem.cached / (1024**3):.1f} GB")

def print_gpu_info():
    """Print GPU information if available"""
    print_header("GPU ANALYSIS")
    
    gpu_count = memory_optimizer._get_gpu_count()
    if gpu_count == 0:
        print("❌ No CUDA-capable GPUs detected")
        print("   Consider using CPU-only mode or installing CUDA drivers")
        return
    
    print(f"✅ Found {gpu_count} CUDA-capable GPU(s)")
    
    gpu_info = memory_optimizer._get_gpu_memory_info()
    for gpu_id, info in gpu_info.items():
        print(f"\nGPU {gpu_id}: {info['name']}")
        print(f"  Total VRAM: {info['total']:.1f} GB")
        print(f"  Used VRAM: {info['allocated']:.1f} GB")
        print(f"  Reserved VRAM: {info['reserved']:.1f} GB")
        print(f"  Free VRAM: {info['free']:.1f} GB")
        
        # Memory utilization percentage
        util_percent = (info['reserved'] / info['total']) * 100
        print(f"  Utilization: {util_percent:.1f}%")

def check_frameworks():
    """Check if required frameworks are properly installed"""
    print_header("FRAMEWORK COMPATIBILITY")
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"   CUDA Version: {torch.version.cuda}")
            print(f"   cuDNN Version: {torch.backends.cudnn.version()}")
        else:
            print("   ⚠️  CUDA not available in PyTorch")
    except ImportError:
        print("❌ PyTorch not installed")
    
    # Check TensorFlow
    try:
        import tensorflow as tf
        version = getattr(tf, '__version__', 'Unknown')
        print(f"✅ TensorFlow: {version}")
        try:
            gpu_devices = tf.config.list_physical_devices('GPU')
            if gpu_devices:
                print(f"   GPU Devices: {len(gpu_devices)}")
            else:
                print("   ⚠️  No GPU devices found for TensorFlow")
        except:
            print("   ⚠️  Unable to check GPU devices for TensorFlow")
    except ImportError:
        print("❌ TensorFlow not installed")
    except Exception as e:
        print(f"⚠️  TensorFlow issue: {e}")
    
    # Check ONNX Runtime
    try:
        import onnxruntime as ort
        print(f"✅ ONNX Runtime: {ort.__version__}")
        providers = ort.get_available_providers()
        print(f"   Available Providers: {providers}")
        if 'CUDAExecutionProvider' in providers:
            print("   ✅ CUDA Execution Provider available")
        else:
            print("   ⚠️  CUDA Execution Provider not available")
    except ImportError:
        print("❌ ONNX Runtime not installed")

def analyze_performance_bottlenecks():
    """Analyze potential performance bottlenecks"""
    print_header("PERFORMANCE ANALYSIS")
    
    sys_mem = memory_optimizer._get_system_memory_info()
    gpu_info = memory_optimizer._get_gpu_memory_info()
    
    # System RAM analysis
    if sys_mem['available'] < 4:
        print("⚠️  LOW SYSTEM RAM WARNING:")
        print(f"   Available RAM: {sys_mem['available']:.1f} GB")
        print("   Recommendation: Close other applications or add more RAM")
    elif sys_mem['available'] < 8:
        print("⚠️  MODERATE SYSTEM RAM:")
        print(f"   Available RAM: {sys_mem['available']:.1f} GB")
        print("   Recommendation: Consider reducing max-memory setting")
    else:
        print(f"✅ Adequate system RAM: {sys_mem['available']:.1f} GB available")
    
    # GPU memory analysis
    if gpu_info:
        primary_gpu = gpu_info[0]
        if primary_gpu['free'] < 2:
            print("\n⚠️  LOW GPU MEMORY WARNING:")
            print(f"   Free VRAM: {primary_gpu['free']:.1f} GB")
            print("   Recommendation: Use lower GPU memory fraction (--gpu-memory-fraction 0.6)")
        elif primary_gpu['free'] < 4:
            print(f"\n⚠️  MODERATE GPU MEMORY:")
            print(f"   Free VRAM: {primary_gpu['free']:.1f} GB")
            print("   Recommendation: Use conservative GPU memory settings")
        else:
            print(f"\n✅ Adequate GPU memory: {primary_gpu['free']:.1f} GB available")
    
    # CPU analysis
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        print(f"\n⚠️  HIGH CPU USAGE: {cpu_percent:.1f}%")
        print("   Recommendation: Reduce execution threads or close other applications")
    else:
        print(f"\n✅ CPU usage normal: {cpu_percent:.1f}%")

def provide_optimization_recommendations():
    """Provide specific optimization recommendations"""
    print_header("OPTIMIZATION RECOMMENDATIONS")
    
    sys_mem = memory_optimizer._get_system_memory_info()
    gpu_info = memory_optimizer._get_gpu_memory_info()
    
    recommendations = []
    
    # Memory-based recommendations
    if sys_mem['available'] < 8:
        recommendations.append("Use --max-memory 4 to limit system RAM usage")
    
    if gpu_info and gpu_info[0]['total'] < 8:
        recommendations.append("Use --gpu-memory-fraction 0.6 for GPUs with less than 8GB VRAM")
    elif gpu_info and gpu_info[0]['total'] >= 12:
        recommendations.append("Use --gpu-memory-fraction 0.85 for high-end GPUs with 12GB+ VRAM")
    
    # Provider recommendations
    if gpu_info:
        recommendations.append("Use --execution-provider cuda for GPU acceleration")
    else:
        recommendations.append("Use --execution-provider cpu for CPU-only systems")
    
    # Threading recommendations
    cpu_cores = psutil.cpu_count(logical=False)
    if cpu_cores >= 8:
        recommendations.append(f"Use --execution-threads {min(cpu_cores, 8)} for optimal threading")
    else:
        recommendations.append(f"Use --execution-threads {cpu_cores} for your {cpu_cores}-core system")
    
    if recommendations:
        print("Suggested command line arguments:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        # Generate complete command
        print(f"\n🚀 RECOMMENDED COMMAND:")
        cmd_parts = ["python run.py"]
        
        if gpu_info:
            cmd_parts.append("--execution-provider cuda")
            if gpu_info[0]['total'] < 8:
                cmd_parts.append("--gpu-memory-fraction 0.6")
            else:
                cmd_parts.append("--gpu-memory-fraction 0.8")
        else:
            cmd_parts.append("--execution-provider cpu")
        
        if sys_mem['available'] < 8:
            cmd_parts.append("--max-memory 4")
        
        cmd_parts.append(f"--execution-threads {min(cpu_cores, 8)}")
        cmd_parts.append("--enable-memory-optimization")
        
        print(" ".join(cmd_parts))
    else:
        print("✅ Your system appears to be optimally configured!")

def main():
    """Main diagnostics function"""
    print("🔍 Deep Live Cam - Memory Diagnostics")
    print("This tool will analyze your system and provide optimization recommendations")
    
    try:
        print_system_info()
        print_memory_info()
        print_gpu_info()
        check_frameworks()
        analyze_performance_bottlenecks()
        provide_optimization_recommendations()
        
        print(f"\n{'='*60}")
        print(" Diagnostics Complete!")
        print("💡 For more help, see the documentation or run with --help")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n❌ Error during diagnostics: {e}")
        print("Some features may not be available on your system.")

if __name__ == "__main__":
    main() 