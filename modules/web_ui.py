import os
import json
import base64
import io
import zipfile
from typing import Callable
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import threading
import time

import modules.globals
import modules.metadata
from modules.face_analyser import (
    get_one_face,
    get_unique_faces_from_target_image,
    get_unique_faces_from_target_video,
    add_blank_map,
    has_valid_map,
    simplify_maps,
)
from modules.capturer import get_video_frame, get_video_frame_total
from modules.processors.frame.core import get_frame_processors_modules
from modules.utilities import (
    is_image,
    is_video,
    resolve_relative_path,
    has_image_extension,
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Global variables for tracking processing status
processing_status = {"status": "idle", "message": "Ready", "progress": 0, "preview": None, "detailed_logs": []}
processing_thread = None

# Global variables for multiple file support
uploaded_sources = []  # List of uploaded source files
uploaded_targets = []  # List of uploaded target files
batch_results = []     # List of processing results

# Ensure upload directory exists
upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), UPLOAD_FOLDER)
os.makedirs(upload_dir, exist_ok=True)
UPLOAD_FOLDER = upload_dir

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_video_stream(file_path):
    """Generate video stream with range support for better performance"""
    def generate():
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024 * 1024)  # Read in 1MB chunks
                if not data:
                    break
                yield data
    
    return Response(generate(), mimetype='video/mp4', 
                   headers={'Accept-Ranges': 'bytes'})

def save_switch_states():
    switch_states = {
        "keep_fps": modules.globals.keep_fps,
        "keep_audio": modules.globals.keep_audio,
        "keep_frames": modules.globals.keep_frames,
        "many_faces": modules.globals.many_faces,
        "map_faces": modules.globals.map_faces,
        "color_correction": modules.globals.color_correction,
        "nsfw_filter": modules.globals.nsfw_filter,
        "live_mirror": modules.globals.live_mirror,
        "live_resizable": modules.globals.live_resizable,
        "fp_ui": modules.globals.fp_ui,
        "show_fps": modules.globals.show_fps,
        "mouth_mask": modules.globals.mouth_mask,
        "show_mouth_mask_box": modules.globals.show_mouth_mask_box
    }
    with open("switch_states.json", "w") as f:
        json.dump(switch_states, f)

def load_switch_states():
    try:
        with open("switch_states.json", "r") as f:
            switch_states = json.load(f)
        modules.globals.keep_fps = switch_states.get("keep_fps", True)
        modules.globals.keep_audio = switch_states.get("keep_audio", True)
        modules.globals.keep_frames = switch_states.get("keep_frames", False)
        modules.globals.many_faces = switch_states.get("many_faces", False)
        modules.globals.map_faces = switch_states.get("map_faces", False)
        modules.globals.color_correction = switch_states.get("color_correction", False)
        modules.globals.nsfw_filter = switch_states.get("nsfw_filter", False)
        modules.globals.live_mirror = switch_states.get("live_mirror", False)
        modules.globals.live_resizable = switch_states.get("live_resizable", False)
        modules.globals.fp_ui = switch_states.get("fp_ui", {"face_enhancer": True})
        modules.globals.show_fps = switch_states.get("show_fps", False)
        modules.globals.mouth_mask = switch_states.get("mouth_mask", False)
        modules.globals.show_mouth_mask_box = switch_states.get("show_mouth_mask_box", False)
    except FileNotFoundError:
        pass

