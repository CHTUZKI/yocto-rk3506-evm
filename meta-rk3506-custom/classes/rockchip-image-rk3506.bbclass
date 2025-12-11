# Copyright (c) 2024, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)
#
# Extended rockchip-image.bbclass for RK3506 with font configuration

inherit rockchip-image

# Configure system fonts for Qt and other applications
# Create symlink /usr/lib/fonts -> /usr/share/fonts for Qt compatibility
# Qt5 is compiled with OE_QMAKE_PATH_QT_FONTS=${libdir}/fonts
# but fonts are installed to standard location /usr/share/fonts
do_post_rootfs:append() {
	if [ -d "${IMAGE_ROOTFS}/usr/share/fonts" ]; then
		echo "Configuring system fonts..."
		
		# Create Qt-compatible font path symlink
		mkdir -p ${IMAGE_ROOTFS}/usr/lib
		ln -rsf ${IMAGE_ROOTFS}/usr/share/fonts ${IMAGE_ROOTFS}/usr/lib/fonts
		
		# Ensure fontconfig cache directory exists
		mkdir -p ${IMAGE_ROOTFS}/var/cache/fontconfig
		chmod 755 ${IMAGE_ROOTFS}/var/cache/fontconfig
		
		# Create font subdirectories if they don't exist
		mkdir -p ${IMAGE_ROOTFS}/usr/share/fonts/truetype
		mkdir -p ${IMAGE_ROOTFS}/usr/share/fonts/opentype
		
		echo "Font paths configured: /usr/lib/fonts -> /usr/share/fonts"
	fi
}

