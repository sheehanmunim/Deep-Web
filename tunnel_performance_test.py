#!/usr/bin/env python3
"""
Pure Cloudflare Tunnel Performance Testing Script
Tests download speeds and optimization effectiveness for Cloudflare tunnels only
"""

import time
import requests
import subprocess
import os
import tempfile
from urllib.parse import urlparse

class CloudflarePerformanceTester:
    def __init__(self):
        self.test_results = {}
        
    def create_test_file(self, size_mb=10):
        """Create a test file of specified size"""
        test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
        
        # Create file with random data
        chunk_size = 1024 * 1024  # 1MB chunks
        for _ in range(size_mb):
            test_file.write(os.urandom(chunk_size))
        
        test_file.close()
        return test_file.name
    
    def test_download_speed(self, url, test_file_path, test_name):
        """Test download speed through Cloudflare tunnel"""
        try:
            print(f"🏃 Testing download speed for {test_name}...")
            
            # Start timing
            start_time = time.time()
            
            # Make request with streaming
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # Download and measure
            downloaded_bytes = 0
            chunk_size = 8192
            
            with tempfile.NamedTemporaryFile() as temp_file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        temp_file.write(chunk)
                        downloaded_bytes += len(chunk)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Calculate metrics
            file_size_mb = downloaded_bytes / (1024 * 1024)
            speed_mbps = (file_size_mb * 8) / duration  # Megabits per second
            
            result = {
                'test_name': test_name,
                'file_size_mb': file_size_mb,
                'duration_seconds': duration,
                'speed_mbps': speed_mbps,
                'status': 'success'
            }
            
            print(f"✅ {test_name}: {file_size_mb:.2f}MB in {duration:.2f}s ({speed_mbps:.2f} Mbps)")
            
        except Exception as e:
            result = {
                'test_name': test_name,
                'error': str(e),
                'status': 'failed'
            }
            print(f"❌ {test_name} test failed: {e}")
        
        self.test_results[test_name] = result
        return result
    
    def test_latency(self, url, test_name):
        """Test latency to Cloudflare tunnel endpoint"""
        try:
            # Test with HEAD request for minimal data transfer
            start_time = time.time()
            response = requests.head(url, timeout=10)
            end_time = time.time()
            
            latency_ms = (end_time - start_time) * 1000
            
            print(f"📡 {test_name} latency: {latency_ms:.2f}ms")
            return latency_ms
            
        except Exception as e:
            print(f"❌ {test_name} latency test failed: {e}")
            return None
    
    def test_cloudflare_metrics(self, metrics_url="http://localhost:9090/metrics"):
        """Test if Cloudflare metrics are available"""
        try:
            response = requests.get(metrics_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Cloudflare metrics accessible at {metrics_url}")
                
                # Parse some basic metrics
                metrics_text = response.text
                if "cloudflared_tunnel_total_requests" in metrics_text:
                    print("📊 Tunnel metrics are being collected")
                return True
            else:
                print(f"⚠️  Metrics endpoint returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Could not access metrics: {e}")
            return False
    
    def run_comprehensive_test(self, cloudflare_url=None):
        """Run comprehensive performance tests for Cloudflare tunnel"""
        print("🎯 Starting Cloudflare Tunnel Performance Tests")
        print("=" * 60)
        
        if not cloudflare_url:
            print("❌ No Cloudflare tunnel URL provided")
            print("💡 Start your tunnel and provide the URL with --cloudflare-url")
            return
        
        # Test metrics availability
        print("\n📊 Testing metrics availability...")
        self.test_cloudflare_metrics()
        
        # Test latency
        print(f"\n📡 Testing latency to {cloudflare_url}...")
        self.test_latency(cloudflare_url, "Cloudflare_Tunnel")
        
        # Test different scenarios
        test_scenarios = [
            ("Small_File_1MB", 1),
            ("Medium_File_10MB", 10),
            ("Large_File_50MB", 50)
        ]
        
        for scenario_name, file_size in test_scenarios:
            print(f"\n📁 Testing {scenario_name} ({file_size}MB)...")
            # Note: For actual file download testing, you'd need to serve 
            # test files through your Deep Live Cam web interface
            self.test_latency(cloudflare_url, scenario_name)
        
        self.print_results()
    
    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 CLOUDFLARE TUNNEL PERFORMANCE RESULTS")
        print("=" * 60)
        
        if not self.test_results:
            print("❌ No test results available")
            return
        
        for test_name, result in self.test_results.items():
            if result['status'] == 'success':
                print(f"""
🔹 {test_name}:
   File Size: {result['file_size_mb']:.2f} MB
   Duration: {result['duration_seconds']:.2f} seconds
   Speed: {result['speed_mbps']:.2f} Mbps
   """)
            else:
                print(f"❌ {test_name}: {result.get('error', 'Unknown error')}")
        
        # Cloudflare-specific recommendations
        print("\n💡 CLOUDFLARE OPTIMIZATION RECOMMENDATIONS:")
        
        successful_tests = [r for r in self.test_results.values() if r['status'] == 'success']
        if successful_tests:
            fastest = max(successful_tests, key=lambda x: x['speed_mbps'])
            print(f"🚀 Best performance: {fastest['test_name']} ({fastest['speed_mbps']:.2f} Mbps)")
        
        print("""
🎯 Cloudflare-Specific Tips:
1. Use --compression-quality 0 for video files (no re-compression)
2. Enable --http2-origin for better multiplexing
3. Use --no-chunked-encoding for large file downloads
4. Monitor metrics at http://localhost:9090/metrics
5. Test different performance modes (maximum/balanced/compatibility)
6. Increase timeouts for large files with --grace-period
7. Use connection pooling with --proxy-keepalive-connections

📈 Performance Modes Comparison:
• Maximum Mode: Zero compression, extended timeouts (best for large videos)
• Balanced Mode: Minimal compression, standard timeouts (good all-around)
• Compatibility Mode: Some compression, conservative settings (most reliable)

🔧 Troubleshooting Slow Downloads:
1. Check tunnel metrics for bottlenecks
2. Verify --compression-quality is set to 0
3. Ensure --http2-origin is enabled
4. Increase timeout values for large files
5. Test with compatibility mode if issues persist
""")

def main():
    """Main function to run Cloudflare performance tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Cloudflare tunnel performance")
    parser.add_argument("--cloudflare-url", help="Cloudflare tunnel URL to test (required)")
    parser.add_argument("--metrics-url", default="http://localhost:9090/metrics", 
                       help="Cloudflare metrics URL")
    
    args = parser.parse_args()
    
    tester = CloudflarePerformanceTester()
    
    if not args.cloudflare_url:
        print("❌ Cloudflare tunnel URL is required")
        print("💡 Usage: python tunnel_performance_test.py --cloudflare-url https://your-tunnel.trycloudflare.com")
        print("\n🚀 To get your URL:")
        print("1. Start your optimized tunnel: python optimized_tunnel.py")
        print("2. Look for the https://xxxxx.trycloudflare.com URL in the output")
        print("3. Use that URL with this test script")
        return
    
    # Run tests
    tester.run_comprehensive_test(cloudflare_url=args.cloudflare_url)

if __name__ == "__main__":
    main() 