# Web Interface Memory Optimization Guide

## 🌐 Using Memory Optimization with the Web Interface

Great news! The memory optimization features are now **automatically integrated** into the web interface. You don't need to manually configure complex command line arguments anymore!

## 🚀 Quick Start

### Option 1: Local Web Interface (Recommended)

```bash
python run_web.py
```

### Option 2: Google Colab Web Interface

```bash
python run_web_colab.py
```

### Option 3: Traditional Command Line with Web UI

```bash
python run.py --web --execution-provider cuda --gpu-memory-fraction 0.6 --enable-memory-optimization
```

## ✨ What Happens Automatically

When you run the web interface, it **automatically**:

1. **🔍 Analyzes your system** - Checks available RAM and GPU memory
2. **🎮 Detects your GPU** - Identifies your graphics card and capabilities
3. **⚙️ Optimizes settings** - Automatically configures optimal memory usage
4. **🚀 Enables acceleration** - Uses GPU if available, with optimized memory allocation

## 📊 Example Output

When you run `python run_web.py`, you'll see:

```
🎭 Deep Live Cam - Web Interface
========================================
🔍 Analyzing system for optimal memory configuration...
💾 System RAM: 5.7GB available of 15.9GB total
🎮 GPU 0: NVIDIA GeForce GTX 1050 - 4.0GB available of 4.0GB total
🚀 CUDA GPU detected: NVIDIA GeForce GTX 1050
   GPU Memory: 4.0 GB
✅ Enabled CUDA GPU acceleration
✅ Enabled advanced memory optimization
🎮 GPU Memory: Using 60% of 4.0GB VRAM (conservative for <8GB GPU)
💾 System Memory: Limited to 4GB (system has 5.7GB available)

🌐 Starting Deep Live Cam Web Interface...
📍 Access your interface at: http://localhost:5000
🚀 GPU acceleration enabled with memory optimization!
💡 Memory settings automatically optimized for your hardware
========================================
```

## 🎯 Hardware-Specific Optimizations

The system automatically detects your hardware and applies optimal settings:

### For GPUs with < 8GB VRAM (like GTX 1050, RTX 3060)

- **GPU Memory**: 60% allocation (conservative)
- **System RAM**: 4GB limit (leaves room for OS)
- **Strategy**: Balanced performance and stability

### For GPUs with >= 8GB VRAM (like RTX 3070, RTX 4080)

- **GPU Memory**: 80% allocation (aggressive)
- **System RAM**: Up to 8GB (performance-focused)
- **Strategy**: Maximum performance

### For Google Colab

- **GPU Memory**: 85% allocation (optimized for cloud)
- **System RAM**: Up to 10GB (Colab-optimized)
- **Strategy**: Cloud environment optimized

## 🔧 Manual Override (Optional)

If you want to manually control the settings, you can still use command line arguments:

```bash
# Conservative settings for older systems
python run_web.py --gpu-memory-fraction 0.5 --max-memory 4

# Aggressive settings for high-end systems
python run_web.py --gpu-memory-fraction 0.9 --max-memory 16

# CPU-only mode
python run_web.py --execution-provider cpu --max-memory 8
```

## 📱 Using the Web Interface

1. **Start the interface**:

   ```bash
   python run_web.py
   ```

2. **Open your browser** and go to: `http://localhost:5000`

3. **Upload your files**:

   - Source image (the face you want to use)
   - Target image/video (what you want to swap the face in)

4. **Configure settings** in the web UI as needed

5. **Click "Process"** - The system will use optimized memory settings automatically!

## 🔍 Troubleshooting

### Issue: Out of Memory Error

**Solution**: The web interface will automatically use conservative settings, but you can make them even more conservative:

```bash
python run_web.py --gpu-memory-fraction 0.4 --max-memory 2
```

### Issue: Slow Performance

**Check**: Make sure GPU acceleration is enabled. You should see:

```
✅ Enabled CUDA GPU acceleration
```

If not, run: `python fix_gpu_setup.py`

### Issue: Can't Access Web Interface

**Solution**:

- Make sure port 5000 is not blocked by firewall
- Try accessing `http://127.0.0.1:5000` instead
- Check the console output for any error messages

## 💡 Pro Tips

1. **Close other applications** before starting for maximum memory availability

2. **Check the console output** to see what memory settings were automatically applied

3. **Use Google Colab version** if you need more powerful hardware:

   ```bash
   python run_web_colab.py
   ```

4. **Monitor memory usage** - The system will log memory information during processing

5. **Restart if needed** - If you encounter memory issues, restart the web interface to clear memory caches

## 🎉 Benefits of Web Interface + Memory Optimization

- **No command line complexity** - Everything is automatic
- **Optimal performance** - Hardware-specific optimizations
- **User-friendly** - Simple browser-based interface
- **Real-time monitoring** - See memory usage in console
- **Intelligent allocation** - Balances system and GPU RAM efficiently

## 🔗 Related Commands

- **Get detailed diagnostics**: `python memory_diagnostics.py`
- **Test memory optimization**: `python test_memory_optimization.py`
- **Fix GPU issues**: `python fix_gpu_setup.py`
- **Traditional command line**: `python run.py --help`

---

**🎯 Bottom Line**: Just run `python run_web.py` and everything is automatically optimized for your hardware!