def image_to_base64(image_path):
    """Convert image to base64 string for web display"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return None

def update_status(message: str, scope: str = 'WEB') -> None:
    """Update processing status for web interface"""
    global processing_status
    
    # Parse progress information from video processing output
    import re
    progress_match = re.search(r'(\d+)%\|[▏▎▍▌▋▊▉█\s]*\|\s*(\d+)/(\d+)\s*\[([^\]]+)<([^\]]+),\s*([^,]+),\s*execution_providers=([^\]]+)\]', message)
    
    if progress_match:
        percentage = int(progress_match.group(1))
        current_frame = int(progress_match.group(2))
        total_frames = int(progress_match.group(3))
        elapsed_time = progress_match.group(4)
        remaining_time = progress_match.group(5)
        frame_rate = progress_match.group(6)
        execution_provider = progress_match.group(7)
        
        # Update progress with detailed video information
        processing_status["progress"] = percentage
        processing_status["message"] = f"Processing video: {current_frame}/{total_frames} frames ({percentage}%)"
        processing_status["video_progress"] = {
            "current_frame": current_frame,
            "total_frames": total_frames,
            "elapsed_time": elapsed_time,
            "remaining_time": remaining_time,
            "frame_rate": frame_rate,
            "execution_provider": execution_provider.strip("'[]")
        }
        
        # Add detailed log entry with video progress
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        detailed_message = f"[{timestamp}] [VIDEO-PROGRESS] 🎬 Frame {current_frame}/{total_frames} ({percentage}%) | ⏱️ {elapsed_time}<{remaining_time} | 🚀 {frame_rate}"
        processing_status["detailed_logs"].append(detailed_message)
    else:
        # Regular status update
        processing_status["message"] = message
        
        # Add detailed log entry with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Add emoji indicators based on scope
        emoji_map = {
            'BATCH': '🚀',
            'SETUP': '📁', 
            'PROCESS': '🎯',
            'ERROR': '❌',
            'WEB': '🌐',
            'DLC.FACE-SWAPPER': '🎭'
        }
        emoji = emoji_map.get(scope, '📝')
        
        detailed_message = f"[{timestamp}] [{scope}] {emoji} {message}"
        processing_status["detailed_logs"].append(detailed_message)
    
    # Keep only last 50 log entries to prevent memory bloat
    if len(processing_status["detailed_logs"]) > 50:
        processing_status["detailed_logs"] = processing_status["detailed_logs"][-50:]
    
    print(f'[{scope}] {message}')

@app.route('/')
def index():
    """Main page"""
    load_switch_states()
    return render_template('index.html', 
                         metadata=modules.metadata,
                         settings=modules.globals)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads (single or multiple)"""
    global uploaded_sources, uploaded_targets
    
    files = request.files.getlist('file')  # Support multiple files
    file_type = request.form.get('type')  # 'source' or 'target'
    
    if not files or (len(files) == 1 and files[0].filename == ''):
        return jsonify({'error': 'No file selected'}), 400
    
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Generate preview
            preview_data = None
            if is_image(filepath):
                preview_data = image_to_base64(filepath)
            elif is_video(filepath):
                # Generate video thumbnail
                cap = cv2.VideoCapture(filepath)
                ret, frame = cap.read()
                if ret:
                    temp_img_path = f"{filepath}_thumb.jpg"
                    cv2.imwrite(temp_img_path, frame)
                    preview_data = image_to_base64(temp_img_path)
                    os.remove(temp_img_path)
                cap.release()
            
            file_info = {
                'id': len(uploaded_sources) + len(uploaded_targets),
                'filename': filename,
                'original_name': file.filename,
                'filepath': filepath,
                'preview': preview_data,
                'type': 'video' if is_video(filepath) else 'image'
            }
            
            # Add to appropriate list
            if file_type == 'source':
                uploaded_sources.append(file_info)
                # Set first source as default
                if len(uploaded_sources) == 1:
                    modules.globals.source_path = filepath
            elif file_type == 'target':
                uploaded_targets.append(file_info)
                # Set first target as default
                if len(uploaded_targets) == 1:
                    modules.globals.target_path = filepath
            
            uploaded_files.append(file_info)
    
    return jsonify({
        'success': True,
        'files': uploaded_files,
        'total_sources': len(uploaded_sources),
        'total_targets': len(uploaded_targets)
    })

@app.route('/files', methods=['GET'])
def get_uploaded_files():
    """Get list of uploaded files"""
    return jsonify({
        'sources': uploaded_sources,
        'targets': uploaded_targets
    })

