# Copyright (C) 2024, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)
#
# Override u-boot-rockchip.bb to use Rockchip official U-Boot repository
# and configure serial baudrate for RK3506
#
# Note: Rockchip official U-Boot already has rk3506_defconfig support,
# so we only need to override SRC_URI and set baudrate

SRCREV = "${AUTOREV}"
SRCREV_rkbin = "${AUTOREV}"

# 注意：移除原因是因为JeffyCN/mirrors自带的uboot不支持RK3506,所以使用rockchip官方uboot替代
# Remove old SRC_URI from base recipe (JeffyCN/mirrors)
SRC_URI:remove = " \
	git://github.com/JeffyCN/mirrors.git;protocol=https;branch=u-boot; \
	git://github.com/JeffyCN/mirrors.git;protocol=https;branch=rkbin;name=rkbin;destsuffix=rkbin; \
"

# Use Rockchip official U-Boot repository (supports rk3506)
SRC_URI:prepend = " \
	git://github.com/rockchip-linux/u-boot.git;protocol=https;branch=next-dev \
	git://github.com/rockchip-linux/rkbin.git;protocol=https;branch=master;name=rkbin;destsuffix=rkbin \
"

# Set serial baudrate to 115200 in defconfig (before parent's do_configure:prepend runs)
do_configure:prepend() {
	# Set serial baudrate to 115200 in defconfig
	if [ -f "${S}/configs/${UBOOT_MACHINE}" ]; then
		sed -i 's/^CONFIG_BAUDRATE=.*/CONFIG_BAUDRATE=115200/' "${S}/configs/${UBOOT_MACHINE}"
		# If CONFIG_BAUDRATE doesn't exist, add it
		if ! grep -q "^CONFIG_BAUDRATE=" "${S}/configs/${UBOOT_MACHINE}"; then
			echo "CONFIG_BAUDRATE=115200" >> "${S}/configs/${UBOOT_MACHINE}"
		fi
		bbnote "Set CONFIG_BAUDRATE=115200 in ${UBOOT_MACHINE}"
	fi
}

# Set serial baudrate to 115200 in .config after configuration
do_configure:append() {
	if [ -f "${B}/.config" ]; then
		sed -i 's/^CONFIG_BAUDRATE=.*/CONFIG_BAUDRATE=115200/' "${B}/.config"
		if ! grep -q "^CONFIG_BAUDRATE=" "${B}/.config"; then
			echo "CONFIG_BAUDRATE=115200" >> "${B}/.config"
		fi
		# Also check in source directory
		if [ -f "${S}/.config" ]; then
			sed -i 's/^CONFIG_BAUDRATE=.*/CONFIG_BAUDRATE=115200/' "${S}/.config"
			if ! grep -q "^CONFIG_BAUDRATE=" "${S}/.config"; then
				echo "CONFIG_BAUDRATE=115200" >> "${S}/.config"
			fi
		fi
	fi
}

