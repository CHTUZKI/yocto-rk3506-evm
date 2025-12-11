# Copyright (c) 2024, Rockchip Electronics Co., Ltd
# Released under the MIT license (see COPYING.MIT for the terms)
#
# Override rockchip-common.inc to prefer kernel 6.6 instead of 6.1

# Prefer using Rockchip BSP kernel 6.6
PREFERRED_VERSION_linux-rockchip ?= "6.6%"
LINUXLIBCVERSION ?= "6.6-custom%"

