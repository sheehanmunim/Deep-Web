# Deep Live Cam - Web Interface Setup Guide

## Overview

This guide explains how to use the new web interface for Deep Live Cam, which provides a modern, browser-based alternative to the desktop GUI.

## Features

✅ **Modern Web Interface** - Clean, responsive design that works on any device  
✅ **Drag & Drop Upload** - Easy file uploading with visual feedback  
✅ **Real-time Progress** - Live status updates during processing  
✅ **Settings Management** - Toggle processing options with intuitive switches  
✅ **File Preview** - Preview uploaded images and video thumbnails  
✅ **Download Results** - Direct download of processed files

## Quick Start

### 1. Install Web Dependencies

If you haven't already installed the web dependencies, run:

```bash
pip install flask==2.3.3 flask-cors==4.0.0 werkzeug==2.3.7
```

Or use the provided batch file (Windows):

```bash
install_web_requirements.bat
```

**Note**: Make sure you also have the core dependencies installed:

```bash
pip install -r requirements.txt
```

### 2. Start the Web Interface

**Option A: Using Python script**

```bash
python run_web.py
```

**Option B: Using batch file (Windows)**

```bash
run-web.bat
```

### 3. Access the Interface

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

## How to Use

1. **Upload Source Face**: Click the left upload box or drag & drop a face image
2. **Upload Target**: Click the right upload box or drag & drop a target image/video
3. **Configure Settings**: Use the toggle switches to adjust processing options:
   - Keep FPS: Maintain original video frame rate
   - Keep Audio: Preserve original audio track
   - Keep Frames: Save temporary processing frames
   - Many Faces: Process multiple faces in the target
   - NSFW Filter: Enable content filtering
   - Face Enhancer: Improve face quality (slower processing)
4. **Start Processing**: Click "Start Processing" button
5. **Monitor Progress**: Watch the real-time progress bar and status messages
6. **Download Result**: Click "Download Result" when processing completes

## File Support

**Source Images**: PNG, JPG, JPEG, GIF  
**Target Files**: PNG, JPG, JPEG, GIF, MP4, AVI, MOV, MKV  
**Max File Size**: 100MB

## Technical Details

### Architecture

- **Backend**: Flask web framework
- **Frontend**: Modern HTML5/CSS3/JavaScript
- **File Handling**: Secure upload with timestamp-based naming
- **Processing**: Threaded background processing
- **Status Updates**: Real-time polling for progress updates

### File Structure

```
├── modules/
│   └── web_ui.py          # Flask web application
├── templates/
│   └── index.html         # Web interface template
├── static/
│   └── style.css          # Additional styles
├── uploads/               # Uploaded files (auto-created)
├── run_web.py            # Web interface launcher
└── run-web.bat           # Windows batch launcher
```

### API Endpoints

- `GET /` - Main interface
- `POST /upload` - File upload handler
- `POST /settings` - Settings update
- `POST /process` - Start processing
- `GET /status` - Processing status
- `GET /download` - Download result
- `GET /preview/<filename>` - File preview

## Troubleshooting

### Common Issues

**1. Port 5000 already in use**

- Solution: Kill the process using port 5000 or modify the port in `web_ui.py`

**2. Module import errors**

- Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

**3. Upload directory permissions**

- Solution: Ensure the application has write permissions in the project directory

**4. Processing fails**

- Solution: Check that both source and target files are uploaded and valid

### Debug Mode

To enable debug mode, modify `web_ui.py`:

```python
app.run(host=host, port=port, debug=True, threaded=True)
```

## Comparison: Web vs Desktop

| Feature           | Web Interface           | Desktop GUI        |
| ----------------- | ----------------------- | ------------------ |
| Accessibility     | Any device with browser | Local machine only |
| File Upload       | Drag & drop + click     | File dialog        |
| Progress Tracking | Real-time updates       | Status bar         |
| Settings          | Toggle switches         | Checkboxes         |
| Preview           | Embedded images         | Separate window    |
| Download          | Direct download         | File saved locally |
| Webcam Support    | Not available           | Available          |
| Face Mapping      | Not available           | Available          |

## Security Notes

- The web interface runs locally (127.0.0.1) by default
- Uploaded files are stored in the `uploads/` directory
- No external network access required
- Files are processed locally on your machine

## Future Enhancements

Planned features for future versions:

- [ ] Webcam support in browser
- [ ] Face mapping interface
- [ ] Batch processing
- [ ] Progress estimation
- [ ] File management interface
- [ ] Settings persistence
- [ ] Mobile optimization

## Support

For issues or questions:

1. Check this guide first
2. Verify all dependencies are installed
3. Try the desktop version to isolate web-specific issues
4. Report bugs with detailed error messages

---

**Enjoy the new web interface! 🚀**
