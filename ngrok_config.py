"""
Ngrok Configuration File
Customize these settings for your ngrok integration
"""

# Ngrok Authentication Token
# Get your free token from: https://dashboard.ngrok.com/get-started/your-authtoken
NGROK_AUTH_TOKEN = "2xbuOdCZEZxqQGx2r77BMgijYAm_5CTUFPLuyB8FWXWCLAmm8"

# Flask Application Settings
FLASK_HOST = "0.0.0.0"  # Listen on all interfaces
FLASK_PORT = 5000       # Port to run Flask on
FLASK_DEBUG = False     # Set to True for development

# Ngrok Tunnel Settings
NGROK_REGION = "us"     # Available: us, eu, ap, au, sa, jp, in
NGROK_SUBDOMAIN = None  # Custom subdomain (requires paid plan)
NGROK_AUTH_ENABLED = True  # Enable HTTP basic auth (requires paid plan)

# Security Settings (for paid plans)
NGROK_USERNAME = None   # HTTP basic auth username
NGROK_PASSWORD = None   # HTTP basic auth password

# Advanced Ngrok Options
NGROK_OPTIONS = {
    "bind_tls": True,           # Enable HTTPS
    "inspect": True,            # Enable ngrok inspection
    "remote_addr": None,        # Reserved TCP address (paid feature)
}

# Environment Detection
COLAB_ENVIRONMENT = False       # Set to True if running in Google Colab
LOCAL_DEVELOPMENT = True       # Set to False for production

# File Upload Settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}

# Processing Settings
DEFAULT_SETTINGS = {
    'keep_fps': True,
    'keep_audio': True,
    'keep_frames': False,
    'many_faces': False,
    'map_faces': False,
    'color_correction': False,
    'nsfw_filter': True,
    'face_enhancer': True,
}

# Display Messages
STARTUP_MESSAGE = """
🎭 Deep Live Cam with Ngrok Integration
==========================================
Ready to create amazing face swaps!
"""

SUCCESS_MESSAGE = """
🚀 Server started successfully!
Access your Deep Live Cam web interface using the ngrok URL above.
Keep this window open to maintain the tunnel.
"""

def get_config():
    """
    Get the current configuration as a dictionary
    """
    return {
        'ngrok_auth_token': NGROK_AUTH_TOKEN,
        'flask_host': FLASK_HOST,
        'flask_port': FLASK_PORT,
        'flask_debug': FLASK_DEBUG,
        'ngrok_region': NGROK_REGION,
        'ngrok_subdomain': NGROK_SUBDOMAIN,
        'ngrok_auth_enabled': NGROK_AUTH_ENABLED,
        'ngrok_username': NGROK_USERNAME,
        'ngrok_password': NGROK_PASSWORD,
        'ngrok_options': NGROK_OPTIONS,
        'colab_environment': COLAB_ENVIRONMENT,
        'local_development': LOCAL_DEVELOPMENT,
        'max_file_size': MAX_FILE_SIZE,
        'allowed_extensions': ALLOWED_EXTENSIONS,
        'default_settings': DEFAULT_SETTINGS,
    }

def validate_config():
    """
    Validate the configuration settings
    """
    errors = []
    
    if not NGROK_AUTH_TOKEN or NGROK_AUTH_TOKEN == "your_token_here":
        errors.append("⚠️  No ngrok auth token set. You may hit rate limits.")
    
    if FLASK_PORT < 1024 or FLASK_PORT > 65535:
        errors.append("❌ Invalid Flask port. Must be between 1024-65535.")
    
    if NGROK_SUBDOMAIN and not NGROK_AUTH_TOKEN:
        errors.append("❌ Custom subdomain requires ngrok auth token.")
    
    if NGROK_AUTH_ENABLED and (not NGROK_USERNAME or not NGROK_PASSWORD):
        errors.append("❌ HTTP auth enabled but username/password not set.")
    
    return errors

def print_config_info():
    """
    Print configuration information
    """
    print("🔧 Configuration Info:")
    print(f"   Flask Port: {FLASK_PORT}")
    print(f"   Ngrok Region: {NGROK_REGION}")
    print(f"   Auth Token Set: {'Yes' if NGROK_AUTH_TOKEN else 'No'}")
    print(f"   Custom Subdomain: {NGROK_SUBDOMAIN or 'None'}")
    print(f"   Environment: {'Google Colab' if COLAB_ENVIRONMENT else 'Local'}")
    
    # Validate and show any issues
    errors = validate_config()
    if errors:
        print("\n⚠️  Configuration Issues:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ Configuration looks good!")

if __name__ == "__main__":
    print_config_info() 