@app.route('/files/<file_type>/<int:file_id>', methods=['DELETE'])
def remove_file(file_type, file_id):
    """Remove a specific uploaded file"""
    global uploaded_sources, uploaded_targets
    
    if file_type == 'source':
        uploaded_sources = [f for f in uploaded_sources if f['id'] != file_id]
        # Update default source if needed
        if uploaded_sources:
            modules.globals.source_path = uploaded_sources[0]['filepath']
        else:
            modules.globals.source_path = None
    elif file_type == 'target':
        uploaded_targets = [f for f in uploaded_targets if f['id'] != file_id]
        # Update default target if needed
        if uploaded_targets:
            modules.globals.target_path = uploaded_targets[0]['filepath']
        else:
            modules.globals.target_path = None
    
    return jsonify({'success': True})

@app.route('/clear-files', methods=['POST'])
def clear_all_files():
    """Clear all uploaded files"""
    global uploaded_sources, uploaded_targets, batch_results
    
    uploaded_sources = []
    uploaded_targets = []
    batch_results = []
    modules.globals.source_path = None
    modules.globals.target_path = None
    
    return jsonify({'success': True})

@app.route('/settings', methods=['POST'])
def update_settings():
    """Update application settings"""
    data = request.get_json()
    
    if 'keep_fps' in data:
        modules.globals.keep_fps = data['keep_fps']
    if 'keep_audio' in data:
        modules.globals.keep_audio = data['keep_audio']
    if 'keep_frames' in data:
        modules.globals.keep_frames = data['keep_frames']
    if 'many_faces' in data:
        modules.globals.many_faces = data['many_faces']
    if 'map_faces' in data:
        modules.globals.map_faces = data['map_faces']
    if 'nsfw_filter' in data:
        modules.globals.nsfw_filter = data['nsfw_filter']
    if 'face_enhancer' in data:
        modules.globals.fp_ui['face_enhancer'] = data['face_enhancer']
    
    save_switch_states()
    return jsonify({'success': True})

@app.route('/process', methods=['POST'])
def start_processing():
    """Start the face swapping process (single or batch)"""
    global processing_thread, processing_status, batch_results
    
    if not uploaded_sources or not uploaded_targets:
        return jsonify({'error': 'Please upload both source and target files'}), 400
    
    if processing_thread and processing_thread.is_alive():
        return jsonify({'error': 'Processing already in progress'}), 400
    
    # Reset batch results
    batch_results = []
    
    # Reset status
    processing_status = {"status": "processing", "message": "Starting batch processing...", "progress": 0, "preview": None, "batch_progress": 0, "total_files": len(uploaded_targets), "detailed_logs": []}
    
    # Start batch processing in a separate thread
    def batch_process_wrapper():
        try:
            total_targets = len(uploaded_targets)
            completed = 0
            
            update_status("🚀 Initializing batch processing...", "BATCH")
            update_status(f"📊 Processing {total_targets} target file(s) with source: {uploaded_sources[0]['original_name']}", "BATCH")
            
            for i, target_file in enumerate(uploaded_targets):
                # Use first source file for processing
                source_file = uploaded_sources[0]
                
                update_status(f"📁 Setting up files for target {i+1}/{total_targets}", "SETUP")
                
                # Set current files for processing
                modules.globals.source_path = source_file['filepath']
                modules.globals.target_path = target_file['filepath']
                
                # Set output path
                target_name = os.path.splitext(target_file['filename'])[0]
                target_ext = os.path.splitext(target_file['filepath'])[1]
                output_filename = f"output_{target_name}{target_ext}"
                modules.globals.output_path = os.path.join(UPLOAD_FOLDER, output_filename)
                
                # Update status
                processing_status["message"] = f"Processing {target_file['original_name']} ({i+1}/{total_targets})"
                processing_status["batch_progress"] = i
                
                update_status(f"🎯 Processing: {target_file['original_name']}", "PROCESS")
                update_status(f"💾 Output will be saved as: {output_filename}", "PROCESS")
                
                # Process current file
                from modules.core import start
                start()
                
                update_status(f"✅ Completed processing target {i+1}/{total_targets}", "PROCESS")
                
                # Generate preview of the result
                preview_data = None
                if modules.globals.output_path and os.path.exists(modules.globals.output_path):
                    if is_image(modules.globals.output_path):
                        preview_data = image_to_base64(modules.globals.output_path)
                    elif is_video(modules.globals.output_path):
                        # Generate video thumbnail
                        cap = cv2.VideoCapture(modules.globals.output_path)
                        ret, frame = cap.read()
                        if ret:
                            temp_img_path = f"{modules.globals.output_path}_preview.jpg"
                            cv2.imwrite(temp_img_path, frame)
                            preview_data = image_to_base64(temp_img_path)
                            os.remove(temp_img_path)
                        cap.release()
                
                # Store result
                batch_results.append({
                    'source': source_file['original_name'],
                    'target': target_file['original_name'],
                    'output_path': modules.globals.output_path,
                    'output_filename': output_filename,
                    'preview': preview_data,
                    'status': 'completed'
                })
                
                completed += 1
                processing_status["progress"] = int((completed / total_targets) * 100)
            
            processing_status["status"] = "completed"
            processing_status["message"] = f"Batch processing completed! {completed} files processed."
            processing_status["batch_progress"] = total_targets
            
            update_status("🎉 Batch processing completed successfully!", "BATCH")
            update_status(f"📈 Total files processed: {completed}/{total_targets}", "BATCH")
            
        except Exception as e:
            processing_status["status"] = "error"
            processing_status["message"] = f"Batch processing error: {str(e)}"
            processing_status["progress"] = 0
            processing_status["preview"] = None
            
            update_status(f"❌ Error during batch processing: {str(e)}", "ERROR")
            update_status("🔧 Check your files and settings, then try again", "ERROR")
    
    processing_thread = threading.Thread(target=batch_process_wrapper)
    processing_thread.start()
    
    return jsonify({'success': True, 'message': 'Batch processing started'})

