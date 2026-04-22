#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Private Art Assistant - OpenClaw Skill 云端API生成脚本
使用魔搭社区API进行图像生成
"""

import argparse
import os
import time
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Private Art Assistant - Cloud API Image Generation')
    parser.add_argument('--prompt', type=str, required=True, help='Image generation prompt')
    parser.add_argument('--model', type=str, default='kolors', help='Model name (kolors, qwen-image, flux-dev, etc.)')
    parser.add_argument('--negative-prompt', type=str, default='', help='Negative prompt')
    parser.add_argument('--count', type=int, default=1, help='Number of images to generate')
    parser.add_argument('--size', type=str, default='1024x1024', help='Image size (e.g., 1024x1024)')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    parser.add_argument('--api-key', type=str, default=None, help='ModelScope API Key (or set MODELSCOPE_API_KEY env)')
    parser.add_argument('--list-models', action='store_true', help='List available models and exit')
    
    args = parser.parse_args()
    
    if args.list_models:
        print("=" * 50)
        print("Private Art Assistant - Available Models")
        print("=" * 50)
        print()
        print("| Model         | Description                    | Language |")
        print("|--------------|--------------------------------|----------|")
        print("| kolors       | 快手可图，高质量（默认）        | 中英文   |")
        print("| qwen-image   | 通义千问，下载量230万+          | 中英文   |")
        print("| flux-dev     | FLUX.1-dev，艺术创作            | 英文     |")
        print("| flux-schnell | FLUX.1 schnell，快速            | 英文     |")
        print("| sd-x1        | SDXL，高质量艺术                | 英文     |")
        print()
        print("Usage: python generate_api.py --prompt '描述' --model kolors")
        return
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"Private Art Assistant - Cloud API Mode")
    print(f"=" * 50)
    print(f"Prompt: {args.prompt}")
    print(f"Model: {args.model}")
    print(f"Size: {args.size}")
    print(f"=" * 50)
    
    # Get API Key
    api_key = args.api_key or os.environ.get('MODELSCOPE_API_KEY')
    if not api_key:
        print("\n❌ Error: MODELSCOPE_API_KEY not set!")
        print("\nPlease set your API key:")
        print("  1. Get your API key from: https://modelscope.cn/my/myaccesstoken")
        print("  2. Set environment variable:")
        print("     Windows: set MODELSCOPE_API_KEY=your_key_here")
        print("     Linux/Mac: export MODELSCOPE_API_KEY=your_key_here")
        print("  3. Or pass directly: python generate_api.py --api-key YOUR_KEY --prompt '描述'")
        return
    
    try:
        import requests
        from PIL import Image
        from io import BytesIO
        
        # API endpoint
        url = 'https://api-inference.modelscope.cn/v1/images/generations'
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': args.model,
            'prompt': args.prompt,
            'negative_prompt': args.negative_prompt if args.negative_prompt else None,
            'n': args.count,
            'size': args.size
        }
        
        print("\n🔄 Generating image via ModelScope API...")
        start_time = time.time()
        
        # Send request with retry
        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            data = response.json()
            
            if 'images' in data and data['images']:
                image_url = data['images'][0]['url']
                
                # Download and save image
                img_response = requests.get(image_url, timeout=30)
                image = Image.open(BytesIO(img_response.content))
                
                # Save image
                timestamp = int(time.time())
                filename = f"generated_{timestamp}.png"
                filepath = output_dir / filename
                image.save(str(filepath))
                
                elapsed = time.time() - start_time
                
                print(f"\n✅ Generation Complete!")
                print(f"- Output: {filepath}")
                print(f"- Time: {elapsed:.2f}s")
                print(f"- Model: {args.model}")
                print(f"- Size: {args.size}")
                print(f"- Prompt: {args.prompt}")
                return
            
            elif 'error' in data:
                print(f"Attempt {attempt + 1} failed: {data['error']}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    print(f"\n❌ Error: {data['error']}")
                    return
            else:
                print(f"Unexpected response: {data}")
                return
                
    except ImportError as e:
        print(f"\n❌ Error: Missing dependency - {e}")
        print("Please install: pip install requests Pillow")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()