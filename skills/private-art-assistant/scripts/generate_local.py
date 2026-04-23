#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Private Art Assistant - 本地Gradio API调用脚本
CoPaw通过execute_shell_command调用此脚本，
脚本通过Gradio Client调用本地运行的服务来生成图片
"""

import argparse
import sys
import time
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Private Art Assistant - Local Gradio API')
    parser.add_argument('--prompt', type=str, required=True, help='Image generation prompt')
    parser.add_argument('--negative-prompt', type=str, default='low quality, blurry', help='Negative prompt')
    parser.add_argument('--steps', type=int, default=20, help='Number of inference steps')
    parser.add_argument('--guidance-scale', type=float, default=7.5, help='Guidance scale')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (-1 for random)')
    parser.add_argument('--output', type=str, default='output.png', help='Output file path')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Private Art Assistant - Local Gradio API")
    print("=" * 50)
    print(f"Prompt: {args.prompt}")
    print(f"Negative Prompt: {args.negative_prompt}")
    print(f"Steps: {args.steps}, Guidance: {args.guidance_scale}, Seed: {args.seed}")
    print("=" * 50)
    
    try:
        from gradio_client import Client
        
        print(f"\nConnecting to local Gradio service...")
        client = Client("http://127.0.0.1:7860", verbose=False)
        
        print("Generating image...")
        start_time = time.time()
        
        # 调用Gradio API的on_generate接口
        # 参数顺序: prompt, negative_prompt, steps, guidance_scale, seed
        result = client.predict(
            args.prompt,
            args.negative_prompt,
            args.steps,
            args.guidance_scale,
            args.seed,
            api_name="/on_generate"
        )
        
        elapsed = time.time() - start_time
        print(f"\nGeneration complete! Time: {elapsed:.2f}s")
        
        # result 是一个元组 (image_path, info_text)
        if isinstance(result, tuple) and len(result) >= 1:
            image_path = result[0]
            info = result[1] if len(result) > 1 else ""
            
            if image_path and os.path.exists(image_path):
                # 复制到指定输出路径
                import shutil
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(image_path, str(output_path))
                
                print(f"\nImage saved to: {output_path.absolute()}")
                print(f"Info: {info}")
                print(f"Generation time: {elapsed:.2f}s")
            else:
                print(f"\nImage path returned but file not found: {image_path}")
                print(f"Info: {info}")
        else:
            print(f"\nUnexpected result format: {result}")
            
    except ConnectionError:
        print("\nError: Cannot connect to local Gradio service!")
        print("Please make sure the Gradio service is running:")
        print("  python main.py  (or python simple_main.py)")
        print("The service should be available at http://127.0.0.1:7860")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
