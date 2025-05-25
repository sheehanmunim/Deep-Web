# Multiple File Upload Features

## Overview

The Deep Live Cam web interface now supports uploading and processing multiple files simultaneously, enabling efficient batch processing of face swapping tasks.

## New Features

### 1. Multiple File Upload

- **Source Files**: Upload multiple source faces (images only)
- **Target Files**: Upload multiple target videos/images
- **Drag & Drop**: Supports dragging multiple files at once
- **File Preview**: Shows thumbnails for uploaded images and video first frames

### 2. File Management

- **File List Display**: Visual list showing all uploaded files with previews
- **Individual File Removal**: Remove specific files without affecting others
- **Clear All**: Quick button to remove all uploaded files
- **File Counter**: Shows total number of source and target files

### 3. Batch Processing

- **Automatic Batch Mode**: Processes all target files using the first source face
- **Progress Tracking**: Real-time status updates for each file being processed
- **Batch Progress**: Shows current file being processed (e.g., "Processing file 2 of 5")
- **Error Handling**: Continues processing other files if one fails

### 4. Results Management

- **Multiple Results Display**: Grid layout showing all processed results
- **Individual Previews**: Thumbnail preview for each result
- **Individual Downloads**: Download specific result files
- **Batch Download**: Download all results (staggered to avoid browser limits)

## How to Use

### Upload Multiple Files

1. Click the upload areas or drag multiple files
2. Source area: Select multiple face images
3. Target area: Select multiple videos/images to process
4. Files will appear in the management section below

### Manage Files

- View all uploaded files in the "Uploaded Files" section
- Remove individual files using the "Remove" button
- Clear all files using the "Clear All" button
- File counts are displayed in real-time

### Batch Processing

1. Ensure you have at least one source and one target file
2. Click "Start Batch Processing (X files)"
3. Monitor progress in real-time
4. View results as they're completed

### Download Results

- Individual downloads: Click "Download" on specific results
- Batch download: Click "Download All Results" for all files
- Results include both image and video outputs with previews

## Technical Implementation

### Backend Changes

- Modified upload endpoint to handle multiple files via `getlist('file')`
- Added file management endpoints (`/files`, `/clear-files`)
- Implemented batch processing with sequential file handling
- Enhanced status tracking with batch progress information
- Added results endpoint for retrieving all processing results

### Frontend Changes

- Updated HTML to support multiple file selection (`multiple` attribute)
- Added file management interface with drag & drop support
- Implemented real-time file list updates
- Enhanced progress tracking for batch operations
- Created grid-based results display

### Storage

- Files stored with unique timestamps to prevent conflicts
- Maintains separate lists for source and target files
- Results stored with source/target relationships
- Preview images generated for all file types

## Benefits

1. **Efficiency**: Process multiple files in one session
2. **Convenience**: Upload all files at once, process in batch
3. **Organization**: Clear file management and result organization
4. **Flexibility**: Mix of images and videos in targets
5. **User Experience**: Visual feedback and progress tracking

## Example Workflow

1. Upload 3 source face images
2. Upload 10 target videos/images
3. Start batch processing
4. System processes all 10 targets using the first source face
5. View grid of 10 results with previews
6. Download individual results or all at once

This enhancement transforms the web interface from single-file processing to a powerful batch processing tool suitable for production workflows.
