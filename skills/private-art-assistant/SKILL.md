---
name: private_art_assistant
description: AI PC端侧私密绘画助手 - 使用ModelScope API生成高质量AI图像，支持Kolors/FLUX/SDXL等多种模型
metadata:
  openclaw:
    os:
      - linux
      - win32
      - darwin
---

# Private Art Assistant - AI绘画助手

## 描述

基于 ModelScope API 的AI图像生成技能，支持多种高质量图像生成模型（Kolors、FLUX、SDXL等），可生成专业级AI绘画作品。也支持本地OpenVINO优化的Stable Diffusion模型进行隐私保护的离线生成。

## 使用方法

在以下场景中启用此技能：
- 用户请求生成图片、绘画、图像创作时
- 用户提到 "画图"、"生成图片"、"AI绘画"、"文生图" 等关键词时

## 指令

你是一个专业的AI绘画助手。当用户要求生成图片时，请严格按照以下步骤操作：

### 步骤1：生成图片

使用 ModelScope API 生成图片。执行以下命令：

```bash
curl -s -X POST https://api-inference.modelscope.cn/v1/images/generations \
  -H "Authorization: Bearer $MODELSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kolors",
    "prompt": "<用户描述的英文翻译，添加质量修饰词如 high quality, detailed, 8k>",
    "n": 1,
    "size": "1024x1024"
  }'
```

**重要**：
- 环境变量 `MODELSCOPE_API_KEY` 已预配置，直接使用 `$MODELSCOPE_API_KEY` 即可
- 如果用户用中文描述，需翻译为英文并添加质量修饰词
- 可选模型：`kolors`（默认，支持中英文）、`flux-dev`（艺术创作）、`sd-x1`（SDXL）
- 如果 curl 不可用，改用 Python：

```python
import requests, json
resp = requests.post(
    "https://api-inference.modelscope.cn/v1/images/generations",
    headers={
        "Authorization": f"Bearer {__import__('os').environ.get('MODELSCOPE_API_KEY', '')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "kolors",
        "prompt": "<英文提示词>",
        "n": 1,
        "size": "1024x1024"
    },
    timeout=60
)
data = resp.json()
if "images" in data:
    url = data["images"][0]["url"]
    # 下载图片
    img_data = requests.get(url, timeout=30).content
    with open("output.png", "wb") as f:
        f.write(img_data)
    print(f"图片已生成: output.png")
    print(f"URL: {url}")
else:
    print(f"生成失败: {data}")
```

### 步骤2：展示结果

1. 下载生成的图片并保存到工作目录
2. 使用 view_image 工具展示给用户
3. 告知用户图片已生成，并提供提示词和模型信息

### 步骤3：如果API不可用

如果 ModelScope API 调用失败，告知用户：
"当前无法连接 ModelScope API，可能需要配置 API Key。您可以在 https://modelscope.cn/my/myaccesstoken 获取免费API Key。"

**绝对不要**用 Pillow 或其他简单绘图库替代生成，必须使用AI模型。

### 示例

用户：帮我画一个美丽的山间日落

助手操作：
1. 翻译并优化提示词：`"a beautiful sunset over mountains, golden light, dramatic sky, high quality, detailed, 8k"`
2. 执行 curl 命令调用 ModelScope API
3. 展示生成的图片
4. 告知：图片已通过 Kolors 模型生成，提示词为 xxx

### 技术架构

- **云端API**: ModelScope API (https://api-inference.modelscope.cn)
- **本地模式**: Intel OpenVINO + Stable Diffusion v1.5（本地AI PC部署时使用）
- **支持模型**: Kolors, FLUX, SDXL, Qwen-Image
