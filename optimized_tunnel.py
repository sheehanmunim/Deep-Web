#!/usr/bin/env python3
"""
Pure Cloudflare Tunnel Optimization for Deep Live Cam
Maximum performance settings without any ngrok dependencies
"""

import subprocess
import time
import os
import sys

class CloudflareOptimizer:
    def __init__(self, port=5000):
        self.port = port
        self.tunnel_process = None
        
    def setup_maximum_performance(self):
        """Setup Cloudflare tunnel with absolute maximum performance settings"""
        try:
            print("📦 Setting up maximum performance Cloudflare tunnel...")
            
            # Download cloudflared if not exists
            if not os.path.exists("cloudflared"):
                subprocess.run([
                    "wget", "-q", 
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", 
                    "-O", "cloudflared"
                ], check=True)
                subprocess.run(["chmod", "+x", "cloudflared"], check=True)
            
            # Maximum performance settings for large file downloads
            print("🚀 Starting Cloudflare tunnel with MAXIMUM performance optimization...")
            self.tunnel_process = subprocess.Popen([
                "./cloudflared", "tunnel",
                "--url", f"http://localhost:{self.port}",
                "--no-autoupdate",
                "--protocol", "auto",                    # Auto-select best protocol
                "--http2-origin",                       # HTTP/2 to origin
                "--compression-quality", "0",           # NO compression for speed
                "--no-chunked-encoding",               # Better for large files
                "--retries", "5",                      # More connection retries
                "--grace-period", "60s",               # Longer grace period
                "--proxy-connect-timeout", "60s",      # Longer connection timeout
                "--proxy-tls-timeout", "60s",          # Longer TLS timeout
                "--proxy-keepalive-connections", "10", # Keep connections alive
                "--proxy-keepalive-timeout", "30s",    # Keepalive timeout
                "--metrics", "localhost:9090"          # Enable metrics
            ])
            
            time.sleep(8)  # Allow more time for tunnel establishment
            
            print("✅ MAXIMUM performance Cloudflare tunnel active!")
            print("🚀 Configuration: Zero compression, HTTP/2, extended timeouts, connection pooling")
            print("📊 Metrics dashboard: http://localhost:9090/metrics")
            return True
            
        except Exception as e:
            print(f"❌ Cloudflare tunnel failed: {e}")
            return False
    
    def setup_balanced_performance(self):
        """Setup Cloudflare tunnel with balanced performance settings"""
        try:
            print("📦 Setting up balanced performance Cloudflare tunnel...")
            
            # Download cloudflared if not exists
            if not os.path.exists("cloudflared"):
                subprocess.run([
                    "wget", "-q", 
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", 
                    "-O", "cloudflared"
                ], check=True)
                subprocess.run(["chmod", "+x", "cloudflared"], check=True)
            
            # Balanced settings - good performance with stability
            print("🚀 Starting Cloudflare tunnel with balanced optimization...")
            self.tunnel_process = subprocess.Popen([
                "./cloudflared", "tunnel",
                "--url", f"http://localhost:{self.port}",
                "--no-autoupdate",
                "--protocol", "auto",           # Auto-select best protocol
                "--http2-origin",              # HTTP/2 to origin
                "--compression-quality", "1",   # Minimal compression
                "--no-chunked-encoding",       # Better for large files
                "--retries", "3",              # Standard retries
                "--grace-period", "30s",       # Standard grace period
                "--proxy-connect-timeout", "30s",  # Standard timeout
                "--proxy-tls-timeout", "30s",      # Standard TLS timeout
                "--metrics", "localhost:9090"       # Enable metrics
            ])
            
            time.sleep(6)
            
            print("✅ Balanced performance Cloudflare tunnel active!")
            print("🚀 Configuration: Minimal compression, HTTP/2, optimized timeouts")
            print("📊 Metrics dashboard: http://localhost:9090/metrics")
            return True
            
        except Exception as e:
            print(f"❌ Cloudflare tunnel failed: {e}")
            return False
    
    def setup_compatibility_mode(self):
        """Setup Cloudflare tunnel with maximum compatibility"""
        try:
            print("📦 Setting up compatibility mode Cloudflare tunnel...")
            
            # Download cloudflared if not exists
            if not os.path.exists("cloudflared"):
                subprocess.run([
                    "wget", "-q", 
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", 
                    "-O", "cloudflared"
                ], check=True)
                subprocess.run(["chmod", "+x", "cloudflared"], check=True)
            
            # Compatibility settings - works everywhere
            print("🚀 Starting Cloudflare tunnel with compatibility optimization...")
            self.tunnel_process = subprocess.Popen([
                "./cloudflared", "tunnel",
                "--url", f"http://localhost:{self.port}",
                "--no-autoupdate",
                "--protocol", "h2mux",         # Older but more compatible protocol
                "--compression-quality", "2",   # Some compression for compatibility
                "--retries", "2",              # Conservative retries
                "--grace-period", "15s",       # Shorter grace period
                "--metrics", "localhost:9090"   # Enable metrics
            ])
            
            time.sleep(5)
            
            print("✅ Compatibility mode Cloudflare tunnel active!")
            print("🚀 Configuration: Compatible protocol, moderate compression")
            print("📊 Metrics dashboard: http://localhost:9090/metrics")
            return True
            
        except Exception as e:
            print(f"❌ Cloudflare tunnel failed: {e}")
            return False
    
    def get_cloudflare_optimization_tips(self):
        """Return Cloudflare-specific optimization tips"""
        tips = [
            "🎯 Cloudflare Tunnel Optimization Tips:",
            "1. Use --compression-quality 0 for video files (no re-compression needed)",
            "2. Enable --http2-origin for better multiplexing",
            "3. Disable chunked encoding with --no-chunked-encoding for large files",
            "4. Increase timeouts for large file downloads",
            "5. Monitor performance at http://localhost:9090/metrics",
            "6. Use connection pooling with --proxy-keepalive-connections",
            "7. Test different performance modes to find what works best",
            "",
            "📈 Performance Modes Available:",
            "• Maximum: Best for large video downloads (your use case)",
            "• Balanced: Good performance with stability",
            "• Compatibility: Most reliable across all networks"
        ]
        return "\n".join(tips)
    
    def monitor_performance(self):
        """Monitor tunnel performance"""
        print("📊 Cloudflare tunnel metrics available at: http://localhost:9090/metrics")
        print("\n" + self.get_cloudflare_optimization_tips())
        
        print("\n🔍 Key metrics to monitor:")
        print("• cloudflared_tunnel_total_requests: Total requests processed")
        print("• cloudflared_tunnel_request_duration_seconds: Response times")
        print("• cloudflared_tunnel_concurrent_requests_per_tunnel: Active downloads")
        print("• cloudflared_tunnel_response_by_code: Success/error rates")
    
    def cleanup(self):
        """Clean up tunnel processes"""
        if self.tunnel_process:
            print("🧹 Cleaning up Cloudflare tunnel...")
            self.tunnel_process.terminate()
            self.tunnel_process.wait()

