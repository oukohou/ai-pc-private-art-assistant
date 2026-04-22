# Private Art Assistant - OpenClaw Skill

基于 Intel OpenVINO 优化的 Stable Diffusion v1.5 端侧图像生成技能。

## 特性

- **端侧部署** - 完全本地运行，零网络依赖
- **隐私保护** - 数据不离开设备
- **异构加速** - 支持 CPU/GPU/NPU 协同计算
- **标准接口** - 符合 OpenClaw Skill 规范

## 安装

将此目录复制到 OpenClaw/CoPaw 的 skills 目录：

```bash
# OpenClaw
cp -r private-art-assistant ~/.openclaw/skills/

# CoPaw
cp -r private-art-assistant ~/.copaw/skills/
```

## 依赖

```bash
pip install torch diffusers transformers accelerate
```

## 使用

在 OpenClaw/CoPaw 中，直接对 AI 说：

> "帮我画一个美丽的山间日落"

AI 将自动调用此技能生成图片。

### 命令行测试

```bash
python scripts/generate.py --prompt "a beautiful sunset over mountains"
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| --prompt | (必需) | 图像描述 |
| --negative-prompt | "" | 负面提示词 |
| --steps | 20 | 推理步数 |
| --guidance-scale | 7.5 | 引导比例 |
| --seed | -1 | 随机种子 |
| --width | 512 | 图像宽度 |
| --height | 512 | 图像高度 |

## 技术架构

- **推理引擎**: Intel OpenVINO 2026.0
- **AI模型**: Stable Diffusion v1.5
- **开发框架**: Optimum Intel + Diffusers
