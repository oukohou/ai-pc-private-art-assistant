# 快速开始指南

## 项目简介

AI PC端侧私密绘画助手 - 基于OpenVINO优化的Stable Diffusion本地部署方案

## 环境要求

- Python 3.10+
- Windows 11 或 Linux
- 8GB+ RAM (推荐16GB)
- 10GB+ 存储空间

## 快速安装

### 方式1: 自动安装脚本 (推荐Windows)

双击运行 `setup.bat`:

```batch
@echo off
REM 自动安装脚本

echo 正在安装AI PC端侧私密绘画助手...
echo.

REM 创建虚拟环境
echo 1. 创建虚拟环境...
python -m venv venv

REM 激活虚拟环境
echo 2. 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 3. 安装依赖包...
pip install -r requirements.txt

echo.
echo 安装完成！
echo.
echo 使用方法:
echo   启动应用: python main.py
echo   指定GPU: python main.py --device GPU
echo   查看帮助: python main.py --help
echo.
pause
```

### 方式2: 手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

### 方式3: 一键命令

```bash
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

## 快速启动

### 基本启动

```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动应用
python main.py
```

应用将自动在浏览器中打开 (http://localhost:7860)

### 高级选项

```bash
# 使用GPU加速
python main.py --device GPU

# 启用量化优化
python main.py --quantize

# 公开访问链接
python main.py --share

# 指定端口
python main.py --server_port 8080

# OpenClaw技能模式
python main.py --openclaw
```

## 首次使用

1. **等待模型下载**: 首次启动会自动下载Stable Diffusion模型 (约5GB)
2. **模型转换**: OpenVINO会自动转换模型格式 (约10分钟)
3. **开始生成**: 转换完成后即可使用

## 界面操作

1. **输入提示词**: 在"提示词"框中输入描述
   - 示例: `a beautiful sunset over mountains, high quality`

2. **调整参数** (可选):
   - **推理步数**: 20-50，越高质量越好
   - **引导比例**: 7.5-15，越高越遵循提示词
   - **随机种子**: -1随机，固定值可重现

3. **点击生成**: 等待10-20秒完成

4. **下载图片**: 右键保存或使用下载按钮

## 常见问题

### Q1: 启动时提示缺少依赖？

**解决**: 重新安装依赖
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Q2: 模型下载很慢？

**解决**: 使用国内镜像
```bash
# 设置HF镜像
set HF_ENDPOINT=https://hf-mirror.com
python main.py
```

### Q3: 显存不足？

**解决**: 使用CPU模式或减少分辨率
```bash
# 使用CPU
python main.py --device CPU
```

### Q4: 生成速度慢？

**解决**: 启用量化优化
```bash
python main.py --quantize
```

### Q5: 如何离线使用？

**解决**: 先在线下载模型，之后可离线使用

```python
# 模型下载后存储在: ./models/stable-diffusion-ov/
# 备份此文件夹即可离线使用
```

## 性能优化

### 推荐配置

**最佳性能**:
```bash
python main.py --device AUTO --quantize
```

**平衡模式**:
```bash
python main.py --device GPU
```

**省电模式**:
```bash
python main.py --device CPU --steps 10
```

### 硬件要求

| 配置 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | Intel Core i5 | Intel Core Ultra 7 |
| RAM | 8GB | 16GB+ |
| GPU | 集成显卡 | Intel Arc GPU |
| 存储 | 20GB | 50GB+ |

## API使用

### Python API

```python
from image_generator import ImageGenerator

# 初始化生成器
gen = ImageGenerator(device="AUTO")

# 生成图像
image, seed = gen.generate(
    prompt="a beautiful sunset",
    num_inference_steps=20
)

# 保存图像
from PIL import Image
img = Image.fromarray(image)
img.save("output.png")
```

### HTTP API

启动技能服务:
```bash
python main.py --openclaw
```

调用API:
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset"}'
```

## 示例提示词

### 风景
```
a beautiful sunset over mountains, high quality, detailed, 8k
```

### 动物
```
a cute cat wearing a hat, cartoon style, colorful, kawaii
```

### 科幻
```
futuristic cityscape, cyberpunk, neon lights, night, detailed
```

### 人像
```
portrait of a beautiful woman, photography, soft lighting, professional
```

### 奇幻
```
a magical forest with glowing mushrooms, fantasy art, dreamy atmosphere
```

## 故障排除

### 问题1: CUDA out of memory

**解决**: 使用CPU或减小batch size
```bash
python main.py --device CPU
```

### 问题2: 模型加载失败

**解决**: 删除模型缓存重新下载
```bash
# 删除模型文件夹
rmdir /s /q models\stable-diffusion-ov

# 重新启动
python main.py
```

### 问题3: 端口被占用

**解决**: 更换端口
```bash
python main.py --server_port 8080
```

### 问题4: 界面打不开

**解决**: 检查防火墙或手动访问
```
http://localhost:7860
```

## 获取帮助

- **查看文档**: README.md
- **技术文章**: technical_article.md
- **提交Issue**: GitHub Issues
- **社区支持**: ModelScope社区

## 许可证

MIT License - 详见LICENSE文件

---

**版本**: v1.0.0  
**最后更新**: 2026年4月3日  
**状态**: ✅ 稳定运行

---

<div align="center">

**🎨 开始你的AI创作之旅吧！**

</div>
