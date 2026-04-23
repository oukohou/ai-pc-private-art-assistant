#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intel AI PC端侧私密绘画助手 - 简化版
直接使用Stable Diffusion，无需OpenVINO转换
"""

import os
import torch
from diffusers import StableDiffusionPipeline
import gradio as gr

# 设置镜像站
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def load_model():
    """加载模型"""
    print("=" * 60)
    print("正在加载 Stable Diffusion v1.5 模型...")
    print("=" * 60)
    
    # 检查本地模型
    local_model_path = "./models/stable-diffusion-v1-5"
    
    if os.path.exists(local_model_path):
        print(f"从本地加载模型: {local_model_path}")
        pipe = StableDiffusionPipeline.from_pretrained(
            local_model_path,
            torch_dtype=torch.float32,
            local_files_only=True
        )
    else:
        print("从HuggingFace下载模型...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32
        )
    
    # 使用CPU
    device = "cpu"
    print(f"使用设备: {device}")
    pipe = pipe.to(device)
    
    # 启用内存优化
    try:
        pipe.enable_attention_slicing()
        print("已启用注意力切片优化")
    except:
        print("注意力切片不可用")
    
    print("模型加载完成！")
    return pipe

def generate_image(pipe, prompt, negative_prompt="", steps=20, guidance_scale=7.5, seed=-1):
    """生成图像"""
    import numpy as np
    from PIL import Image
    
    if seed == -1:
        seed = np.random.randint(0, 2147483647)
    
    generator = torch.Generator().manual_seed(seed)
    
    print(f"生成图像: {prompt}")
    print(f"步数: {steps}, 引导比例: {guidance_scale}, 种子: {seed}")
    
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt if negative_prompt else None,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        generator=generator
    ).images[0]
    
    return image

def create_interface(pipe):
    """创建Gradio界面"""
    with gr.Blocks(title="Intel AI PC Art Assistant") as interface:
        gr.HTML("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
                <h1 style="color: white; margin: 0;">AI PC端侧私密绘画助手</h1>
                <p style="color: #f0f0f0; margin-top: 10px;">Stable Diffusion v1.5 | 本地隐私保护</p>
            </div>
        """)
        
        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="提示词",
                    placeholder="描述你想生成的图像...",
                    lines=3,
                    value="a beautiful sunset over mountains, high quality, detailed"
                )
                
                negative_prompt = gr.Textbox(
                    label="负面提示词",
                    placeholder="不想出现的内容...",
                    lines=2,
                    value="low quality, blurry"
                )
                
                with gr.Row():
                    steps = gr.Slider(10, 50, value=20, label="推理步数")
                    guidance_scale = gr.Slider(1.0, 20.0, value=7.5, label="引导比例")
                
                seed = gr.Number(value=-1, label="随机种子", info="-1表示随机")
                
                generate_btn = gr.Button("生成图像", variant="primary", size="lg")
            
            with gr.Column():
                output_image = gr.Image(label="生成结果")
                
                info = gr.Textbox(label="生成信息", lines=5, interactive=False)
        
        def on_generate(prompt, negative_prompt, steps, guidance_scale, seed):
            import time
            import traceback
            
            try:
                start = time.time()
                print(f"\n开始生成: {prompt}")
                
                image = generate_image(pipe, prompt, negative_prompt, int(steps), float(guidance_scale), int(seed))
                
                elapsed = time.time() - start
                info_text = f"生成完成！\n耗时: {elapsed:.2f}秒\n种子: {seed if seed != -1 else '随机'}\n推理步数: {steps}\n引导比例: {guidance_scale}"
                print(f"生成成功，耗时 {elapsed:.2f}秒")
                
                return image, info_text
            except Exception as e:
                error_msg = f"生成失败: {str(e)}\n\n请尝试:\n1. 减少推理步数\n2. 简化提示词\n3. 重启程序"
                print(f"错误: {traceback.format_exc()}")
                return None, error_msg
        
        generate_btn.click(
            fn=on_generate,
            inputs=[prompt, negative_prompt, steps, guidance_scale, seed],
            outputs=[output_image, info]
        )
    
    return interface

if __name__ == "__main__":
    print("=" * 60)
    print("Intel AI PC端侧私密绘画助手")
    print("基于Stable Diffusion的端侧AI绘画")
    print("=" * 60)
    
    # 加载模型
    pipe = load_model()
    
    # 创建界面
    print("正在启动Web界面...")
    interface = create_interface(pipe)
    
    # 启动服务器
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True
    )