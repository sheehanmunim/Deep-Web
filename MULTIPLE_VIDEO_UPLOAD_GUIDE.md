# Multiple Video Upload Guide 🎥

## Overview

Deep Live Cam supports uploading and processing **multiple video files simultaneously**, making it perfect for batch face swapping operations. This feature allows you to process dozens of videos at once with the same source face(s).

## ✨ Features

### 🎬 Multiple Video Support

- Upload multiple videos at once (drag & drop or file selector)
- Support for various formats: **MP4, AVI, MOV, MKV, WebM, FLV, M4V, 3GP**
- File size limit: **500MB per video file**
- Mix videos and images in the same batch

### 🚀 Batch Processing

- Process all uploaded videos automatically
- Real-time progress tracking for each video
- Detailed processing logs with frame-by-frame progress
- Memory optimization for multiple large videos

### 📁 File Management

- Visual preview for all uploaded files
- Individual file removal without affecting others
- Bulk clear options (clear sources, targets, or all)
- File type indicators and counts

### 📦 Results Management

- Download individual processed videos
- Bulk download all results as ZIP
- Video preview with full-screen playback
- Processing status for each file

## 🎯 How to Use

### Step 1: Upload Source Face(s)

1. Click the **"Select Source Faces"** box or drag images
2. Choose one or more face images (JPG, PNG, etc.)
3. Preview thumbnails will appear

### Step 2: Upload Target Videos

1. Click the **"Select Target Videos/Images"** box
2. **Select multiple video files** using:
   - **Ctrl+Click** (Windows/Linux) or **Cmd+Click** (Mac) to select multiple files
   - **Drag and drop** multiple files at once
3. Supported formats are clearly shown in the upload box
4. Watch the upload progress and file count

### Step 3: Review Uploaded Files

- Check the **"Uploaded Files"** section
- See video thumbnails and file information
- Remove individual files if needed
- Use clear buttons to start over

### Step 4: Configure Settings

- Adjust processing settings as needed:
  - **Keep FPS**: Maintain original video frame rate
  - **Keep Audio**: Preserve original audio track
  - **Face Enhancer**: Improve face quality (may affect performance)

### Step 5: Start Batch Processing

1. Click **"🚀 Start Batch Processing"** button
2. The button shows how many files will be processed
3. Watch real-time progress for each video
4. View detailed processing logs

### Step 6: Download Results

- **Individual Downloads**: Click download button for specific videos
- **Bulk Download**: Download all results as a ZIP file
- **Video Preview**: Click videos to play them full-screen

## 💡 Tips for Best Performance

### Video Format Recommendations

- **MP4**: Best compatibility and performance
- **H.264 codec**: Fastest processing
- **1080p or lower**: Optimal balance of quality and speed

### File Size Management

- Keep videos under **500MB each** for faster uploads
- Consider compressing very large videos before upload
- Use MP4 format for best compression

### Batch Size Guidelines

- **1-5 videos**: Excellent performance
- **5-10 videos**: Good performance (may take longer)
- **10+ videos**: Consider processing in smaller batches

### Memory Optimization

- Close other applications to free up RAM
- The system automatically optimizes memory usage
- GPU acceleration is used when available

## 🔧 Technical Details

### Supported Video Formats

| Format | Extension | Recommended |
| ------ | --------- | ----------- |
| MP4    | .mp4      | ✅ **Best** |
| AVI    | .avi      | ✅ Good     |
| MOV    | .mov      | ✅ Good     |
| MKV    | .mkv      | ✅ Good     |
| WebM   | .webm     | ⚠️ OK       |
| FLV    | .flv      | ⚠️ OK       |
| M4V    | .m4v      | ⚠️ OK       |
| 3GP    | .3gp      | ⚠️ OK       |

### System Requirements

- **RAM**: 8GB+ recommended for multiple videos
- **GPU**: CUDA-compatible GPU for faster processing
- **Storage**: Enough space for input + output videos
- **CPU**: Multi-core processor recommended

### Processing Features

- **Automatic GPU detection** and optimization
- **Memory management** prevents system overload
- **Progress tracking** with ETA calculations
- **Error handling** continues processing if one file fails

## 🚨 Troubleshooting

### Upload Issues

- **File too large**: Ensure videos are under 500MB each
- **Format not supported**: Convert to MP4 using FFmpeg or similar tools
- **Upload fails**: Check internet connection and try smaller batches

### Processing Issues

- **Out of memory**: Try smaller batches or lower resolution videos
- **Processing stuck**: Check GPU drivers and CUDA installation
- **Poor quality**: Enable face enhancer (may be slower)

### Performance Issues

- **Slow processing**: Ensure GPU acceleration is enabled
- **System lag**: Close other applications and try smaller batches
- **Long wait times**: Normal for large videos, check progress logs

## 📊 Example Workflows

### Content Creator Workflow

1. Upload 10 video clips (30 seconds each)
2. Use the same face for all videos
3. Process in one batch
4. Download as ZIP for easy organization

### Social Media Batch

1. Upload multiple TikTok/Instagram videos
2. Different face for different videos (process separately)
3. Preview results before downloading
4. Individual downloads for posting

### Professional Video Production

1. Upload scene cuts from a larger project
2. Apply same face replacement across all scenes
3. Use face enhancer for higher quality
4. Download all for video editing software

## 🎉 Benefits of Multiple Video Upload

- **Time Saving**: Process multiple videos without manual intervention
- **Consistency**: Same settings applied to all videos
- **Convenience**: One-click download of all results
- **Organization**: Clear file management and tracking
- **Efficiency**: Optimized memory usage for batch operations

---

**Ready to process multiple videos?** Start by uploading your source face, then select multiple target videos and watch the magic happen! 🎭✨
