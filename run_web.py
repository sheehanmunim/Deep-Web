#!/usr/bin/env python3

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import core

if __name__ == '__main__':
    # Add --web flag to command line arguments
    if '--web' not in sys.argv:
        sys.argv.append('--web')
    
    core.run() 