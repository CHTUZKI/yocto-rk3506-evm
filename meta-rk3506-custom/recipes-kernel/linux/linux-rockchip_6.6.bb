# Copyright (C) 2024, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)

require recipes-kernel/linux/linux-yocto.inc

# Include linux-rockchip.inc from meta-rockchip layer
# Use absolute path to ensure BitBake can find it
# ${TOPDIR} points to build directory, so we go up one level to reach meta-rockchip
require ${TOPDIR}/../meta-rockchip/recipes-kernel/linux/linux-rockchip.inc

inherit local-git

SRCREV = "${AUTOREV}"
KBRANCH = "develop-6.6"
SRC_URI = " \
	git://github.com/rockchip-linux/kernel.git;protocol=https;branch=${KBRANCH} \
	file://${THISDIR}/files/cgroups.cfg \
	file://${THISDIR}/files/ethernet.cfg \
	file://${THISDIR}/files/drm.cfg \
	file://${THISDIR}/files/backlight.cfg \
	file://${THISDIR}/files/mpp.cfg \
	file://${THISDIR}/files/rk3506g-core.dts \
	file://${THISDIR}/files/rk3506b-core.dts \
"

LIC_FILES_CHKSUM = "file://COPYING;md5=6bc538ed5bd9a7fc9398086aedcd7e46"

KERNEL_VERSION_SANITY_SKIP = "1"
LINUX_VERSION ?= "6.6"

SRC_URI:append = " ${@bb.utils.contains('IMAGE_FSTYPES', 'ext4', \
		   'file://${THISDIR}/files/ext4.cfg', \
		   '', \
		   d)}"

# Replace device tree file and drivers from meta-rockchip layer
do_configure:append() {
	install -d ${S}/arch/arm/boot/dts/rockchip
	
	# Install device tree based on machine type
	if [ "${MACHINE}" = "rockchip-rk3506g-core-evm" ]; then
		bbnote "Installing device tree file rk3506g-core.dts for RK3506G"
		install -m 0644 ${THISDIR}/files/rk3506g-core.dts \
			${S}/arch/arm/boot/dts/rockchip/rk3506g-core.dts
	elif [ "${MACHINE}" = "rockchip-rk3506b-core-evm" ]; then
		bbnote "Installing device tree file rk3506b-core.dts for RK3506B"
		install -m 0644 ${THISDIR}/files/rk3506b-core.dts \
			${S}/arch/arm/boot/dts/rockchip/rk3506b-core.dts
	fi
}

