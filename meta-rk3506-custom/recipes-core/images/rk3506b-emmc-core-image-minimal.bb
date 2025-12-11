# Copyright (c) 2025, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)

SUMMARY = "RK3506B Core EVM minimal image (eMMC boot) with display and test utilities"
DESCRIPTION = "A minimal image for RK3506B Core EVM board with eMMC boot, SSH, tools, LVGL and display test utilities"

IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"

IMAGE_LINGUAS = " "

LICENSE = "MIT"

inherit core-image

# Extend core-image-minimal with SSH, tools, LVGL and display test utilities
CORE_IMAGE_EXTRA_INSTALL += " \
    htop \
    net-tools \
    file \
    lvgl \
    lvgl-demo-fb \
    dsi-display-test \
    st7701-panel-test \
    lvgl-test \
    mp4-player \
    pyqt-test \
    gstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    ffmpeg \
    ttf-dejavu-sans \
    ttf-dejavu-sans-mono \
    ttf-dejavu-serif \
    ttf-wqy-zenhei \
    fontconfig \
    fontconfig-utils \
    i2c-tools \
"

# Add SSH server feature (dropbear) and enable root login with empty password
IMAGE_FEATURES += "ssh-server-dropbear debug-tweaks"

IMAGE_ROOTFS_SIZE ?= "8192"
IMAGE_ROOTFS_EXTRA_SPACE:append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 4096", "", d)}"

