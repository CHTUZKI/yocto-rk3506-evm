#!/usr/bin/env python3
"""Font Diagnostic Test for PyQt5 on RK3506"""

import sys
import os
import stat
from pathlib import Path

def check_path(path, description):
    """Check if path exists and print details"""
    print(f"\n{description}:")
    if os.path.exists(path):
        print(f"  ✓ Path exists: {path}")
        if os.path.islink(path):
            real_path = os.path.realpath(path)
            print(f"  → Is symlink, points to: {real_path}")
            if os.path.exists(real_path):
                print(f"  ✓ Target exists: {real_path}")
            else:
                print(f"  ✗ Target does NOT exist: {real_path}")
        if os.path.isdir(path):
            print(f"  → Is directory")
            try:
                files = os.listdir(path)
                print(f"  → Contains {len(files)} items")
                if len(files) > 0:
                    print(f"  → First 5 items: {files[:5]}")
            except Exception as e:
                print(f"  ✗ Cannot list directory: {e}")
        elif os.path.isfile(path):
            print(f"  → Is file")
            try:
                size = os.path.getsize(path)
                print(f"  → Size: {size} bytes")
            except:
                pass
        # Check permissions
        try:
            mode = os.stat(path).st_mode
            perms = stat.filemode(mode)
            print(f"  → Permissions: {perms}")
        except Exception as e:
            print(f"  ✗ Cannot check permissions: {e}")
    else:
        print(f"  ✗ Path does NOT exist: {path}")

def list_font_files(directory):
    """List all font files in directory"""
    font_extensions = ['.ttf', '.otf', '.ttc', '.pcf', '.bdf']
    font_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in font_extensions):
                    full_path = os.path.join(root, file)
                    font_files.append(full_path)
    except Exception as e:
        print(f"  ✗ Error walking directory: {e}")
    return font_files

print("="*60)
print("PyQt5 Font Diagnostic Test")
print("="*60)

