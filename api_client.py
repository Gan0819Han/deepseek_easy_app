import requests
from PyQt5.QtCore import QThread, pyqtSignal

class DeepseekThread(QThread):
    """处理Deepseek API调用的线程"""
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key, api_url, messages, model_name, use_proxy=False, proxy_url="", verify_ssl=True):
        super().__init__()
        self.api_key = api_key
        self.api_url = api_url
        self.messages = messages
        self.model_name = model_name
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
                "model": self.model_name,
                "messages": self.messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            proxies = None
            if self.use_proxy and self.proxy_url:
                proxies = {
                    "http": self.proxy_url,
                    "https": self.proxy_url
                }
            
            # 修改请求设置，增加超时时间和重试机制
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                proxies=proxies,
                verify=self.verify_ssl,
                timeout=(10, 30)  # 保持当前超时设置
            )
            
            # 将响应处理移到try块内部
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                self.result_ready.emit(response_text)
            else:
                error_message = f"API错误: {response.status_code} - {response.text}"
                self.error_occurred.emit(error_message)
                
        except requests.exceptions.Timeout as e:
            error_type = "连接超时" if isinstance(e, requests.ConnectTimeout) else "读取超时"
            self.error_occurred.emit(f"网络超时 ({error_type}): 请检查代理设置或尝试重新发送")
        except Exception as e:
            self.error_occurred.emit(f"发生错误: {str(e)}")