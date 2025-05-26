import os
import gc
import logging
import psutil
import torch
import tensorflow as tf
import onnxruntime as ort
import modules.globals

logger = logging.getLogger(__name__)

class MemoryOptimizer:
    """
    Advanced memory optimizer that efficiently uses both system RAM and GPU RAM
    """
    
    def __init__(self):
        self.gpu_memory_fraction = 0.8  # Use 80% of GPU memory by default
        self.system_memory_limit = None
        self.gpu_device_count = self._get_gpu_count()
        
    def _get_gpu_count(self) -> int:
        """Get the number of available GPUs"""
        if torch.cuda.is_available():
            return torch.cuda.device_count()
        return 0
    
    def _get_system_memory_info(self):
        """Get system memory information in GB"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024**3),
            'available': memory.available / (1024**3),
            'used': memory.used / (1024**3),
            'percentage': memory.percent
        }
    
    def _get_gpu_memory_info(self):
        """Get GPU memory information for all available GPUs"""
        gpu_info = {}
        if torch.cuda.is_available():
            for i in range(self.gpu_device_count):
                props = torch.cuda.get_device_properties(i)
                allocated = torch.cuda.memory_allocated(i) / (1024**3)
                reserved = torch.cuda.memory_reserved(i) / (1024**3)
                total = props.total_memory / (1024**3)
                
                gpu_info[i] = {
                    'name': props.name,
                    'total': total,
                    'allocated': allocated,
                    'reserved': reserved,
                    'free': total - reserved
                }
        return gpu_info
    
    def configure_tensorflow_memory(self) -> None:
        """Configure TensorFlow for optimal memory usage"""
        try:
            # Get all GPU devices
            gpus = tf.config.experimental.list_physical_devices('GPU')
            
            if gpus:
                for gpu in gpus:
                    # Enable memory growth (allocate memory as needed)
                    tf.config.experimental.set_memory_growth(gpu, True)
                    
                    # Set memory limit if specified
                    if self.system_memory_limit:
                        gpu_memory_limit = int(self.gpu_memory_fraction * self._get_gpu_memory_info()[0]['total'] * 1024)
                        tf.config.experimental.set_memory_growth(gpu, False)
                        tf.config.experimental.set_memory_limit(gpu, gpu_memory_limit)
                
                logger.info(f"Configured TensorFlow memory for {len(gpus)} GPU(s)")
            else:
                logger.info("No GPUs found for TensorFlow")
                
        except Exception as e:
            logger.warning(f"Failed to configure TensorFlow memory: {e}")
    
    def get_optimized_onnx_session_options(self) -> ort.SessionOptions:
        """Get optimized ONNX Runtime session options"""
        session_options = ort.SessionOptions()
        
        # Enable all optimizations
        session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        # Set thread counts based on system capabilities
        cpu_count = psutil.cpu_count(logical=False)
        session_options.intra_op_num_threads = min(cpu_count, 8)
        session_options.inter_op_num_threads = min(cpu_count // 2, 4)
        
        # Enable memory pattern optimization
        session_options.enable_mem_pattern = True
        
        # Enable CPU memory arena optimization
        session_options.enable_cpu_mem_arena = True
        
        # Set execution mode for better memory efficiency
        session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        
        return session_options
    
    def get_optimized_gpu_provider_options(self):
        """Get optimized GPU provider options for ONNX Runtime"""
        gpu_info = self._get_gpu_memory_info()
        
        if not gpu_info:
            return {}
        
        # Use the first GPU (can be extended for multi-GPU)
        primary_gpu = gpu_info[0]
        
        # Calculate optimal memory allocation
        available_gpu_memory = primary_gpu['free'] * 1024 * 1024 * 1024  # Convert to bytes
        gpu_memory_limit = int(available_gpu_memory * self.gpu_memory_fraction)
        
        cuda_options = {
            # Memory optimization
            'device_id': 0,
            'gpu_mem_limit': gpu_memory_limit,
            'arena_extend_strategy': 'kSameAsRequested',  # More conservative memory allocation
            'cudnn_conv_algo_search': 'HEURISTIC',  # Faster initialization
            'do_copy_in_default_stream': True,  # Better memory efficiency
            
            # Performance optimization
            'cudnn_conv_use_max_workspace': True,
            'cudnn_conv1d_pad_to_nc1d': True,
        }
        
        # Enable memory pooling for better GPU memory management
        if hasattr(ort, 'OrtMemoryInfo'):
            cuda_options['enable_cuda_graph'] = False  # Disable for better memory control
        
        return cuda_options
    
    def optimize_torch_memory(self) -> None:
        """Optimize PyTorch memory usage"""
        if torch.cuda.is_available():
            # Set memory fraction for PyTorch
            for i in range(self.gpu_device_count):
                torch.cuda.set_per_process_memory_fraction(self.gpu_memory_fraction, device=i)
            
            # Enable memory efficiency features
            torch.backends.cudnn.benchmark = True  # Optimize for consistent input sizes
            torch.backends.cudnn.deterministic = False  # Allow non-deterministic for speed
            
            # Set CUDA memory allocation strategy
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128,garbage_collection_threshold:0.6'
            
            logger.info(f"Optimized PyTorch memory for {self.gpu_device_count} GPU(s)")
    
    def setup_memory_monitoring(self) -> None:
        """Setup memory monitoring hooks"""
        def log_memory_usage():
            sys_mem = self._get_system_memory_info()
            gpu_mem = self._get_gpu_memory_info()
            
            logger.info(f"System Memory: {sys_mem['used']:.1f}GB/{sys_mem['total']:.1f}GB ({sys_mem['percentage']:.1f}%)")
            
            for gpu_id, info in gpu_mem.items():
                logger.info(f"GPU {gpu_id} ({info['name']}): {info['allocated']:.1f}GB/{info['total']:.1f}GB")
        
        # Log initial memory state
        log_memory_usage()
    
    def clear_memory_cache(self) -> None:
        """Clear memory caches to free up RAM and VRAM"""
        # Clear Python garbage collection
        gc.collect()
        
        # Clear PyTorch CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        
        # Clear TensorFlow memory
        try:
            tf.keras.backend.clear_session()
        except:
            pass
    
    def optimize_for_inference(self) -> None:
        """Apply all optimizations for inference workload"""
        logger.info("Applying memory optimizations...")
        
        # Configure each framework
        self.configure_tensorflow_memory()
        self.optimize_torch_memory()
        
        # Setup monitoring
        self.setup_memory_monitoring()
        
        logger.info("Memory optimization complete")
    
    def get_recommended_batch_size(self, input_size: tuple, model_complexity: str = 'medium') -> int:
        """Get recommended batch size based on available memory"""
        gpu_info = self._get_gpu_memory_info()
        
        if not gpu_info:
            return 1  # CPU-only, use conservative batch size
        
        available_memory_gb = gpu_info[0]['free']
        
        # Estimate memory per sample (rough approximation)
        complexity_multiplier = {
            'low': 0.1,
            'medium': 0.3,
            'high': 0.6
        }
        
        memory_per_sample = (input_size[0] * input_size[1] * 3 * 4) / (1024**3)  # Assuming RGB float32
        memory_per_sample *= complexity_multiplier.get(model_complexity, 0.3)
        
        recommended_batch = max(1, int(available_memory_gb * 0.7 / memory_per_sample))
        
        return min(recommended_batch, 8)  # Cap at 8 for stability


# Global memory optimizer instance
memory_optimizer = MemoryOptimizer() 