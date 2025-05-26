"""
Deep Live Cam - Google Colab Quick Start
Copy and paste this entire script into a Google Colab cell to get started quickly.
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install all required dependencies with GPU support"""
    print("🔧 Installing dependencies...")
    
    # Install system dependencies
    subprocess.run(["apt", "update", "-qq"], check=True)
    subprocess.run(["apt", "install", "-y", "ffmpeg"], check=True)
    
    # Install Python dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok==7.0.5"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "flask==2.3.3"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "flask-cors==4.0.0"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "werkzeug==2.3.7"], check=True)
    
    # Install GPU-optimized packages
    print("🚀 Setting up GPU acceleration...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "onnxruntime", "onnxruntime-gpu"], check=False)
    subprocess.run([sys.executable, "-m", "pip", "install", "onnxruntime-gpu==1.16.3"], check=True)
    
    # Verify GPU setup
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("⚠️  No GPU detected - make sure you're using GPU runtime!")
    except ImportError:
        print("⚠️  Could not verify GPU setup")
    
    print("✅ Dependencies installed!")

def setup_ngrok_and_run():
    """Setup ngrok and run the web interface"""
    
    # Import after installation
    from pyngrok import ngrok
    
    # Configuration
    NGROK_AUTH_TOKEN = "2xbuOdCZEZxqQGx2r77BMgijYAm_5CTUFPLuyB8FWXWCLAmm8"  # Replace with your token
    PORT = 5000
    
    try:
        # Set auth token
        if NGROK_AUTH_TOKEN and NGROK_AUTH_TOKEN != "your_token_here":
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            print("✅ Ngrok auth token set")
        else:
            print("⚠️  No auth token provided - you may hit rate limits")
        
        # Kill any existing tunnels
        ngrok.kill()
        
        # Create tunnel
        public_url = ngrok.connect(PORT)
        print(f"\n🚀 Ngrok tunnel active!")
        print(f"🌐 Access your Deep Live Cam at: {public_url}")
        print(f"📱 Direct link: {public_url}")
        
        # Start a simple Flask app for demonstration
        # In a real setup, you'd import and run your actual Deep Live Cam app here
        from flask import Flask, render_template_string
        
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Deep Live Cam - Ready!</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .status { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .info { background: #cce6ff; border: 1px solid #99ccff; color: #0066cc; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .next-steps { background: #fff3cd; border: 1px solid #ffecb5; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎭 Deep Live Cam - Colab Setup Complete!</h1>
                    
                    <div class="status">
                        <strong>✅ Status:</strong> Ngrok tunnel is active and web interface is running!
                    </div>
                    
                    <div class="info">
                        <strong>🌐 Access URL:</strong> {{ public_url }}<br>
                        <strong>📍 Local Port:</strong> {{ port }}<br>
                        <strong>🖥️ Environment:</strong> Google Colab
                    </div>
                    
                    <div class="next-steps">
                        <strong>📋 Next Steps:</strong><br>
                        1. This is a basic setup confirmation page<br>
                        2. To use the full Deep Live Cam interface, you'll need to:<br>
                        &nbsp;&nbsp;&nbsp;• Clone the actual Deep Live Cam repository<br>
                        &nbsp;&nbsp;&nbsp;• Install all required dependencies<br>
                        &nbsp;&nbsp;&nbsp;• Run the complete web interface<br>
                        3. See the GOOGLE_COLAB_SETUP.md for full instructions
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p>🔗 <a href="https://github.com/your-username/Deep-Live-Cam-New" target="_blank">View GitHub Repository</a></p>
                        <p>📚 <a href="#" onclick="alert('Check the GOOGLE_COLAB_SETUP.md file for complete instructions!')">Full Setup Guide</a></p>
                    </div>
                </div>
            </body>
            </html>
            """, public_url=public_url, port=PORT)
        
        print(f"\n🌟 Starting web server on port {PORT}...")
        print("⚠️  Keep this cell running to maintain the tunnel!")
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=PORT, debug=False)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have a valid ngrok auth token")

def main():
    """Main function to run the complete setup"""
    print("🎭 Deep Live Cam - Google Colab Quick Start")
    print("=" * 50)
    
    try:
        # Step 1: Install dependencies
        install_dependencies()
        
        # Step 2: Setup ngrok and run
        setup_ngrok_and_run()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're using a GPU runtime")
        print("2. Check your ngrok auth token")
        print("3. Restart the runtime and try again")

if __name__ == "__main__":
    main() 