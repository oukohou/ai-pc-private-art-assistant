#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intel AI PC端侧私密绘画助手
基于OpenVINO™优化的Stable Diffusion端侧图像生成应用

项目名称: AI PC Private Art Assistant
技术栈: OpenVINO™, Stable Diffusion, Gradio
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from image_generator import ImageGenerator
from gradio_interface import create_gradio_interface
from openclaw_skill import OpenClawSkill

def main():
    parser = argparse.ArgumentParser(description='Intel AI PC端侧私密绘画助手')
    parser.add_argument('--model', type=str, default='stable-diffusion-v1-5',
                        help='模型名称或路径')
    parser.add_argument('--device', type=str, default='AUTO',
                        help='推理设备 (AUTO, CPU, GPU, NPU)')
    parser.add_argument('--quantize', action='store_true',
                        help='使用INT8量化优化')
    parser.add_argument('--share', action='store_true',
                        help='创建公开链接')
    parser.add_argument('--server_port', type=int, default=7860,
                        help='Gradio服务端口')
    parser.add_argument('--openclaw', action='store_true',
                        help='以OpenClaw Skill模式运行')
    parser.add_argument('--skill_name', type=str, default='private_art_assistant',
                        help='OpenClaw Skill名称')
    
    args = parser.parse_args()
    
    print("="*60)
    print("Intel AI PC端侧私密绘画助手")
    print("基于OpenVINO™优化的Stable Diffusion")
    print("="*60)
    print(f"模型: {args.model}")
    print(f"设备: {args.device}")
    print(f"量化: {args.quantize}")
    print("="*60)
    
    try:
        # 初始化图像生成器
        print("正在初始化模型...")
        generator = ImageGenerator(
            model_id=args.model,
            device=args.device,
            quantize=args.quantize
        )
        
        if args.openclaw:
            # OpenClaw Skill模式
            print("正在启动OpenClaw Skill...")
            skill = OpenClawSkill(
                generator=generator,
                skill_name=args.skill_name
            )
            skill.run()
        else:
            # Gradio Web界面模式
            print("正在启动Gradio Web界面...")
            interface = create_gradio_interface(generator)
            interface.launch(
                server_name="0.0.0.0",
                server_port=args.server_port,
                share=args.share,
                inbrowser=True
            )
            
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
