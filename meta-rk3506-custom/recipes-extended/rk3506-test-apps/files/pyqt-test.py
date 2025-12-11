#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 Display Test for RK3506 EVM
RK3506 显示测试程序 - 480x800 DSI显示屏
现代化中文界面设计
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QCheckBox, QRadioButton,
                             QSlider, QProgressBar, QSpinBox, QComboBox, QGroupBox,
                             QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QPalette, QColor, QFontDatabase

class PyQtTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        
        # 设置默认字体（确保字体可用）
        font_db = QFontDatabase()
        available_fonts = font_db.families()
        
        # 尝试使用DejaVu Sans，如果不可用则使用系统默认字体
        if 'DejaVu Sans' in available_fonts:
            default_font = QFont('DejaVu Sans', 10)
        elif len(available_fonts) > 0:
            default_font = QFont(available_fonts[0], 10)
        else:
            default_font = QFont()
        
        self.setFont(default_font)
        
        self.init_ui()
        self.setup_style()
        
        # 启动时钟更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新
        self.update_time()
        
    def setup_style(self):
        """设置现代化样式表"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QLabel#titleLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
            
            QLabel#timeLabel {
                color: #3498db;
                font-size: 14px;
                padding: 5px;
            }
            
            QLabel#statusLabel {
                color: #27ae60;
                font-size: 13px;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
            }
            
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2c3e50;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 12px;
                font-weight: bold;
                min-height: 35px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #21618c;
            }
            
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            
            QCheckBox, QRadioButton {
                font-size: 12px;
                spacing: 8px;
            }
            
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            
            QSlider::groove:horizontal {
                height: 8px;
                background: #ecf0f1;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #3498db;
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                text-align: center;
                font-size: 11px;
                font-weight: bold;
            }
            
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 4px;
            }
            
            QSpinBox, QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
                background-color: white;
            }
            
            QSpinBox:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QLabel#counterLabel {
                color: #e74c3c;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
    def init_ui(self):
        self.setWindowTitle("RK3506 Control Test")
        
        # 窗口将以全屏模式启动，自动适配屏幕尺寸
        
        # 创建可滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll)
        
        # 主容器
        container = QWidget()
        scroll.setWidget(container)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        container.setLayout(main_layout)
        
        # === 顶部标题区域 ===
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # 标题标签
        title_label = QLabel("RK3506 Display Test")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # 时钟标签
        self.time_label = QLabel("")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.time_label)
        
        main_layout.addLayout(header_layout)
        
        # 状态标签
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # === 按钮组 ===
        button_group = QGroupBox("Button Test")
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        
        # 第一行按钮
        btn_row1 = QHBoxLayout()
        btn_row1.setSpacing(8)
        self.btn1 = QPushButton("OK")
        self.btn1.clicked.connect(lambda: self.on_button_click("OK"))
        btn_row1.addWidget(self.btn1)
        
        self.btn2 = QPushButton("Cancel")
        self.btn2.clicked.connect(lambda: self.on_button_click("Cancel"))
        btn_row1.addWidget(self.btn2)
        
        self.btn3 = QPushButton("Refresh")
        self.btn3.clicked.connect(lambda: self.on_button_click("Refresh"))
        btn_row1.addWidget(self.btn3)
        button_layout.addLayout(btn_row1)
        
        # 第二行按钮
        btn_row2 = QHBoxLayout()
        btn_row2.setSpacing(8)
        self.btn4 = QPushButton("Previous")
        self.btn4.clicked.connect(lambda: self.on_button_click("Previous"))
        btn_row2.addWidget(self.btn4)
        
        self.btn5 = QPushButton("Next")
        self.btn5.clicked.connect(lambda: self.on_button_click("Next"))
        btn_row2.addWidget(self.btn5)
        
        self.btn6 = QPushButton("Settings")
        self.btn6.clicked.connect(lambda: self.on_button_click("Settings"))
        btn_row2.addWidget(self.btn6)
        button_layout.addLayout(btn_row2)
        
        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)
        
        # === 文本输入框 ===
        input_group = QGroupBox("Text Input")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(5)
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        self.line_edit.textChanged.connect(self.on_text_changed)
        input_layout.addWidget(self.line_edit)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # === 复选框和单选按钮 ===
        check_radio_group = QGroupBox("Selection Controls")
        check_radio_layout = QVBoxLayout()
        check_radio_layout.setSpacing(10)
        
        self.checkbox1 = QCheckBox("Enable Feature A")
        self.checkbox1.stateChanged.connect(self.on_checkbox_changed)
        check_radio_layout.addWidget(self.checkbox1)
        
        self.checkbox2 = QCheckBox("Enable Feature B")
        self.checkbox2.stateChanged.connect(self.on_checkbox_changed)
        check_radio_layout.addWidget(self.checkbox2)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        check_radio_layout.addWidget(line)
        
        self.radio1 = QRadioButton("Red Theme")
        self.radio1.toggled.connect(self.on_radio_changed)
        check_radio_layout.addWidget(self.radio1)
        
        self.radio2 = QRadioButton("Blue Theme")
        self.radio2.toggled.connect(self.on_radio_changed)
        self.radio2.setChecked(True)  # 默认选中
        check_radio_layout.addWidget(self.radio2)
        
        check_radio_group.setLayout(check_radio_layout)
        main_layout.addWidget(check_radio_group)
        
        # === 滑动条和进度条 ===
        slider_group = QGroupBox("Slider & Progress")
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(12)
        
        # 滑块标签
        slider_label_layout = QHBoxLayout()
        slider_label_layout.addWidget(QLabel("Volume:"))
        self.slider_value_label = QLabel("50")
        self.slider_value_label.setStyleSheet("color: #3498db; font-weight: bold;")
        slider_label_layout.addWidget(self.slider_value_label)
        slider_label_layout.addStretch()
        slider_layout.addLayout(slider_label_layout)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.on_slider_changed)
        slider_layout.addWidget(self.slider)
        
        # 进度条标签
        slider_layout.addWidget(QLabel("Download Progress:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(50)
        slider_layout.addWidget(self.progress_bar)
        
        slider_group.setLayout(slider_layout)
        main_layout.addWidget(slider_group)
        
        # === 数字调节框和下拉框 ===
        other_group = QGroupBox("Number & Selection")
        other_layout = QVBoxLayout()
        other_layout.setSpacing(10)
        
        # 数字框
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("Quantity:"))
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(10)
        self.spinbox.valueChanged.connect(self.on_spinbox_changed)
        spinbox_layout.addWidget(self.spinbox)
        spinbox_layout.addStretch()
        other_layout.addLayout(spinbox_layout)
        
        # 下拉框
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("City:"))
        self.combobox = QComboBox()
        self.combobox.addItems(["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Hangzhou"])
        self.combobox.currentTextChanged.connect(self.on_combo_changed)
        combo_layout.addWidget(self.combobox)
        combo_layout.addStretch()
        other_layout.addLayout(combo_layout)
        
        other_group.setLayout(other_layout)
        main_layout.addWidget(other_group)
        
        # === 底部计数器 ===
        counter_group = QGroupBox("Statistics")
        counter_layout = QHBoxLayout()
        counter_layout.addWidget(QLabel("Click Count:"))
        self.counter_label = QLabel("0")
        self.counter_label.setObjectName("counterLabel")
        counter_layout.addWidget(self.counter_label)
        counter_layout.addStretch()
        counter_group.setLayout(counter_layout)
        main_layout.addWidget(counter_group)
        
        # 添加弹性空间
        main_layout.addStretch()
    
    def update_time(self):
        """更新时钟显示"""
        current_time = QTime.currentTime()
        time_text = current_time.toString("HH:mm:ss")
        self.time_label.setText(f"Time: {time_text}")
    
    def on_button_click(self, button_name):
        """按钮点击事件"""
        self.click_count += 1
        self.counter_label.setText(str(self.click_count))
        self.status_label.setText(f"Clicked: {button_name}")
    
    def on_text_changed(self, text):
        """文本改变事件"""
        if text:
            self.status_label.setText(f"Input: {text}")
        else:
            self.status_label.setText("Status: Ready")
    
    def on_checkbox_changed(self, state):
        """复选框改变事件"""
        sender = self.sender()
        status = "Enabled" if state == Qt.Checked else "Disabled"
        self.status_label.setText(f"{sender.text()} {status}")
    
    def on_radio_changed(self, checked):
        """单选按钮改变事件"""
        if checked:
            sender = self.sender()
            self.status_label.setText(f"Switched to: {sender.text()}")
    
    def on_slider_changed(self, value):
        """滑块改变事件"""
        self.slider_value_label.setText(str(value))
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Volume: {value}%")
    
    def on_spinbox_changed(self, value):
        """数字框改变事件"""
        self.status_label.setText(f"Quantity: {value}")
    
    def on_combo_changed(self, text):
        """下拉框改变事件"""
        self.status_label.setText(f"Selected City: {text}")
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Escape:
            self.status_label.setText("Goodbye! Exiting...")
            QTimer.singleShot(500, self.close)  # 延迟关闭以显示消息
        super().keyPressEvent(event)

def main():
    """主函数 - 初始化并启动应用"""
    print("=" * 60)
    print("RK3506 PyQt5 Display Test")
    print("=" * 60)
    
    # 设置QPA平台为嵌入式设备
    # 优先使用eglfs (GPU加速)，备选linuxfb
    if 'QT_QPA_PLATFORM' not in os.environ:
        # 检查eglfs是否可用
        if os.path.exists('/usr/lib/plugins/platforms/libqeglfs.so'):
            os.environ['QT_QPA_PLATFORM'] = 'eglfs'
            print("Using platform: eglfs (GPU accelerated)")
        elif os.path.exists('/usr/lib/plugins/platforms/libqlinuxfb.so'):
            os.environ['QT_QPA_PLATFORM'] = 'linuxfb'
            print("Using platform: linuxfb (Linux FrameBuffer)")
        else:
            # 降级到offscreen用于测试
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
            print("Warning: Using platform: offscreen (no display)")
    
    # 配置运行时环境
    # 注意：系统已在 rockchip-image.bbclass 中配置了 /usr/lib/fonts -> /usr/share/fonts
    # 以下配置作为额外保障，确保在各种情况下都能正常工作
    
    # 设置 XDG_RUNTIME_DIR 避免警告
    if 'XDG_RUNTIME_DIR' not in os.environ:
        os.environ['XDG_RUNTIME_DIR'] = '/tmp'
    
    # 显式设置字体目录到包含字体文件的子目录
    # Qt不会递归扫描子目录，所以必须指向实际包含字体文件的目录
    font_dirs = [
        '/usr/lib/fonts/truetype',
        '/usr/share/fonts/truetype',
        '/usr/lib/fonts',
        '/usr/share/fonts'
    ]
    
    font_dir_set = False
    if 'QT_QPA_FONTDIR' not in os.environ:
        for font_dir in font_dirs:
            if os.path.exists(font_dir) and os.path.isdir(font_dir):
                # 检查目录中是否有字体文件
                font_files = [f for f in os.listdir(font_dir) 
                             if f.lower().endswith(('.ttf', '.otf', '.ttc'))]
                if font_files:
                    os.environ['QT_QPA_FONTDIR'] = font_dir
                    print(f"Font directory: {font_dir} ({len(font_files)} fonts)")
                    font_dir_set = True
                    break
    
    print("\nStarting application...")
    print("Tips:")
    print("   - Application will run in fullscreen mode")
    print("   - Press ESC key to exit\n")
    
    app = QApplication(sys.argv)
    
    # 显式加载字体文件到Qt字体数据库
    # 因为Qt可能不会自动扫描子目录
    font_db = QFontDatabase()
    fonts_loaded = 0
    
    # 尝试加载主要字体文件
    main_fonts = [
        '/usr/share/fonts/truetype/DejaVuSans.ttf',
        '/usr/lib/fonts/truetype/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/DejaVuSans-Bold.ttf',
        '/usr/lib/fonts/truetype/DejaVuSans-Bold.ttf',
    ]
    
    for font_path in main_fonts:
        if os.path.exists(font_path):
            font_id = font_db.addApplicationFont(font_path)
            if font_id != -1:
                families = font_db.applicationFontFamilies(font_id)
                fonts_loaded += 1
                print(f"Loaded font: {font_path} -> {families}")
            break  # 只需要加载一个主字体
    
    # 如果主字体加载失败，尝试扫描并加载所有字体
    if fonts_loaded == 0:
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                try:
                    for font_file in os.listdir(font_dir):
                        if font_file.lower().endswith(('.ttf', '.otf', '.ttc')):
                            font_path = os.path.join(font_dir, font_file)
                            font_id = font_db.addApplicationFont(font_path)
                            if font_id != -1:
                                families = font_db.applicationFontFamilies(font_id)
                                fonts_loaded += 1
                                if fonts_loaded <= 3:  # 只打印前3个
                                    print(f"Loaded font: {font_file} -> {families}")
                                if fonts_loaded >= 5:  # 加载几个主要字体就够了
                                    break
                    if fonts_loaded > 0:
                        break
                except Exception as e:
                    print(f"Warning: Error scanning {font_dir}: {e}")
    
    if fonts_loaded > 0:
        print(f"Total fonts loaded: {fonts_loaded}")
    else:
        print("Warning: No fonts loaded! Text may not display correctly.")
    
    # 使用 Fusion 样式作为基础（现代化外观）
    app.setStyle('Fusion')
    
    # 创建并显示窗口
    window = PyQtTestWindow()
    
    # 直接全屏启动（适合小屏幕嵌入式设备）
    window.showFullScreen()
    
    print("Application started successfully")
    print("=" * 60)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

