#!/bin/sh
# Video system diagnostic script for RK3506
# Checks GStreamer, DRM, and video playback capabilities

echo "=========================================="
echo "  RK3506 Video System Check"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}[OK]${NC} $1"
}

check_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check GStreamer
echo "1. Checking GStreamer installation..."
if command -v gst-launch-1.0 >/dev/null 2>&1; then
    GST_VERSION=$(gst-launch-1.0 --version 2>&1 | head -n1)
    check_pass "GStreamer installed: $GST_VERSION"
else
    check_fail "GStreamer not found"
fi

# Check GStreamer plugins
echo ""
echo "2. Checking GStreamer plugins..."
if gst-inspect-1.0 filesrc >/dev/null 2>&1; then
    check_pass "filesrc plugin available"
else
    check_fail "filesrc plugin not found"
fi

if gst-inspect-1.0 libav >/dev/null 2>&1; then
    check_pass "libav plugin available (software decoder)"
else
    check_warn "libav plugin not found (software decoder)"
fi

# Check DRM
echo ""
echo "3. Checking DRM devices..."
if [ -c /dev/dri/card0 ]; then
    check_pass "/dev/dri/card0 exists"
    if [ -r /dev/dri/card0 ] && [ -w /dev/dri/card0 ]; then
        check_pass "/dev/dri/card0 permissions OK"
    else
        check_warn "/dev/dri/card0 permission issue"
    fi
else
    check_warn "/dev/dri/card0 not found"
fi

# Check video group
echo ""
echo "4. Checking user permissions..."
if groups | grep -q video; then
    check_pass "User is in 'video' group"
else
    check_warn "User is NOT in 'video' group"
fi

# Check test video file
echo ""
echo "5. Checking test video file..."
VIDEO_FILE="/usr/share/mp4-player/videoplayback.mp4"
if [ -f "$VIDEO_FILE" ]; then
    check_pass "Test video found: $VIDEO_FILE"
    VIDEO_SIZE=$(du -h "$VIDEO_FILE" | cut -f1)
    echo "   Size: $VIDEO_SIZE"
else
    check_warn "Test video not found: $VIDEO_FILE"
fi

# Check mp4-player binary
echo ""
echo "6. Checking mp4-player binary..."
if command -v mp4-player >/dev/null 2>&1; then
    check_pass "mp4-player binary found"
else
    check_fail "mp4-player binary not found"
fi

echo ""
echo "=========================================="
echo "  Check Complete"
echo "=========================================="

