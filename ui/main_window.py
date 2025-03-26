# 修改导入部分
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QSplitter,
    QLineEdit, QFormLayout, QCheckBox, QComboBox,
    QFrame, QSizePolicy  # 添加缺失的QFrame和QSizePolicy
)
from PyQt5.QtCore import Qt
from api_client import DeepseekThread
from PyQt5.QtGui import QIcon

class DeepseekWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.message_history = []
        self.system_prompt = ""
        self.initUI()
        self.load_styles()  # 新增样式初始化
    
    def load_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                font-family: '微软雅黑';
            }
            QTextEdit, QLineEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #006CBB;
            }
            QLabel {
                color: #666666;
                font-weight: bold;
            }
            QSplitter::handle {
                background: #E0E0E0;
                height: 5px;
            }
        """)

    def initUI(self):
        self.setWindowTitle('Deepseek 助手')
        self.setGeometry(100, 100, 1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # API设置部分
        settings_widget = QWidget()
        settings_layout = QFormLayout(settings_widget)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        settings_layout.addRow("API Key:", self.api_key_input)
        
        self.api_url_input = QLineEdit("https://api.deepseek.com/v1/chat/completions")
        settings_layout.addRow("API URL:", self.api_url_input)
        
        self.model_selector = QComboBox()
        self.model_selector.addItems(["deepseek-chat", "deepseek-reasoner"])
        settings_layout.addRow("选择模型:", self.model_selector)
        
        # 代理设置
        proxy_widget = QWidget()
        proxy_layout = QHBoxLayout(proxy_widget)
        proxy_layout.setContentsMargins(0, 0, 0, 0)
        self.use_proxy_checkbox = QCheckBox("使用代理")
        proxy_layout.addWidget(self.use_proxy_checkbox)
        self.proxy_url_input = QLineEdit()
        self.proxy_url_input.setPlaceholderText("http://proxy.example.com:port")
        proxy_layout.addWidget(self.proxy_url_input)
        settings_layout.addRow("代理设置:", proxy_widget)
        
        self.verify_ssl_checkbox = QCheckBox("验证SSL证书")
        self.verify_ssl_checkbox.setChecked(True)
        settings_layout.addRow("SSL选项:", self.verify_ssl_checkbox)
        
        # 在API设置部分添加提示词输入
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("请输入系统提示词（例如：你是一个专业翻译助手）")
        self.prompt_input.setMaximumHeight(80)
        settings_layout.addRow("系统提示:", self.prompt_input)
        
        # 在API设置部分下方添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #444;")
        main_layout.addWidget(line)
        
        # 修改分割器策略
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(5)  # 增加分割线宽度
        splitter.setStyleSheet("QSplitter::handle { background: #444; }")
        
        # 调整输入输出区域的尺寸策略
        # 创建输入区域时添加实例变量
        self.input_widget = QWidget()  # 修改为实例变量
        input_layout = QVBoxLayout(self.input_widget)
        input_label = QLabel("输入:")
        self.input_text = QTextEdit()
        send_button = QPushButton("发送到Deepseek")
        send_button.clicked.connect(self.process_input)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(send_button)
        
        # 创建输出区域时添加实例变量
        self.output_widget = QWidget()  # 修改为实例变量
        output_layout = QVBoxLayout(self.output_widget)
        output_label = QLabel("Deepseek输出:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        clear_button = QPushButton("清除对话历史")
        clear_button.clicked.connect(self.clear_history)
        output_layout.addWidget(clear_button)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        
        # 修改尺寸策略设置部分
        self.input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.output_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 限制设置区域的最大高度
        settings_widget.setMaximumHeight(280)
        
        main_layout.addWidget(settings_widget)
        
        # 分割器布局
        splitter = QSplitter(Qt.Vertical)
        
        # 输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_label = QLabel("输入:")
        self.input_text = QTextEdit()
        send_button = QPushButton("发送到Deepseek")
        send_button.clicked.connect(self.process_input)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(send_button)
        
        # 输出区域
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_label = QLabel("Deepseek输出:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        clear_button = QPushButton("清除对话历史")
        clear_button.clicked.connect(self.clear_history)
        output_layout.addWidget(clear_button)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        splitter.setSizes([300, 300])
        main_layout.addWidget(splitter)
        
        # 状态栏和信号连接
        self.statusBar().showMessage('准备就绪')
        self.use_proxy_checkbox.toggled.connect(self.toggle_proxy_input)
        self.proxy_url_input.setEnabled(False)
        
    def toggle_proxy_input(self, checked):
        self.proxy_url_input.setEnabled(checked)
        
    def clear_history(self):
        self.message_history = []
        self.output_text.setText("对话历史已清除")
        self.statusBar().showMessage('对话历史已清除')
        
    def process_input(self):
        # 获取系统提示词
        system_prompt = self.prompt_input.toPlainText().strip()
        
        prompt = self.input_text.toPlainText().strip()
        api_key = self.api_key_input.text().strip()
        api_url = self.api_url_input.text().strip()
        use_proxy = self.use_proxy_checkbox.isChecked()
        proxy_url = self.proxy_url_input.text().strip() if use_proxy else ""
        verify_ssl = self.verify_ssl_checkbox.isChecked()
        model_name = self.model_selector.currentText()
        
        if not prompt:
            self.statusBar().showMessage('请输入内容')
            return
            
        if not api_key or not api_url:
            self.statusBar().showMessage('请填写API配置')
            return
            
        if use_proxy and not proxy_url:
            self.statusBar().showMessage('已启用代理但未设置代理URL')
            return
            
        self.statusBar().showMessage('正在处理...')
        
        # 构建消息历史（包含系统提示）
        current_messages = []
        if system_prompt:
            current_messages.append({"role": "system", "content": system_prompt})
        current_messages.extend(self.message_history)
        current_messages.append({"role": "user", "content": prompt})
        
        # 更新消息历史显示
        self.message_history.append({"role": "user", "content": prompt})
        self.update_conversation_display()
        
        # 创建线程时传递 current_messages
        self.thread = DeepseekThread(
            api_key, 
            api_url, 
            current_messages,  # 传递包含系统提示的消息
            model_name,
            use_proxy, 
            proxy_url, 
            verify_ssl
        )
        self.thread.result_ready.connect(self.update_output)
        self.thread.error_occurred.connect(self.handle_error)
        self.thread.start()
        self.input_text.clear()
    
    def update_output(self, result):
        self.message_history.append({"role": "assistant", "content": result})
        self.update_conversation_display()
        self.statusBar().showMessage('处理完成')
    
    def update_conversation_display(self):
        """更新对话显示区域，展示完整的对话历史"""
        self.output_text.clear()
        for message in self.message_history:
            role = "用户" if message["role"] == "user" else "DeepSeek"
            # 过滤系统提示词不显示在对话历史中
            if message["role"] != "system":
                self.output_text.append(f"【{role}】: {message['content']}\n")
    
    def handle_error(self, error_message):
        self.output_text.append(f"\n错误: {error_message}")
        self.statusBar().showMessage('发生错误')