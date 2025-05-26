import sys
import importlib
from concurrent.futures import ThreadPoolExecutor
from types import ModuleType
from typing import Any, List, Callable
from tqdm import tqdm

import modules
import modules.globals                   

FRAME_PROCESSORS_MODULES: List[ModuleType] = []
FRAME_PROCESSORS_INTERFACE = [
    'pre_check',
    'pre_start',
    'process_frame',
    'process_image',
    'process_video'
]


def load_frame_processor_module(frame_processor: str) -> Any:
    try:
        frame_processor_module = importlib.import_module(f'modules.processors.frame.{frame_processor}')
        for method_name in FRAME_PROCESSORS_INTERFACE:
            if not hasattr(frame_processor_module, method_name):
                sys.exit()
    except ImportError:
        print(f"Frame processor {frame_processor} not found")
        sys.exit()
    return frame_processor_module


def get_frame_processors_modules(frame_processors: List[str]) -> List[ModuleType]:
    global FRAME_PROCESSORS_MODULES

    if not FRAME_PROCESSORS_MODULES:
        for frame_processor in frame_processors:
            frame_processor_module = load_frame_processor_module(frame_processor)
            FRAME_PROCESSORS_MODULES.append(frame_processor_module)
    set_frame_processors_modules_from_ui(frame_processors)
    return FRAME_PROCESSORS_MODULES

def set_frame_processors_modules_from_ui(frame_processors: List[str]) -> None:
    global FRAME_PROCESSORS_MODULES
    for frame_processor, state in modules.globals.fp_ui.items():
        if state == True and frame_processor not in frame_processors:
            frame_processor_module = load_frame_processor_module(frame_processor)
            FRAME_PROCESSORS_MODULES.append(frame_processor_module)
            modules.globals.frame_processors.append(frame_processor)
        if state == False:
            try:
                frame_processor_module = load_frame_processor_module(frame_processor)
                FRAME_PROCESSORS_MODULES.remove(frame_processor_module)
                modules.globals.frame_processors.remove(frame_processor)
            except:
                pass

def multi_process_frame(source_path: str, temp_frame_paths: List[str], process_frames: Callable[[str, List[str], Any], None], progress: Any = None) -> None:
    with ThreadPoolExecutor(max_workers=modules.globals.execution_threads) as executor:
        futures = []
        for path in temp_frame_paths:
            future = executor.submit(process_frames, source_path, [path], progress)
            futures.append(future)
        for future in futures:
            future.result()


def process_video(source_path: str, frame_paths: list[str], process_frames: Callable[[str, List[str], Any], None]) -> None:
    progress_bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
    total = len(frame_paths)
    
    # Use a simpler approach with a wrapper that tracks progress
    import time
    last_update_time = 0
    
    def update_web_progress(pbar):
        nonlocal last_update_time
        current_time = time.time()
        
        # Only update every 0.5 seconds to avoid spamming
        if current_time - last_update_time < 0.5:
            return
        last_update_time = current_time
        
        try:
            from modules.core import update_status
            
            # Calculate percentage
            percentage = int((pbar.n / pbar.total) * 100) if pbar.total > 0 else 0
            
            # Calculate timing information more accurately
            current_time = time.time()
            elapsed_time = current_time - pbar.start_t
            elapsed = pbar.format_interval(elapsed_time)
            
            # Calculate rate (time per frame)
            if pbar.n > 0 and elapsed_time > 0:
                rate_value = elapsed_time / pbar.n
                rate = f"{rate_value:.2f}s/frame"
            else:
                rate = "0.00s/frame"
            
            # Calculate remaining time
            if pbar.n > 0 and elapsed_time > 0:
                remaining_frames = pbar.total - pbar.n
                time_per_frame = elapsed_time / pbar.n
                eta_seconds = remaining_frames * time_per_frame
                remaining = pbar.format_interval(eta_seconds)
            else:
                remaining = '00:00'
            
            # Create progress message that matches the expected format
            postfix_str = f"execution_providers={modules.globals.execution_providers}, execution_threads={modules.globals.execution_threads}, max_memory={modules.globals.max_memory}"
            progress_msg = f"{percentage:3d}%|{'█' * (percentage // 4)}{'▊' if percentage % 4 >= 2 else ''}{'▏' if percentage % 4 == 1 else ''}{'▎' if percentage % 4 == 3 else ''}{' ' * (25 - percentage // 4)}| {pbar.n}/{pbar.total} [{elapsed}<{remaining}, {rate}, {postfix_str}]"
            
            # Send to update_status for web interface parsing
            update_status(progress_msg, 'VIDEO-PROGRESS')
            
        except Exception as e:
            # Fallback to simple progress if detailed formatting fails
            try:
                from modules.core import update_status
                percentage = int((pbar.n / pbar.total) * 100) if pbar.total > 0 else 0
                update_status(f"Processing video frames: {pbar.n}/{pbar.total} ({percentage}%)", 'VIDEO-PROGRESS')
            except:
                pass
    
    # Custom progress class that calls our update function
    class WebProgressBar(tqdm):
        def update(self, n=1):
            result = super().update(n)
            update_web_progress(self)
            return result
    
    with WebProgressBar(total=total, desc='Processing', unit='frame', dynamic_ncols=True, bar_format=progress_bar_format) as progress:
        progress.set_postfix({'execution_providers': modules.globals.execution_providers, 'execution_threads': modules.globals.execution_threads, 'max_memory': modules.globals.max_memory})
        multi_process_frame(source_path, frame_paths, process_frames, progress)
