#!/usr/bin/env python3
"""
Test script to verify memory optimization features
"""

import sys
import os

# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def test_memory_optimizer_import():
    """Test that the memory optimizer can be imported"""
    try:
        from modules.memory_optimizer import memory_optimizer
        print("✅ Memory optimizer imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import memory optimizer: {e}")
        return False

def test_memory_info():
    """Test memory information gathering"""
    try:
        from modules.memory_optimizer import memory_optimizer
        
        # Test system memory info
        sys_mem = memory_optimizer._get_system_memory_info()
        print(f"✅ System memory info: {sys_mem['total']:.1f}GB total, {sys_mem['available']:.1f}GB available")
        
        # Test GPU memory info
        gpu_info = memory_optimizer._get_gpu_memory_info()
        if gpu_info:
            for gpu_id, info in gpu_info.items():
                print(f"✅ GPU {gpu_id} info: {info['name']}, {info['total']:.1f}GB total")
        else:
            print("ℹ️  No GPU information available (CPU-only system)")
        
        return True
    except Exception as e:
        print(f"❌ Failed to get memory info: {e}")
        return False

def test_onnx_session_options():
    """Test ONNX Runtime session options generation"""
    try:
        from modules.memory_optimizer import memory_optimizer
        
        session_options = memory_optimizer.get_optimized_onnx_session_options()
        print(f"✅ ONNX session options created successfully")
        print(f"   Graph optimization level: {session_options.graph_optimization_level}")
        print(f"   Intra-op threads: {session_options.intra_op_num_threads}")
        print(f"   Memory pattern enabled: {session_options.enable_mem_pattern}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create ONNX session options: {e}")
        return False

def test_gpu_provider_options():
    """Test GPU provider options generation"""
    try:
        from modules.memory_optimizer import memory_optimizer
        
        provider_options = memory_optimizer.get_optimized_gpu_provider_options()
        if provider_options:
            print(f"✅ GPU provider options created successfully")
            print(f"   Device ID: {provider_options.get('device_id', 'Not set')}")
            print(f"   GPU memory limit: {provider_options.get('gpu_mem_limit', 'Not set')}")
            print(f"   Arena extend strategy: {provider_options.get('arena_extend_strategy', 'Not set')}")
        else:
            print("ℹ️  No GPU provider options (CPU-only system)")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create GPU provider options: {e}")
        return False

def test_memory_optimization():
    """Test the complete memory optimization process"""
    try:
        from modules.memory_optimizer import memory_optimizer
        
        print("🔧 Testing memory optimization...")
        memory_optimizer.optimize_for_inference()
        print("✅ Memory optimization completed successfully")
        
        return True
    except Exception as e:
        print(f"❌ Failed to optimize memory: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Deep Live Cam Memory Optimization")
    print("=" * 50)
    
    tests = [
        ("Memory Optimizer Import", test_memory_optimizer_import),
        ("Memory Information", test_memory_info),
        ("ONNX Session Options", test_onnx_session_options),
        ("GPU Provider Options", test_gpu_provider_options),
        ("Memory Optimization", test_memory_optimization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print(f"\n{'=' * 50}")
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Memory optimization is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 