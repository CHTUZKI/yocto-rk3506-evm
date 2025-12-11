#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 触摸屏响应测试程序
极简版本，用于测试触摸屏响应速度
"""

import sys
import os
import time
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase


class TouchTestWindow(QMainWindow):
    def __init__(self, logger=None):
        super().__init__()
        self.touch_count = 0
        self.last_touch_time = 0
        self.logger = logger or logging.getLogger(__name__)
        self.status_timer = None  # 用于管理状态恢复定时器
        self.log_counter = 0  # 日志计数器，用于减少日志频率
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Touch Response Test")
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(layout)
        
        # 标题
        title = QLabel("触摸屏响应测试")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 触摸计数
        self.count_label = QLabel("触摸次数: 0")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("font-size: 20px; color: #3498db;")
        layout.addWidget(self.count_label)
        
        # 响应时间显示
        self.time_label = QLabel("响应时间: -- ms")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 18px; color: #27ae60;")
        layout.addWidget(self.time_label)
        
        # 坐标显示
        self.coord_label = QLabel("坐标: (0, 0)")
        self.coord_label.setAlignment(Qt.AlignCenter)
        self.coord_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        layout.addWidget(self.coord_label)
        
        # 测试按钮
        self.test_button = QPushButton("点击这里测试")
        self.test_button.setMinimumHeight(80)
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        self.test_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.test_button)
        
        # 状态标签
        self.status_label = QLabel("等待触摸...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #95a5a6;")
        layout.addWidget(self.status_label)
        
        # 添加弹性空间
        layout.addStretch()
        
        # 说明文字
        info = QLabel("触摸屏幕任意位置测试响应速度\n按ESC键退出")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 14px; color: #bdc3c7;")
        layout.addWidget(info)
        
    def touchEvent(self, event):
        """处理触摸事件（优先使用）"""
        # 先让事件传递给子控件（如按钮），确保按钮的pressed状态能立即显示
        result = super().touchEvent(event)
        
        # 获取触摸点信息
        touch_points = event.touchPoints()
        if touch_points:
            touch_point = touch_points[0]
            x = int(touch_point.pos().x())
            y = int(touch_point.pos().y())
            
            # 直接处理，不使用定时器，减少内存占用
            self._handle_touch(x, y)
        
        return result
    
    def _handle_touch(self, x, y):
        """处理触摸事件（直接处理，减少延迟）"""
        touch_time = time.time() * 1000
        
        # 计算响应时间
        if self.last_touch_time > 0:
            response_time = touch_time - self.last_touch_time
        else:
            response_time = 0
        
        self.last_touch_time = touch_time
        self.touch_count += 1
        
        # 减少日志频率：每10次触摸记录一次，或响应时间>100ms时记录
        self.log_counter += 1
        if self.log_counter >= 10 or response_time > 100:
            self.logger.info(f"触摸事件 #{self.touch_count}: 坐标=({x}, {y}), 响应时间={response_time:.1f}ms")
            self.log_counter = 0
        
        # 立即更新UI显示（不使用异步，减少内存占用）
        self._update_touch_display(x, y, response_time)
    
    def _update_touch_display(self, x, y, response_time):
        """更新触摸显示（直接更新，立即生效）"""
        # 立即更新UI，不使用异步
        self.count_label.setText(f"触摸次数: {self.touch_count}")
        self.coord_label.setText(f"坐标: ({x}, {y})")
        self.time_label.setText(f"响应时间: {response_time:.1f} ms" if response_time > 0 else "响应时间: -- ms")
        self.status_label.setText(f"触摸检测到! (响应时间: {response_time:.1f} ms)" if response_time > 0 else "首次触摸")
        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        
        # 取消之前的定时器（避免内存泄漏）
        if self.status_timer:
            self.status_timer.stop()
            self.status_timer.deleteLater()
        
        # 创建新的定时器恢复状态（使用对象方法而不是lambda，减少内存占用）
        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)
        self.status_timer.timeout.connect(self._reset_status)
        self.status_timer.start(500)
    
    def _reset_status(self):
        """恢复状态标签（定时器回调）"""
        self.status_label.setText("等待触摸...")
        self.status_label.setStyleSheet("font-size: 16px; color: #95a5a6;")
        if self.status_timer:
            self.status_timer.deleteLater()
            self.status_timer = None
    
    def mousePressEvent(self, event):
        """处理鼠标/触摸按下事件（备用）"""
        # 先让事件传递给子控件（如按钮），确保按钮的pressed状态能立即显示
        super().mousePressEvent(event)
        
        # 获取位置信息
        x = int(event.pos().x())
        y = int(event.pos().y())
        
        # 直接处理，不使用定时器
        self._handle_touch(x, y)
    
    def on_button_clicked(self):
        """按钮点击事件"""
        self.touch_count += 1
        if self.log_counter == 0:  # 只在需要记录日志时记录
            self.logger.info(f"按钮点击事件: 触摸次数={self.touch_count}")
        self.count_label.setText(f"触摸次数: {self.touch_count}")
        self.status_label.setText("按钮被点击!")
        self.status_label.setStyleSheet("font-size: 16px; color: #27ae60; font-weight: bold;")
        
        # 取消之前的定时器
        if self.status_timer:
            self.status_timer.stop()
            self.status_timer.deleteLater()
        
        # 使用对象方法而不是lambda
        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)
        self.status_timer.timeout.connect(self._reset_status)
        self.status_timer.start(500)
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
    

def setup_logging():
    """设置日志系统，日志文件保存在程序所在目录"""
    # 优先使用 /home/root/ 目录
    log_dir = '/home/root'
    program_dir = log_dir
    
    # 如果 /home/root/ 不存在，尝试获取程序所在目录
    if not os.path.exists(log_dir):
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序
            program_dir = os.path.dirname(sys.executable)
        else:
            # 如果是脚本
            program_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = program_dir
    
    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建日志文件名（带时间戳）
    log_filename = os.path.join(log_dir, f'pyqt-touch-test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # 同时输出到控制台
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"日志系统初始化完成，日志文件: {log_filename}")
    logger.info(f"程序目录: {program_dir}")
    
    return logger

def setup_font_paths():
    """设置字体路径，确保 Qt 能找到字体"""
    # 创建 /usr/lib/fonts 到 /usr/share/fonts 的符号链接（如果不存在）
    font_link = '/usr/lib/fonts'
    font_target = '/usr/share/fonts'
    
    if os.path.exists(font_target) and not os.path.exists(font_link):
        try:
            os.makedirs('/usr/lib', exist_ok=True)
            os.symlink(font_target, font_link)
            print(f"Created font symlink: {font_link} -> {font_target}")
        except Exception as e:
            print(f"Warning: Failed to create font symlink: {e}")
    
    # 确保字体目录存在
    if os.path.exists(font_target):
        print(f"Font directory exists: {font_target}")
        # 列出可用的字体文件
        font_files = []
        for root, dirs, files in os.walk(font_target):
            for file in files:
                if file.endswith(('.ttf', '.otf', '.ttc')):
                    font_files.append(os.path.join(root, file))
        if font_files:
            print(f"Found {len(font_files)} font files")
        else:
            print("Warning: No font files found in font directory")
    else:
        print(f"Warning: Font directory does not exist: {font_target}")

def find_touchscreen_device():
    """自动检测触摸屏设备"""
    # 首先尝试 udev 符号链接
    if os.path.exists('/dev/input/touchscreen0') and os.access('/dev/input/touchscreen0', os.R_OK):
        return '/dev/input/touchscreen0'
    
    # 扫描所有 event 设备，通过设备名称识别触摸屏
    for i in range(10):
        event_path = f'/dev/input/event{i}'
        if not os.path.exists(event_path) or not os.access(event_path, os.R_OK):
            continue
        
        # 通过 /sys/class/input/ 检查设备名称
        try:
            sys_name_path = f'/sys/class/input/event{i}/device/name'
            if os.path.exists(sys_name_path):
                with open(sys_name_path, 'r') as f:
                    name = f.read().strip().lower()
                    # 检查设备名称中是否包含触摸屏相关关键词
                    if any(keyword in name for keyword in ['touch', 'ts', 'cst', 'hyn']):
                        print(f"Found touchscreen: {event_path} (name: {name})")
                        return event_path
        except Exception as e:
            continue
    
    # 如果没找到，尝试常见的 event0（通常触摸屏是 event0）
    if os.path.exists('/dev/input/event0') and os.access('/dev/input/event0', os.R_OK):
        print("Using /dev/input/event0 as fallback (may not be touchscreen)")
        return '/dev/input/event0'
    
    return None

def main():
    """主函数"""
    # 初始化日志系统（必须在最开始）
    logger = setup_logging()
    
    logger.info("=" * 60)
    logger.info("PyQt5 Touch Response Test")
    logger.info("=" * 60)
    print("=" * 60)
    print("PyQt5 Touch Response Test")
    print("=" * 60)
    
    # 设置字体路径（必须在创建 QApplication 之前）
    setup_font_paths()
    logger.info("字体路径设置完成")
    
    # 设置QPA平台
    if 'QT_QPA_PLATFORM' not in os.environ:
        if os.path.exists('/usr/lib/plugins/platforms/libqeglfs.so'):
            os.environ['QT_QPA_PLATFORM'] = 'eglfs'
            logger.info("使用平台: eglfs")
            print("Using platform: eglfs")
        elif os.path.exists('/usr/lib/plugins/platforms/libqlinuxfb.so'):
            os.environ['QT_QPA_PLATFORM'] = 'linuxfb'
            logger.info("使用平台: linuxfb")
            print("Using platform: linuxfb")
        else:
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
            logger.warning("使用平台: offscreen")
            print("Warning: Using platform: offscreen")
    
    # 配置触摸屏输入设备（关键优化）
    if 'QT_QPA_GENERIC_PLUGINS' not in os.environ:
        touchscreen_device = find_touchscreen_device()
        if touchscreen_device:
            # 如果是符号链接，解析实际路径
            if os.path.islink(touchscreen_device):
                real_path = os.readlink(touchscreen_device)
                if not os.path.isabs(real_path):
                    # 相对路径，需要转换为绝对路径
                    real_path = os.path.join(os.path.dirname(touchscreen_device), real_path)
                touchscreen_device = os.path.realpath(touchscreen_device)
                print(f"Resolved touchscreen device: {touchscreen_device}")
            
            # 使用 evdevtouch 插件，指定触摸设备
            # 格式: evdevtouch:/dev/input/event0
            os.environ['QT_QPA_GENERIC_PLUGINS'] = f'evdevtouch:{touchscreen_device}'
            logger.info(f"触摸屏设备已配置: {touchscreen_device}")
            print(f"Touchscreen device configured: {touchscreen_device}")
        else:
            os.environ['QT_QPA_GENERIC_PLUGINS'] = 'evdevtouch'
            logger.warning("未找到触摸屏设备，使用自动检测")
            print("Warning: Touchscreen device not found, using auto-detection")
    
    # 设置触摸屏环境变量（额外配置）
    touchscreen_device = find_touchscreen_device()
    if touchscreen_device:
        # 解析实际设备路径
        if os.path.islink(touchscreen_device):
            touchscreen_device = os.path.realpath(touchscreen_device)
        os.environ['QT_QPA_EVDEV_TOUCHSCREEN_PARAMETERS'] = touchscreen_device
        print(f"Additional touchscreen config: {touchscreen_device}")
    
    # 设置 XDG_RUNTIME_DIR
    if 'XDG_RUNTIME_DIR' not in os.environ:
        os.environ['XDG_RUNTIME_DIR'] = '/tmp'
    
    logger.info("启动应用程序...")
    print("\nStarting application...")
    print("Touch the screen to test response speed")
    print("Press ESC to exit\n")
    
    app = QApplication(sys.argv)
    
    # 加载系统字体到 Qt 字体数据库
    font_db = QFontDatabase()
    font_dirs = ['/usr/share/fonts', '/usr/lib/fonts']
    font_count = 0
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.endswith(('.ttf', '.otf', '.ttc')):
                        font_path = os.path.join(root, file)
                        try:
                            font_id = font_db.addApplicationFont(font_path)
                            if font_id >= 0:
                                families = font_db.applicationFontFamilies(font_id)
                                if families:
                                    font_count += 1
                                    if font_count <= 5:  # 只记录前5个字体
                                        logger.debug(f"加载字体: {families[0]} from {file}")
                                    print(f"Loaded font: {families[0]} from {file}")
                        except Exception as e:
                            logger.error(f"加载字体失败 {file}: {e}")
    
    logger.info(f"共加载 {font_count} 个字体")
    
    # 创建并显示窗口
    window = TouchTestWindow(logger=logger)
    # 启用触摸事件（关键设置）
    window.setAttribute(Qt.WA_AcceptTouchEvents, True)
    # 设置窗口标志，确保能接收所有输入事件
    window.setAttribute(Qt.WA_NoSystemBackground, False)
    # 启用鼠标跟踪（有助于触摸事件）
    window.setMouseTracking(True)
    
    logger.info(f"窗口属性设置: WA_AcceptTouchEvents={window.testAttribute(Qt.WA_AcceptTouchEvents)}")
    print("Window attributes set:")
    print(f"  WA_AcceptTouchEvents: {window.testAttribute(Qt.WA_AcceptTouchEvents)}")
    
    window.showFullScreen()
    
    logger.info("应用程序已启动，等待触摸输入")
    print("Application started")
    print("=" * 60)
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()

