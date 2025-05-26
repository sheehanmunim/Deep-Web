# Memory Optimization Guide for Deep Live Cam

This guide explains how to optimize memory usage to efficiently utilize both system RAM and GPU RAM for better performance.

## Overview

Deep Live Cam now includes advanced memory optimization features that:

- **Intelligently manage GPU memory allocation**
- **Optimize ONNX Runtime session configurations**
- **Balance system RAM and GPU RAM usage**
- **Provide real-time memory monitoring**
- **Automatically tune memory settings based on your hardware**

## Quick Start

### 1. Run Memory Diagnostics

First, analyze your system to get personalized recommendations:

```bash
python memory_diagnostics.py
```

This will show you:

- Current system and GPU memory usage
- Framework compatibility status
- Performance bottlenecks
- Recommended command line arguments

### 2. Use Optimized Settings

Based on the diagnostics, run with optimized settings:

```bash
# For systems with GPU (recommended)
python run.py --execution-provider cuda --gpu-memory-fraction 0.8 --enable-memory-optimization

# For systems with limited GPU memory (< 8GB)
python run.py --execution-provider cuda --gpu-memory-fraction 0.6 --max-memory 4

# For CPU-only systems
python run.py --execution-provider cpu --max-memory 8
```

## Memory Optimization Features

### GPU Memory Management

The new system provides several GPU memory optimizations:

#### 1. **Dynamic GPU Memory Allocation**

- Uses `arena_extend_strategy: kSameAsRequested` for conservative memory allocation
- Automatically calculates optimal GPU memory limits based on available VRAM
- Prevents GPU memory fragmentation

#### 2. **GPU Memory Fraction Control**

```bash
--gpu-memory-fraction 0.8  # Use 80% of GPU memory (default)
--gpu-memory-fraction 0.6  # Use 60% for systems with limited VRAM
--gpu-memory-fraction 0.9  # Use 90% for high-end GPUs with 12GB+ VRAM
```

#### 3. **ONNX Runtime Optimizations**

- Optimized session options for memory efficiency
- Enhanced CUDA provider options
- Memory pattern optimization enabled
- CPU memory arena optimization

### System RAM Management

#### 1. **Intelligent Memory Limits**

The system automatically suggests optimal memory limits based on your hardware:

```bash
--max-memory 4   # For systems with 8GB or less RAM
--max-memory 8   # For systems with 16GB RAM
--max-memory 16  # For systems with 32GB+ RAM
```

#### 2. **Framework Memory Optimization**

- **TensorFlow**: Memory growth enabled, prevents memory leaks
- **PyTorch**: Optimized CUDA memory allocation strategies
- **ONNX Runtime**: Enhanced session configurations

### Advanced Configuration

#### Command Line Options

```bash
# Memory optimization options
--gpu-memory-fraction FLOAT    # GPU memory fraction (0.1-0.95)
--enable-memory-optimization   # Enable advanced optimizations (default: True)
--max-memory INT              # Maximum system RAM in GB

# Execution options
--execution-provider PROVIDER  # cuda, cpu, etc.
--execution-threads INT       # Number of execution threads
```

#### Environment Variables

You can also set these environment variables for additional control:

```bash
# PyTorch CUDA memory allocation
export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:128,garbage_collection_threshold:0.6"

# ONNX Runtime thread control
export OMP_NUM_THREADS=1
```

## Memory Usage Patterns

### Optimal Configuration by Hardware

#### High-End Systems (RTX 4090, RTX 3090, etc.)

```bash
python run.py \
  --execution-provider cuda \
  --gpu-memory-fraction 0.85 \
  --max-memory 16 \
  --execution-threads 8 \
  --enable-memory-optimization
```

#### Mid-Range Systems (RTX 4070, RTX 3070, etc.)

```bash
python run.py \
  --execution-provider cuda \
  --gpu-memory-fraction 0.75 \
  --max-memory 8 \
  --execution-threads 6 \
  --enable-memory-optimization
```

#### Budget Systems (GTX 1660, RTX 3060, etc.)

```bash
python run.py \
  --execution-provider cuda \
  --gpu-memory-fraction 0.6 \
  --max-memory 4 \
  --execution-threads 4 \
  --enable-memory-optimization
```

#### CPU-Only Systems

```bash
python run.py \
  --execution-provider cpu \
  --max-memory 8 \
  --execution-threads 4 \
  --enable-memory-optimization
```

## Monitoring Memory Usage

### Real-Time Monitoring

The system provides real-time memory monitoring during processing:

```
[DLC.MEMORY] System Memory: 8.2GB/16.0GB (51.2%)
[DLC.MEMORY] GPU 0 (NVIDIA GeForce RTX 4070): 4.1GB/12.0GB
```

### Memory Diagnostics

Run the diagnostics script anytime to check current status:

```bash
python memory_diagnostics.py
```

## Troubleshooting

### Common Issues and Solutions

#### 1. **Out of Memory Errors**

```
RuntimeError: CUDA out of memory
```

**Solution**: Reduce GPU memory fraction

```bash
--gpu-memory-fraction 0.5
```

#### 2. **System RAM Exhaustion**

```
MemoryError: Unable to allocate array
```

**Solution**: Reduce max memory setting

```bash
--max-memory 4
```

#### 3. **Slow Performance**

**Solution**: Check if you're using CPU instead of GPU

```bash
python memory_diagnostics.py  # Check GPU availability
--execution-provider cuda     # Force GPU usage
```

#### 4. **Memory Fragmentation**

**Solution**: Enable memory optimization and restart

```bash
--enable-memory-optimization
```

### Performance Tips

1. **Close other applications** before running Deep Live Cam
2. **Use the diagnostics script** to get personalized recommendations
3. **Monitor memory usage** during processing
4. **Adjust settings gradually** if you encounter issues
5. **Restart the application** if memory usage becomes fragmented

## Technical Details

### Memory Allocation Strategy

The optimization system uses a multi-layered approach:

1. **GPU Memory**: Allocated conservatively with `kSameAsRequested` strategy
2. **System RAM**: Limited based on available memory and user settings
3. **Framework Memory**: Each framework (PyTorch, TensorFlow, ONNX) is optimized individually
4. **Cache Management**: Automatic cache clearing between operations

### ONNX Runtime Optimizations

- **Graph Optimization**: `ORT_ENABLE_ALL` for maximum optimization
- **Memory Patterns**: Enabled for better memory reuse
- **Thread Management**: Optimized based on CPU cores
- **Execution Mode**: Sequential for better memory efficiency

### GPU Provider Options

```python
{
    'device_id': 0,
    'gpu_mem_limit': calculated_limit,
    'arena_extend_strategy': 'kSameAsRequested',
    'cudnn_conv_algo_search': 'HEURISTIC',
    'do_copy_in_default_stream': True,
    'cudnn_conv_use_max_workspace': True
}
```

## Contributing

If you encounter memory-related issues or have suggestions for improvements, please:

1. Run `python memory_diagnostics.py` and include the output
2. Specify your hardware configuration
3. Include the command line arguments you used
4. Describe the specific issue or error message

This helps us improve the memory optimization system for everyone!