@app.route('/status')
def get_status():
    """Get current processing status"""
    return jsonify(processing_status)

@app.route('/results')
def get_batch_results():
    """Get batch processing results"""
    return jsonify({'results': batch_results})

@app.route('/download')
def download_result():
    """Download the processed result"""
    if not modules.globals.output_path or not os.path.exists(modules.globals.output_path):
        return jsonify({'error': 'No output file available'}), 404
    
    return send_file(modules.globals.output_path, as_attachment=True)

@app.route('/download-all')
def download_all_results():
    """Download all batch results as a ZIP file"""
    global batch_results
    
    if not batch_results:
        return jsonify({'error': 'No results available for download'}), 404
    
    # Create a temporary ZIP file
    zip_filename = f"deep_live_cam_results_{int(time.time())}.zip"
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, result in enumerate(batch_results):
                if os.path.exists(result['output_path']):
                    # Add file to ZIP with a clean name
                    clean_name = f"result_{i+1}_{result['target'].replace(' ', '_')}"
                    file_ext = os.path.splitext(result['output_path'])[1]
                    zipf.write(result['output_path'], f"{clean_name}{file_ext}")
        
        # Send the ZIP file and clean up after
        def remove_file(response):
            try:
                os.remove(zip_path)
            except:
                pass
            return response
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
    
    except Exception as e:
        return jsonify({'error': f'Failed to create ZIP file: {str(e)}'}), 500

@app.route('/preview/<path:filename>')
def preview_file(filename):
    """Serve uploaded files for preview with proper content type"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # For video files, use streaming for better performance
    if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return get_video_stream(file_path)
    elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        return send_file(file_path)

def init_web(start_func: Callable[[], None], destroy_func: Callable[[], None], host='127.0.0.1', port=5000):
    """Initialize and run the web application"""
    global app
    
    load_switch_states()
    
    print(f"Starting Deep Live Cam Web Interface")
    print(f"Open your browser and go to: http://{host}:{port}")
    
    # Override the update_status function in core module
    import modules.core
    modules.core.update_status = update_status
    
    try:
        app.run(host=host, port=port, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        destroy_func() 