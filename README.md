# RK3506 Yocto 项目

基于 Yocto Project 的 RK3506 嵌入式 Linux 开发环境。

## 功能展示

功能展示图片请查看 `图片/` 文件夹。

## 硬件参数

**RK3506G**

| 项目 | 参数 |
|------|------|
| 处理器 | Rockchip RK3506G2 (3x Cortex-A7) |
| 主频 | 1.5GHz |
| 内存 | 128MB DDR3L 内置|
| 存储 | SD卡启动 |
| 显示接口 | MIPI DSI 2 Lane (1280x1280@60Hz), RGB888 (1280x1280@60Hz) |

## 项目结构

本项目采用标准的 Yocto 项目组织方式：

```
rk3506-new/
├── poky/                  # Yocto 官方发行版核心层 (scarthgap)
├── meta-openembedded/     # OpenEmbedded 元层 (scarthgap)
├── meta-qt5/              # Qt5 支持层 (scarthgap)
├── meta-rockchip/         # Rockchip BSP 层 (scarthgap) - 官方版本
├── meta-rk3506-custom/    # RK3506 定制层 - 包含所有自定义改动
└── build/                 # BitBake 构建目录
```

### 层说明

- **meta-rockchip**: 官方 Rockchip BSP 层，提供基础的 Rockchip SoC 支持
- **meta-rk3506-custom**: 本项目定制层，包含所有针对 RK3506 的自定义改动：
  - RK3506 机器配置和设备树
  - 内核 6.6 版本支持
  - 显示测试应用
  - 触摸屏驱动补丁
  - 其他硬件相关配置

更多信息请查看 `meta-rockchip/README.md`。

## 显示测试程序

在 `meta-rk3506-custom/recipes-extended/rk3506-test-apps` 目录下提供了多个显示测试工具：

| 程序 | 说明 |
|------|------|
| `dsi-display-test` | 基础 DRM 显示测试，循环显示不同颜色 ✅|
| `st7701-panel-test` | 面板测试程序（通过设备树写入面板初始化序列） ✅|
| `lvgl-test` | LVGL 轻量级图形库演示 ✅|
| `mp4-player` | GStreamer 视频播放器（软解码） ✅|
| `pyqt-test` | PyQt5 图形界面测试程序 ✅ |

**注意**: RK3506G2 无硬件视频解码器，视频播放使用软件解码。

## 已知问题

- ⚠️ **串口波特率**: 当前为 1.5M (1500000)，U-Boot 已配置为 115200，但内核串口仍为 1.5M
- ⚠️ **设备树**: 仅完善了必要的基础设备树配置


## 串口配置

使用串口调试工具连接设备时，必须设置波特率为 **1500000**：

```bash
# screen
screen /dev/ttyUSB0 1500000

# minicom
minicom -D /dev/ttyUSB0 -b 1500000
```

## 快速开始

### 初始化构建环境

```bash
cd /home/xuning/rk3506-new
source poky/oe-init-build-env build
```

### 构建镜像

```bash
bitbake rk3506g-sd-core-image-minimal
```

构建完成后，镜像文件位于 `build/tmp/deploy/images/rockchip-rk3506g-core-evm/` 目录下。

详细构建说明请参考 `硬件相关/rk3506g构建命令.txt`。

**注意**: 构建命令文件中的路径需要更新为 `/home/xuning/rk3506-new/poky`。

## 登录信息

- **用户名**：`root`
- **密码**：无（直接回车即可）

## 致谢

特别感谢：

- [**Yocto Project**](https://www.yoctoproject.org/) 团队和社区，为嵌入式 Linux 开发提供了强大而灵活的构建系统和工具链
- **Jeffy Chen** (jeffy.chen@rock-chips.com) 维护的 [meta-rockchip](https://github.com/JeffyCN/meta-rockchip) BSP 层，为 Rockchip SoC 开发板提供了优秀的 Yocto 支持

## License

本项目遵循 MIT 许可证。

## 免责声明

**重要提示：**

本 Yocto 项目为实验性开发环境，主要用于 RK3506 平台的功能验证和技术探索。当前状态说明：

- ⚠️ 本项目**仅用于功能测试和开发调试**，未经充分的生产环境验证
- ⚠️ 不保证系统的稳定性、安全性和长期可靠性
- ⚠️ 是否具备实际生产部署能力需要根据具体应用场景进行全面测试和评估
- ⚠️ 使用本项目所产生的任何问题、损失或后果，作者不承担任何责任

**建议：**

- 在生产环境部署前，请进行充分的功能测试、压力测试和稳定性测试
- 根据实际需求完善设备树配置、驱动程序和系统安全设置
- 建议由专业团队评估后再决定是否用于商业产品

**本项目按"原样"提供，不附带任何明示或暗示的保证。使用者需自行承担使用风险。**
