import os
from datetime import datetime  # 导入datetime模块以获取当前时间
import base64  # 导入base64模块

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class KimiAPIHandler:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
        )

    def chat_with_kimi(self, message):
        """
        与Kimi AI进行对话
        
        参数:
            message (str): 用户发送的消息
            
        返回:
            str: Kimi AI的回复
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
            
            # 创建聊天消息
            messages = [
                {
                    "role": "system",
                    "content": f"你是 Kimi，由 Moonshot AI 提供的人工智能助手。你可以帮助用户解答各种问题，提供信息和建议。当前时间为 {current_time}。"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            # 调用Kimi API进行聊天
            completion = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=messages,
                temperature=0.7,
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            # 添加错误处理
            print(f"Error chatting with Kimi: {e}")
            return f"ERROR: 与Kimi对话时发生错误 - {str(e)}"
    
    def convert_schedule_to_ics(self, schedule_input):
        """
        将用户输入的日程转换为ICS格式
        
        参数:
            schedule_input (str): 用户输入的日程描述
            
        返回:
            str: ICS格式的日程数据
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
            completion = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {
                        "role": "system",
                        "content": f"你是 Kimi，由 Moonshot AI 提供的人工智能助手。你的任务是将用户输入的日程转换为ICS格式的代码，并且不得输出ICS代码以外的任何内容，包括提示性的文件。当前时间为 {current_time}。ICS是一种日历事件的标准格式，请确保输出的内容符合ICS规范。",
                    },
                    {
                        "role": "user",
                        "content": f"请将以下日程转换为ICS代码：\n{schedule_input}",
                    },
                ],
                temperature=0.3,
            )
            return completion.choices[0].message.content
        except Exception as e:
            # 添加错误处理
            print(f"Error converting schedule to ICS: {e}")
            return f"ERROR: 转换日程时发生错误 - {str(e)}"

    def convert_image_to_ics(self, image_data):
        """
        将图片中的日程信息转换为ICS格式
        
        参数:
            image_data (bytes): 图片的二进制数据
            
        返回:
            str: ICS格式的日程数据
        """
        try:
            # 将图片数据编码为base64格式
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
            
            # 创建多模态消息，包含文本指令和图片数据
            messages = [
                {
                    "role": "system",
                    "content": f"你是 Kimi，由 Moonshot AI 提供的人工智能助手。你的任务是从提供的图片中提取日程信息并转换为ICS格式的代码，并且不得输出ICS代码以外的任何内容，包括提示性的文件。当前时间为 {current_time}。ICS是一种日历事件的标准格式，请确保输出的内容符合ICS规范。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请分析这张图片中的日程信息，并将其转换为ICS格式的代码："},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                    ]
                }
            ]
            
            # 调用Kimi API进行转换
            completion = self.client.chat.completions.create(
                model="moonshot-v1-128k-vision-preview",  # 使用官方推荐的支持视觉功能的模型
                messages=messages,
                temperature=0.3,
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            # 添加错误处理
            print(f"Error converting image to ICS: {e}")
            return f"ERROR: 转换图片时发生错误 - {str(e)}"

# 初始化Kimi API处理器
api_key = os.environ.get("MOONSHOT_API_KEY")
if not api_key:
    raise ValueError("MOONSHOT_API_KEY environment variable is not set.")
handler = KimiAPIHandler(api_key)  # 使用环境变量获取API密钥

@app.post("/convert-to-ics")
async def convert_to_ics(request: Request):
    data = await request.json()
    schedule_input = data.get("scheduleInput", "")
    ics_output = handler.convert_schedule_to_ics(schedule_input)
    return {"ics": ics_output}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    reply = handler.chat_with_kimi(message)
    return {"reply": reply}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    处理图片上传的接口
    """
    # 读取图片内容
    image_data = await file.read()
    
    # 调用图像处理方法
    ics_output = handler.convert_image_to_ics(image_data)
    
    return {"ics": ics_output}
