import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QSplitter, QLineEdit, QFormLayout, QCheckBox,
                            QComboBox)  # 添加QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class DeepseekThread(QThread):
    """处理Deepseek API调用的线程,避免界面卡顿"""
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key, api_url, messages, model_name, use_proxy=False, proxy_url="", verify_ssl=True):
        super().__init__()
        self.api_key = api_key
        self.api_url = api_url
        self.messages = messages
        self.model_name = model_name  # 添加模型名称参数
        self.use_proxy = use_proxy
        self.proxy_url = proxy_url
        self.verify_ssl = verify_ssl
        
    def run(self):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model_name,  # 使用选择的模型名称
                "messages": self.messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 设置代理和SSL选项
            proxies = None
            if self.use_proxy and self.proxy_url:
                proxies = {
                    "http": self.proxy_url,
                    "https": self.proxy_url
                }
            
            # 发送请求时设置代理和SSL验证选项
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data, 
                proxies=proxies,
                verify=self.verify_ssl,
                timeout=30  # 添加超时设置
            )
            
            if response.status_code == 200:
                result = response.json()
                # 根据实际API返回结构调整此处
                response_text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                self.result_ready.emit(response_text)
            else:
                error_message = f"API错误: {response.status_code} - {response.text}"
                self.error_occurred.emit(error_message)
                
        except Exception as e:
            self.error_occurred.emit(f"发生错误: {str(e)}")


class DeepseekApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.message_history = []  # 添加消息历史列表
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Deepseek 助手')
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建API设置部分
        settings_widget = QWidget()
        settings_layout = QFormLayout(settings_widget)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        settings_layout.addRow("API Key:", self.api_key_input)
        
        self.api_url_input = QLineEdit("https://api.deepseek.com/v1/chat/completions")
        settings_layout.addRow("API URL:", self.api_url_input)
        
        # 添加模型选择下拉框
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "deepseek-chat", 
            "deepseek-reasoner"
        ])
        settings_layout.addRow("选择模型:", self.model_selector)
        
        # 添加代理设置
        proxy_widget = QWidget()
        proxy_layout = QHBoxLayout(proxy_widget)
        proxy_layout.setContentsMargins(0, 0, 0, 0)
        
        self.use_proxy_checkbox = QCheckBox("使用代理")
        proxy_layout.addWidget(self.use_proxy_checkbox)
        
        self.proxy_url_input = QLineEdit()
        self.proxy_url_input.setPlaceholderText("http://proxy.example.com:port")
        proxy_layout.addWidget(self.proxy_url_input)
        
        settings_layout.addRow("代理设置:", proxy_widget)
        
        # 添加SSL验证选项
        self.verify_ssl_checkbox = QCheckBox("验证SSL证书")
        self.verify_ssl_checkbox.setChecked(True)
        settings_layout.addRow("SSL选项:", self.verify_ssl_checkbox)
        
        main_layout.addWidget(settings_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 创建输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        input_label = QLabel("输入:")
        input_layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        input_layout.addWidget(self.input_text)
        
        send_button = QPushButton("发送到Deepseek")
        send_button.clicked.connect(self.process_input)
        input_layout.addWidget(send_button)
        
        # 创建输出区域
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        output_label = QLabel("Deepseek输出:")
        output_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        
        # 在输出区域上方添加清除历史按钮
        clear_button = QPushButton("清除对话历史")
        clear_button.clicked.connect(self.clear_history)
        output_layout.insertWidget(0, clear_button)
        
        # 添加到分割器
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        splitter.setSizes([300, 300])  # 设置初始大小比例
        
        main_layout.addWidget(splitter)
        
        # 状态栏
        self.statusBar().showMessage('准备就绪')
        
        # 连接 use_proxy_checkbox 的 toggled 信号
        self.use_proxy_checkbox.toggled.connect(self.toggle_proxy_input)
        
        # 初始化时禁用代理输入框
        self.proxy_url_input.setEnabled(False)
        
    def toggle_proxy_input(self, checked):
        # 当复选框被选中时启用代理输入框，否则禁用
        self.proxy_url_input.setEnabled(checked)
        
    def clear_history(self):
        """清除对话历史"""
        self.message_history = []
        self.output_text.setText("对话历史已清除")
        self.statusBar().showMessage('对话历史已清除')
        
    def process_input(self):
        # 获取输入文本和API设置
        prompt = self.input_text.toPlainText().strip()
        api_key = self.api_key_input.text().strip()
        api_url = self.api_url_input.text().strip()
        
        # 获取选择的模型
        model_name = self.model_selector.currentText()
        
        # 获取代理和SSL选项
        use_proxy = self.use_proxy_checkbox.isChecked()
        proxy_url = self.proxy_url_input.text().strip() if use_proxy else ""
        verify_ssl = self.verify_ssl_checkbox.isChecked()
        
        if not prompt:
            self.statusBar().showMessage('请输入内容')
            return
            
        if not api_key:
            self.statusBar().showMessage('请输入API Key')
            return
            
        if not api_url:
            self.statusBar().showMessage('请输入API URL')
            return
            
        if use_proxy and not proxy_url:
            self.statusBar().showMessage('已启用代理但未设置代理URL')
            return
            
        # 更新状态
        self.statusBar().showMessage('正在处理...')
        
        # 将用户输入添加到消息历史
        self.message_history.append({"role": "user", "content": prompt})
        
        # 更新输出区域显示完整对话历史
        self.update_conversation_display()
        self.output_text.append("\n\n正在等待Deepseek的回复...")
        
        # 创建并启动线程，传递完整的消息历史和模型名称
        self.thread = DeepseekThread(
            api_key, 
            api_url, 
            self.message_history,
            model_name,  # 传递模型名称
            use_proxy=use_proxy, 
            proxy_url=proxy_url, 
            verify_ssl=verify_ssl
        )
        self.thread.result_ready.connect(self.update_output)
        self.thread.error_occurred.connect(self.handle_error)
        self.thread.start()
        
        # 清空输入框
        self.input_text.clear()
    
    def update_output(self, result):
        # 将AI回复添加到消息历史
        self.message_history.append({"role": "assistant", "content": result})
        
        # 更新对话显示
        self.update_conversation_display()
        self.statusBar().showMessage('处理完成')
    
    def update_conversation_display(self):
        """更新对话显示区域，展示完整的对话历史"""
        self.output_text.clear()
        for message in self.message_history:
            role = "用户" if message["role"] == "user" else "DeepSeek"
            content = message["content"]
            self.output_text.append(f"【{role}】: {content}\n")
        
    def handle_error(self, error_message):
        # 保留当前对话历史显示，只在末尾添加错误信息
        self.update_conversation_display()
        self.output_text.append(f"\n错误: {error_message}")
        self.statusBar().showMessage('发生错误')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DeepseekApp()
    ex.show()
    sys.exit(app.exec_())