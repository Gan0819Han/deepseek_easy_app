# Deepseek 助手应用

这是一个使用PyQt5构建的桌面应用程序，它允许用户通过Deepseek API发送请求并获取AI模型的回复。

## 功能

- 直观的用户界面，分为输入和输出两个窗口
- 支持配置Deepseek API密钥和URL
- 支持配置代理服务器设置和SSL验证选项
- 异步处理API请求，不会阻塞UI
- 显示错误信息和处理状态

## 安装依赖

在运行应用程序之前，请确保已安装以下依赖：

```bash
pip install PyQt5 requests
```

## 使用方法

1. 运行应用程序:
   ```bash
   python deepseek_app.py
   ```

2. 在界面上方配置必要的设置：
   - 输入您的Deepseek API密钥（必需）
   - 默认API URL已预填，但可以根据需要修改
   - 如果需要使用代理，勾选"使用代理"并输入代理URL（格式：http://proxy.example.com:port）
   - 如果遇到SSL证书问题，可以取消勾选"验证SSL证书"选项

3. 在输入框中输入您的问题或提示

4. 点击"发送到Deepseek"按钮提交请求

5. 在下方的输出窗口中查看Deepseek AI的回复

## 网络连接问题解决方案

如果遇到类似以下的错误：
```
HTTPSConnectionPool(host='api.deepseek.com', port=443): Max retries exceeded with url: / (Caused by ProxyError('Unable to connect to proxy', SSLError(SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF) (_ssl.c:1149)'))))
```

可以尝试以下解决方案：

1. **代理设置**：
   - 如果您在使用代理，确保代理URL格式正确
   - 检查代理服务器是否可用和稳定
   - 尝试使用不同的代理服务器

2. **SSL验证**：
   - 如果遇到SSL证书相关错误，可以取消勾选"验证SSL证书"选项
   - 注意：禁用SSL验证可能会降低连接的安全性

3. **网络连接**：
   - 检查您的网络连接是否稳定
   - 确认您能够正常访问api.deepseek.com
   - 如果使用公司或学校网络，可能有防火墙限制

4. **API URL**：
   - 确保API URL正确无误
   - 可以尝试联系Deepseek获取正确的API端点

## 注意事项

- 您需要有效的Deepseek API密钥才能使用此应用程序
- API请求可能需要一些时间来处理，具体取决于网络状况和请求复杂性
- 大多数错误会在输出窗口中显示，并在状态栏中提示

## 自定义

您可以通过修改`deepseek_app.py`文件来自定义应用程序：

- 调整窗口大小和布局
- 修改默认的API参数
- 添加更多功能，如保存对话历史等 