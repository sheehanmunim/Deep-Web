# 🎭 Deep Live Cam - Google Colab Setup Guide

This guide will help you run Deep Live Cam in Google Colab with ngrok integration for easy web access.

## 📋 Prerequisites

1. **Google Colab Account**: Sign up at [colab.research.google.com](https://colab.research.google.com)
2. **GPU Runtime**: Essential for face processing
3. **Ngrok Account** (Optional but recommended): Get a free account at [ngrok.com](https://ngrok.com)

## 🚀 Quick Setup

### Step 1: Create a New Colab Notebook

1. Go to [Google Colab](https://colab.research.google.com)
2. Create a new notebook
3. Change runtime to GPU: `Runtime` → `Change runtime type` → `Hardware accelerator: GPU`

### Step 2: Clone and Setup Repository with GPU Support

```python
# Clone the repository
!git clone https://github.com/sheehanmunim/Deep-Web.git
%cd Deep-Web

# Install system dependencies
!apt update -qq
!apt install -y ffmpeg

# Install Python dependencies with GPU support
!pip install -r requirements.txt

# Upgrade to GPU-optimized ONNX Runtime for better performance
!pip uninstall -y onnxruntime onnxruntime-gpu
!pip install onnxruntime-gpu==1.16.3

# Verify GPU setup
import torch
if torch.cuda.is_available():
    print(f"✅ GPU Setup Complete!")
    print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
    print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("⚠️  GPU not detected. Make sure you selected GPU runtime!")
    print("   Go to Runtime → Change runtime type → Hardware accelerator: GPU")
```

### Step 3: Configure Ngrok (Optional but Recommended)

```python
import os

# Replace with your actual ngrok auth token
# Get it from: https://dashboard.ngrok.com/get-started/your-authtoken
NGROK_AUTH_TOKEN = "your_actual_token_here"

# Set environment variable
os.environ['NGROK_AUTH_TOKEN'] = NGROK_AUTH_TOKEN

print("🔑 Ngrok auth token configured")
```

**Note**: If you don't set an auth token, you may hit ngrok's rate limits but it will still work.

### Step 4: Start Deep Live Cam with Ngrok

```python
# Start the web interface with ngrok
!python run_web_colab.py
```

**⚠️ Important**: Keep this cell running to maintain the web interface!

## 📱 Using the Web Interface

1. **Access the Interface**: Click the ngrok URL displayed in the output
2. **Upload Source Image**: Upload the face you want to use as the source
3. **Upload Target**: Upload the image or video for face swapping
4. **Configure Settings**: Adjust quality, face mapping, and other options
5. **Process**: Click "Process" to start face swapping
6. **Download**: Download your processed result

## 🎯 Features Available in Colab

- ✅ Image to Image face swapping
- ✅ Image to Video face swapping
- ✅ Multiple face detection and mapping
- ✅ Face enhancement
- ✅ Color correction
- ✅ Batch processing
- ✅ Real-time preview
- ✅ Download results as ZIP

## 🔧 Troubleshooting

### Common Issues and Solutions

**1. "Runtime disconnected" error**

- Solution: Colab has usage limits. Try reconnecting or using a different account.

**2. "Out of memory" error**

- Solution: Use smaller images/videos or restart the runtime.

**3. "Ngrok tunnel failed" error**

- Solution: Check your auth token or try without it.

**4. Slow processing**

- Solution: Ensure GPU runtime is enabled and try smaller files.

**5. "Module not found" error**

- Solution: Re-run the installation cell.

**6. Still using CPU instead of GPU**

- Check if you enabled GPU runtime: Runtime → Change runtime type → GPU
- Look for "Applied providers: ['CPUExecutionProvider']" in logs
- Solution: Run the GPU fix script:

```python
!python fix_gpu_setup.py
```

### Performance Tips

- **Use GPU**: Always enable GPU runtime for faster processing
- **Optimize File Size**: Smaller files process faster
- **Batch Processing**: Upload multiple targets to process efficiently
- **Keep Session Active**: Don't let the Colab session timeout

## 📊 Expected Processing Times (with GPU)

| File Type | Size       | Estimated Time |
| --------- | ---------- | -------------- |
| Image     | 512x512    | 5-10 seconds   |
| Image     | 1024x1024  | 10-20 seconds  |
| Video     | 480p, 10s  | 1-2 minutes    |
| Video     | 720p, 10s  | 2-4 minutes    |
| Video     | 1080p, 10s | 5-10 minutes   |

## 🆓 Colab Limitations

**Free Tier:**

- 12-hour session limit
- GPU usage caps
- May disconnect if idle

**Pro Tier:**

- 24-hour sessions
- Higher GPU quotas
- Priority access

## 🔒 Privacy and Security

- **Local Processing**: All processing happens in your Colab instance
- **Temporary Storage**: Files are deleted when session ends
- **Ngrok Security**: Use auth tokens for added security
- **No Data Retention**: Google Colab doesn't permanently store your files

## 📚 Additional Resources

- [Deep Live Cam GitHub](https://github.com/sheehanmunim/Deep-Web)
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html)
- [Ngrok Documentation](https://ngrok.com/docs)
- [GPU Runtime Guide](https://colab.research.google.com/notebooks/gpu.ipynb)

## ⚖️ Legal and Ethical Use

**Please use responsibly:**

- ✅ Only use images you have rights to
- ✅ Get consent when using other people's faces
- ✅ Follow local laws and regulations
- ❌ Don't create deepfakes for malicious purposes
- ❌ Don't impersonate others without permission

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the GitHub issues page
3. Join the community discussions
4. Report bugs with detailed information

---

**Enjoy creating with Deep Live Cam! 🎬✨**
