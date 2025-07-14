## 项目概述
本工具支持将文本格式的日程信息转换为标准的 ICS 日历文件格式，方便导入到各类日历应用中使用。该工具包含一个前端页面和一个后端服务，前端用于输入日程并展示生成的ICS内容，后端使用FastAPI提供Kimi API处理器以实现日程到ICS的转换。

## 功能特点
- 支持将用户输入的日程描述通过Kimi API转换为ICS格式代码
- 提供友好的前端界面用于输入日程和查看生成结果
- 支持一键复制或下载生成的ICS内容
- 后端集成OpenAI客户端调用Moonshot Kimi API
- 添加CORS中间件以支持跨域请求

## 安装与运行
### 安装依赖
```bash
pip install fastapi uvicorn openai python-multipart
```

### 配置API密钥
在启动服务前通过终端设置环境变量：
```bash
export MOONSHOT_API_KEY="your_actual_api_key_here"
```

### 启动后端服务
```bash
python BackendService.py
```
默认监听地址：`http://localhost:8000`

### 运行前端服务（可选）
```bash
python -m http.server 8001
```
浏览器访问：`http://localhost:8001`

## 使用帮助
1. 在前端页面输入日程详情
2. 点击“生成 ICS”按钮获取转换后的ICS内容
3. 可选择复制代码或下载ICS文件用于导入日历应用

## 注意事项
- 确保使用的API密钥具有调用目标模型（如`moonshot-v1-8k`）的权限
- 检查网络环境是否满足API调用要求
- 不要将API密钥硬编码在代码中，请使用环境变量存储敏感信息