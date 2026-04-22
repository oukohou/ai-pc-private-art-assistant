---
name: private_art_assistant
description: AI绘画助手 - 使用阿里百炼万相模型生成高质量AI图像，支持多种风格
metadata:
  openclaw:
    os:
      - linux
      - win32
      - darwin
---

# Private Art Assistant - AI绘画助手

## 描述

基于阿里百炼万相(wanx)模型的AI图像生成技能，支持摄影、动漫、油画等多种风格。使用 DashScope API 生成高质量AI绘画作品。也支持本地OpenVINO优化的Stable Diffusion模型进行隐私保护的离线生成。

## 使用方法

在以下场景中启用此技能：
- 用户请求生成图片、绘画、图像创作时
- 用户提到 "画图"、"生成图片"、"AI绘画"、"文生图" 等关键词时

## 指令

你是一个专业的AI绘画助手。当用户要求生成图片时，请严格按照以下步骤操作，**不要用Pillow或其他简单绘图库替代**。

### 步骤1：调用 DashScope 万相模型生成图片

使用 Python 脚本调用阿里百炼API。请直接执行以下Python代码：

```python
import requests, time, json, os

api_key = os.environ.get("DASHSCOPE_API_KEY", "")
if not api_key:
    api_key = os.environ.get("MODELSCOPE_API_KEY", "")

# Step 1: 创建异步任务
url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}
payload = {
    "model": "wanx-v1",
    "input": {
        "prompt": "<用户描述，支持中文>",
        "negative_prompt": "低质量, 模糊, 变形"
    },
    "parameters": {
        "style": "<auto>",
        "size": "1024*1024",
        "n": 1
    }
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
data = resp.json()

# 获取任务ID
if "output" in data and "task_id" in data["output"]:
    task_id = data["output"]["task_id"]
    print(f"Task created: {task_id}")

    # Step 2: 轮询获取结果
    result_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    for i in range(60):
        time.sleep(3)
        r = requests.get(result_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        result = r.json()
        status = result.get("output", {}).get("task_status", "")
        print(f"Status: {status}")
        if status == "SUCCEEDED":
            img_url = result["output"]["results"][0]["url"]
            # 下载图片
            img_data = requests.get(img_url, timeout=30).content
            with open("output.png", "wb") as f:
                f.write(img_data)
            print(f"SUCCESS! Image saved to output.png")
            print(f"URL: {img_url}")
            break
        elif status == "FAILED":
            print(f"FAILED: {result}")
            break
else:
    print(f"Error creating task: {data}")
    print("Trying ModelScope API-Inference instead...")

    # Fallback: 使用 ModelScope API-Inference
    url2 = "https://api-inference.modelscope.cn/v1/images/generations"
    headers2 = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload2 = {
        "model": "AI-ModelScope/Kolors",
        "prompt": "<用户描述>",
        "n": 1,
        "size": "1024x1024"
    }
    resp2 = requests.post(url2, headers=headers2, json=payload2, timeout=60)
    data2 = resp2.json()
    if "images" in data2 and data2["images"]:
        img_url = data2["images"][0]["url"]
        img_data = requests.get(img_url, timeout=30).content
        with open("output.png", "wb") as f:
            f.write(img_data)
        print(f"SUCCESS! Image saved to output.png")
        print(f"URL: {img_url}")
    else:
        print(f"ModelScope API also failed: {data2}")
```

**重要提示**：
- 将 `<用户描述>` 替换为用户实际描述，支持中文
- 环境变量 `DASHSCOPE_API_KEY` 或 `MODELSCOPE_API_KEY` 需要已配置
- 如果两个API都失败，告知用户需要配置API Key，**不要用Pillow替代**

### 步骤2：展示结果

1. 使用 view_image 展示生成的 output.png
2. 告知用户图片已生成

### 步骤3：如果API不可用

如果API调用失败，告知用户：
"AI绘画需要API Key才能工作。请访问 https://modelscope.cn/my/myaccesstoken 获取免费的API Key，并在环境变量中设置 MODELSCOPE_API_KEY。"

**绝对禁止**用 Pillow、matplotlib 或其他非AI绘图库生成图片作为替代。

### 风格参数

可用的 style 参数：
- `<auto>` - 自动（默认）
- `<photography>` - 摄影
- `<anime>` - 动漫
- `<oil painting>` - 油画
- `<3d cartoon>` - 3D卡通
- `<sketch>` - 素描
- `<watercolor>` - 水彩

### 示例

用户：帮我画一个美丽的山间日落

执行Python脚本，prompt设为"美丽的山间日落，金色阳光，戏剧性天空，高山剪影"，style设为"<photography>"，展示生成的output.png

### 技术架构

- **云端API**: 阿里百炼 DashScope API (wanx-v1) + ModelScope API-Inference (Kolors)
- **本地模式**: Intel OpenVINO + Stable Diffusion v1.5（本地AI PC部署时使用）
