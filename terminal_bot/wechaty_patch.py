"""
Patch for Wechaty package to fix dataclass issues with Python 3.11
"""
import os
import sys
import shutil
from pathlib import Path

def patch_wechaty():
    """Patch the Wechaty package to work with Python 3.11"""
    try:
        # Find the site-packages directory in the virtual environment
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
        if sys.platform.startswith('win'):
            site_packages = os.path.join(venv_path, "Lib", "site-packages")
        else:
            # For Linux/Mac
            site_packages = os.path.join(venv_path, "lib", "python3.11", "site-packages")
            # Try alternative paths if the first one doesn't exist
            if not os.path.exists(site_packages):
                for py_ver in ["3.10", "3.9", "3.8", "3.7"]:
                    alt_path = os.path.join(venv_path, "lib", f"python{py_ver}", "site-packages")
                    if os.path.exists(alt_path):
                        site_packages = alt_path
                        break
        
        # Path to the wechaty.py file
        wechaty_file = os.path.join(site_packages, 'wechaty', 'wechaty.py')
        
        if not os.path.exists(wechaty_file):
            print(f"Error: Could not find {wechaty_file}")
            return False
        
        # Create a backup
        backup_file = wechaty_file + '.bak'
        if not os.path.exists(backup_file):
            shutil.copy2(wechaty_file, backup_file)
            print(f"Created backup at {backup_file}")
        
        # Read the file
        with open(wechaty_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the dataclass issue by using default_factory
        content = content.replace(
            "puppet_options: PuppetOptions = PuppetOptions()",
            "puppet_options: PuppetOptions = field(default_factory=lambda: PuppetOptions())"
        )
        
        # Add the import for field
        content = content.replace(
            "from dataclasses import dataclass",
            "from dataclasses import dataclass, field"
        )
        
        # Write the modified content back
        with open(wechaty_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully patched {wechaty_file}")
        return True
    
    except Exception as e:
        print(f"Error patching Wechaty: {e}")
        return False

if __name__ == "__main__":
    if patch_wechaty():
        print("Patch applied successfully!")
    else:
        print("Failed to apply patch.")
        sys.exit(1) 