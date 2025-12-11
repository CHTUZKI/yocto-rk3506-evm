# Copyright (C) 2024, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)
#
# Override linux-rockchip_6.1.bb to use Rockchip BSP kernel with custom device tree

# Disable this recipe - using 6.6 instead
COMPATIBLE_MACHINE = "^$"

SRCREV = "${AUTOREV}"
KBRANCH = "develop-6.1"
SRC_URI:prepend = " \
	git://github.com/rockchip-linux/kernel.git;protocol=https;branch=${KBRANCH} \
	file://${THISDIR}/files/ethernet.cfg \
	file://${THISDIR}/files/drm.cfg \
	file://${THISDIR}/files/rk3506g-core.dts \
"

# Replace device tree file from meta-rockchip layer
do_configure:append() {
	bbnote "Replacing device tree file rk3506g-core.dts from meta-rockchip layer"
	install -d ${S}/arch/arm/boot/dts/rockchip
	install -m 0644 ${THISDIR}/files/rk3506g-core.dts \
		${S}/arch/arm/boot/dts/rockchip/rk3506g-core.dts
}

