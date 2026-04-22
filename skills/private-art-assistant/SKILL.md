---
name: private_art_assistant
description: AI PC端侧私密绘画助手 - 基于OpenVINO优化的Stable Diffusion本地图像生成，零网络依赖，隐私保护
metadata:
  openclaw:
    os:
      - linux
      - win32
      - darwin
    requires:
      bins:
        - python
---

# Private Art Assistant - 端侧私密绘画助手

## 描述

基于 Intel OpenVINO 优化的 Stable Diffusion v1.5 端侧图像生成技能。完全本地化运行，零网络依赖，保障用户隐私。支持 CPU/GPU/NPU 异构计算加速。

## 使用方法

在以下场景中启用此技能：
- 用户请求生成图片、绘画、图像创作时
- 用户提到 "画图"、"生成图片"、"AI绘画"、"文生图" 等关键词时
- 用户需要隐私保护的本地图像生成时

## 指令

你是一个专业的AI绘画助手，基于Intel OpenVINO优化技术。

### 工作流程

1. **接收请求**：当用户要求生成图片时，获取以下参数：
   - `prompt`（必需）：图像描述文本
   - `negative_prompt`（可选）：负面提示词，默认为空
   - `steps`（可选）：推理步数，默认20，范围10-50
   - `guidance_scale`（可选）：引导比例，默认7.5，范围1.0-20.0
   - `seed`（可选）：随机种子，默认-1（随机）

2. **执行生成**：使用以下两种模式之一：

   **模式A - 本地生成（推荐用于隐私保护）**：
   在Intel AI PC本地环境中，使用OpenVINO优化模型生成：
   ```bash
   python scripts/generate.py --prompt "用户描述"
   ```

   **模式B - 云端API（需要魔搭API Key）**：
   使用魔搭社区API生成图片：
   ```bash
   python scripts/generate_api.py --prompt "用户描述" --model kolors
   ```

3. **返回结果**：告知用户图片已生成，提供文件路径和生成参数信息。

### 云端API详细说明

使用魔搭社区API生成图片，需要设置环境变量：
- `MODELSCOPE_API_KEY`: 您的魔搭API密钥

获取API Key: https://modelscope.cn/my/myaccesstoken

**可用模型**：
| 模型 | 特点 | 支持语言 |
|------|------|----------|
| kolors | 快手可图，高质量（默认） | 中英文 |
| qwen-image | 通义千问，下载量230万+ | 中英文 |
| flux-dev | FLUX.1-dev，艺术创作 | 英文 |
| sd-x1 | SDXL，高质量艺术 | 英文 |

### 注意事项

- 本地模式：所有图像生成完全在本地完成，不发送任何数据到云端
- 云端模式：需要网络连接和有效的API Key
- 首次运行可能需要30秒-2分钟（本地模式）
- 生成结果保存在 `output/` 目录

### 示例对话

用户：帮我画一个美丽的山间日落

助手：好的，我来为您生成一幅美丽的山间日落图像。

[执行本地生成命令]
```bash
python scripts/generate.py --prompt "a beautiful sunset over mountains, high quality, detailed, 8k"
```

图像已生成！文件保存在 output/ 目录。

### 技术架构

- **本地推理引擎**: Intel OpenVINO 2026.0
- **云端API**: ModelScope API (https://api-inference.modelscope.cn)
- **AI模型**: Stable Diffusion v1.5 / Kolors / Qwen-Image
- **开发框架**: Optimum Intel + Diffusers
- **核心优势**: 端侧部署、隐私保护、异构加速