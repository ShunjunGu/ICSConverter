import os

from fastapi import FastAPI, Request
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

    def convert_schedule_to_ics(self, schedule_input):
        """
        将用户输入的日程转换为ICS格式
        
        参数:
            schedule_input (str): 用户输入的日程描述
            
        返回:
            str: ICS格式的日程数据
        """
        try:
            completion = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {
                        "role": "system",
                        "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。你的任务是将用户输入的日程转换为ICS格式的代码，并且不得输出ICS代码以外的任何内容，包括提示性的文件。ICS是一种日历事件的标准格式，请确保输出的内容符合ICS规范。",
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

# 初始化Kimi API处理器
handler = KimiAPIHandler(os.environ.get("MOONSHOT_API_KEY", "$MOONSHOT_API_KEY"))  # 使用环境变量获取API密钥

@app.post("/convert-to-ics")
async def convert_to_ics(request: Request):
    data = await request.json()
    schedule_input = data.get("scheduleInput", "")
    ics_output = handler.convert_schedule_to_ics(schedule_input)
    return {"ics": ics_output}