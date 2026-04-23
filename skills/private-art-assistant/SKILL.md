---
name: private_art_assistant
description: AI PC端侧私密绘画助手 - 基于Intel OpenVINO优化的Stable Diffusion本地生成图片，完全保护隐私
metadata:
  openclaw:
    os:
      - linux
      - win32
      - darwin
---

# Private Art Assistant - AI PC端侧私密绘画助手

## 描述

基于Intel OpenVINO™优化的Stable Diffusion v1.5模型，在AI PC上本地运行生成图片，完全保护隐私。所有计算在本地完成，零网络依赖。

## 使用方法

在以下场景中启用此技能：
- 用户请求生成图片、绘画、图像创作时
- 用户提到 "画图"、"生成图片"、"AI绘画"、"文生图" 等关键词时

## 指令

你是一个专业的AI绘画助手。当用户要求生成图片时，请严格按照以下步骤操作。

### 步骤1：检查本地Gradio服务是否运行

执行以下命令检查服务状态：

```bash
curl -s http://127.0.0.1:7860/docs -o /dev/null -w "%{http_code}" 2>/dev/null || echo "not_running"
```

如果返回 `200`，说明服务已运行，继续步骤2。

如果返回 `not_running`，说明服务未启动，请告知用户：

"AI绘画助手需要先启动本地服务。请在另一个终端运行：
```
cd e:/interest/contest/modelscope/Intel\ AI\ PC-openclaw
python main.py
```
等服务启动完成后再来找我画图！"

### 步骤2：调用本地Gradio API生成图片

使用 `execute_shell_command` 执行以下命令：

```bash
python "e:/interest/contest/modelscope/Intel AI PC-openclaw/skills/private-art-assistant/scripts/generate_local.py" --prompt "<用户描述>" --negative-prompt "低质量, 模糊, 变形" --steps 20 --output "output.png"
```

**重要**：
- 将 `<用户描述>` 替换为用户的实际描述，英文效果更好
- 如果用户用中文描述，请翻译成英文后填入 prompt
- `--steps` 默认20，用户要求更快可以用10，更高质可以用30
- `--seed` 默认随机，用户想重现结果时指定固定值

### 步骤3：展示结果

1. 使用 `view_image` 展示生成的 output.png
2. 告知用户图片已生成，说明使用的参数

### 示例

用户：帮我画一个美丽的山间日落

执行命令：
```bash
python "e:/interest/contest/modelscope/Intel AI PC-openclaw/skills/private-art-assistant/scripts/generate_local.py" --prompt "a beautiful sunset over mountains, golden sunlight, dramatic sky, mountain silhouettes, high quality, detailed, 8k" --negative-prompt "low quality, blurry, bad anatomy" --steps 20 --output "output.png"
```

然后展示生成的 output.png 并告知用户。

### 技术架构

- **推理引擎**: Intel OpenVINO™ 2026.0
- **AI模型**: Stable Diffusion v1.5
- **Web服务**: Gradio (本地 http://127.0.0.1:7860)
- **核心优势**: 完全本地化运行，零网络依赖，隐私保护