print("\n" + "="*60)
print("Step 1: Environment Variables")
print("="*60)
font_env_vars = ['QT_QPA_FONTDIR', 'QT_QPA_PLATFORM', 'FONTCONFIG_FILE', 
                 'FONTCONFIG_PATH', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR']
for var in font_env_vars:
    value = os.environ.get(var, 'Not set')
    print(f"{var}: {value}")

print("\n" + "="*60)
print("Step 2: Font Directory Paths Check")
print("="*60)
font_paths = [
    '/usr/lib/fonts',
    '/usr/share/fonts',
    '/usr/share/fonts/truetype',
    '/usr/share/fonts/opentype',
    '/usr/share/fonts/TTF',
    '/usr/share/fonts/OTF',
    '/usr/lib/fonts/truetype',
    '/usr/lib/fonts/opentype',
]

for path in font_paths:
    check_path(path, f"Checking {path}")

print("\n" + "="*60)
print("Step 3: Font Files Search")
print("="*60)
for path in font_paths:
    if os.path.exists(path) and os.path.isdir(path):
        fonts = list_font_files(path)
        print(f"\n{path}:")
        if fonts:
            print(f"  ✓ Found {len(fonts)} font file(s)")
            for font in fonts[:10]:  # Show first 10
                print(f"    - {font}")
            if len(fonts) > 10:
                print(f"    ... and {len(fonts) - 10} more")
        else:
            print(f"  ✗ No font files found")

print("\n" + "="*60)
print("Step 4: Testing PyQt5 Import")
print("="*60)
try:
    from PyQt5 import QtCore, QtGui
    print("✓ PyQt5 imported successfully")
    print(f"  Qt version: {QtCore.QT_VERSION_STR}")
    print(f"  PyQt version: {QtCore.PYQT_VERSION_STR}")
except Exception as e:
    print(f"✗ ERROR importing PyQt5: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("Step 5: Qt Font Database")
print("="*60)

# Set QT_QPA_PLATFORM if not already set (use offscreen for testing)
if 'QT_QPA_PLATFORM' not in os.environ:
    # Try to find available platform plugins
    if os.path.exists('/usr/lib/plugins/platforms/libqeglfs.so'):
        os.environ['QT_QPA_PLATFORM'] = 'eglfs'
        print("Setting QT_QPA_PLATFORM=eglfs for font testing")
    elif os.path.exists('/usr/lib/plugins/platforms/libqoffscreen.so'):
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        print("Setting QT_QPA_PLATFORM=offscreen for font testing")
    else:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        print("Setting QT_QPA_PLATFORM=offscreen (default for testing)")

# Set XDG_RUNTIME_DIR if not set
if 'XDG_RUNTIME_DIR' not in os.environ:
    os.environ['XDG_RUNTIME_DIR'] = '/tmp'
    print("Setting XDG_RUNTIME_DIR=/tmp")

try:
    app = QtGui.QGuiApplication(sys.argv) if not QtGui.QGuiApplication.instance() else QtGui.QGuiApplication.instance()
    
    font_db = QtGui.QFontDatabase()
    families = font_db.families()
    
    print(f"✓ Font database initialized")
    print(f"  Total font families found: {len(families)}")
    
    if len(families) == 0:
        print("  ✗ WARNING: No fonts found in Qt font database!")
        print("  This is likely the root cause of font display issues.")
    else:
        print(f"\n  Available font families (first 20):")
        for i, family in enumerate(sorted(families)[:20]):
            print(f"    {i+1}. {family}")
        if len(families) > 20:
            print(f"    ... and {len(families) - 20} more")
        
        # Check for common fonts
        common_fonts = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Sans', 'Sans Serif', 'Monospace']
        print(f"\n  Checking for common fonts:")
        for font_name in common_fonts:
            if font_name in families:
                print(f"    ✓ {font_name} - Available")
            else:
                print(f"    ✗ {font_name} - NOT found")
    
    # Test default font
    print(f"\n  Testing default font:")
    default_font = QtGui.QFont()
    print(f"    Family: {default_font.family()}")
    print(f"    Point size: {default_font.pointSize()}")
    print(f"    Pixel size: {default_font.pixelSize()}")
    
    # Test if we can create a font
    test_font = QtGui.QFont("DejaVu Sans", 12)
    if test_font.exactMatch():
        print(f"    ✓ Can create 'DejaVu Sans' font")
    else:
        print(f"    ✗ Cannot create 'DejaVu Sans' font (fallback: {test_font.family()})")
    
    # Check font paths Qt is using
    print(f"\n  Qt font paths:")
    font_paths_qt = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.FontsLocation)
    if font_paths_qt:
        for path in font_paths_qt:
            print(f"    - {path}")
            check_path(path, f"      Qt font path")
    else:
        print(f"    ✗ No font paths configured in Qt")
        
except Exception as e:
    print(f"✗ ERROR testing font database: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Step 6: Fontconfig Check (if available)")
print("="*60)
try:
    import subprocess
    result = subprocess.run(['fc-list'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        fonts = result.stdout.strip().split('\n')
        print(f"✓ fontconfig found")
        print(f"  Total fonts: {len(fonts)}")
        if fonts and fonts[0]:
            print(f"  First few fonts:")
            for font in fonts[:5]:
                print(f"    - {font}")
        else:
            print(f"  ✗ No fonts found via fontconfig")
    else:
        print(f"✗ fontconfig command failed: {result.stderr}")
except FileNotFoundError:
    print("✗ fontconfig (fc-list) not available")
except Exception as e:
    print(f"✗ Error checking fontconfig: {e}")

print("\n" + "="*60)
print("Step 7: Recommendations")
print("="*60)
print("Based on the diagnostics above:")
print("1. Check if /usr/lib/fonts or /usr/share/fonts exists and contains font files")
print("2. Verify the symlink /usr/lib/fonts -> /usr/share/fonts is correct")
print("3. Ensure font files have proper permissions (readable)")
print("4. Check if Qt can access the font directories")
print("5. If no fonts found, install font packages (e.g., ttf-dejavu, ttf-liberation)")

print("\n" + "="*60)
print("Diagnostic Complete")
print("="*60)

