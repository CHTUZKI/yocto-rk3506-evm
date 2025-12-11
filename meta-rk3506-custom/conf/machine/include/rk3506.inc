# Copyright (c) 2025, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)

require conf/machine/include/arm/armv7a/tune-cortexa7.inc
require conf/machine/include/rockchip-common.inc

SERIAL_CONSOLES = "115200;ttyFIQ0"

RK_SOC_FAMILY := "rk3506"

KBUILD_DEFCONFIG := "rk3506_defconfig"

# Force using u-boot-rockchip instead of standard u-boot
# This overrides the default selection based on version numbers
PREFERRED_PROVIDER_virtual/bootloader := "u-boot-rockchip"
PREFERRED_PROVIDER_u-boot := "u-boot-rockchip"

# Ensure using linux-rockchip (from Rockchip official kernel repository)
# This ensures we use the custom linux-rockchip_6.6.bb recipe which uses
# github.com/rockchip-linux/kernel.git (Rockchip official kernel)
PREFERRED_PROVIDER_virtual/kernel := "linux-rockchip"