def main():
    """Main function to setup optimized Cloudflare tunnels"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pure Cloudflare Tunnel Optimizer for Deep Live Cam")
    parser.add_argument("--port", type=int, default=5000, help="Local port to expose")
    parser.add_argument("--mode", choices=["maximum", "balanced", "compatibility"], 
                       default="maximum", help="Performance optimization mode")
    
    args = parser.parse_args()
    
    optimizer = CloudflareOptimizer(args.port)
    
    print("🎭 Pure Cloudflare Tunnel Optimizer for Deep Live Cam")
    print("=" * 60)
    print(f"🎯 Mode: {args.mode.title()}")
    print(f"📍 Port: {args.port}")
    print("=" * 60)
    
    try:
        if args.mode == "maximum":
            success = optimizer.setup_maximum_performance()
        elif args.mode == "balanced":
            success = optimizer.setup_balanced_performance()
        else:  # compatibility
            success = optimizer.setup_compatibility_mode()
        
        if success:
            optimizer.monitor_performance()
            
            print("\n" + "="*60)
            print("🌟 Cloudflare tunnel is running! Press Ctrl+C to stop")
            print("🔗 Look for your tunnel URL in the output above")
            print("📊 Monitor performance: http://localhost:9090/metrics")
            print("="*60)
            
            # Keep running
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to setup Cloudflare tunnel")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down Cloudflare tunnel...")
    finally:
        optimizer.cleanup()

if __name__ == "__main__":
    main() 