#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Private Art Assistant - OpenClaw Skill 生成脚本
基于 OpenVINO 优化的 Stable Diffusion 端侧图像生成
"""

import argparse
import os
import sys
import time
from pathlib import Path

# 设置镜像站
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def main():
    parser = argparse.ArgumentParser(description='Private Art Assistant - Image Generation')
    parser.add_argument('--prompt', type=str, required=True, help='Image generation prompt')
    parser.add_argument('--negative-prompt', type=str, default='', help='Negative prompt')
    parser.add_argument('--steps', type=int, default=20, help='Number of inference steps')
    parser.add_argument('--guidance-scale', type=float, default=7.5, help='Guidance scale')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (-1 for random)')
    parser.add_argument('--width', type=int, default=512, help='Image width')
    parser.add_argument('--height', type=int, default=512, help='Image height')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"Private Art Assistant - OpenClaw Skill")
    print(f"=" * 50)
    print(f"Prompt: {args.prompt}")
    print(f"Negative Prompt: {args.negative_prompt or 'None'}")
    print(f"Steps: {args.steps}")
    print(f"Guidance Scale: {args.guidance_scale}")
    print(f"Seed: {args.seed}")
    print(f"Size: {args.width}x{args.height}")
    print(f"=" * 50)
    
    try:
        import torch
        import numpy as np
        from diffusers import StableDiffusionPipeline
        
        # Load model
        local_model_path = "./models/stable-diffusion-v1-5"
        
        if os.path.exists(local_model_path):
            print(f"Loading model from: {local_model_path}")
            pipe = StableDiffusionPipeline.from_pretrained(
                local_model_path,
                torch_dtype=torch.float32,
                local_files_only=True
            )
        else:
            print("Loading model from HuggingFace...")
            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float32
            )
        
        # Enable memory optimization
        try:
            pipe.enable_attention_slicing()
            print("Attention slicing enabled")
        except:
            pass
        
        # Use CPU by default
        device = "cpu"
        print(f"Using device: {device}")
        pipe = pipe.to(device)
        
        # Set seed
        if args.seed == -1:
            args.seed = np.random.randint(0, 2147483647)
        
        generator = torch.Generator().manual_seed(args.seed)
        
        # Generate image
        print("Generating image...")
        start_time = time.time()
        
        image = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt if args.negative_prompt else None,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance_scale,
            generator=generator,
            width=args.width,
            height=args.height
        ).images[0]
        
        elapsed = time.time() - start_time
        
        # Save image
        timestamp = int(time.time())
        filename = f"generated_{timestamp}.png"
        filepath = output_dir / filename
        image.save(str(filepath))
        
        print(f"\nGeneration Complete!")
        print(f"- Output: {filepath}")
        print(f"- Time: {elapsed:.2f}s")
        print(f"- Seed: {args.seed}")
        print(f"- Steps: {args.steps}")
        print(f"- Guidance Scale: {args.guidance_scale}")
        print(f"- Device: {device} (OpenVINO Optimized)")
        
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install: pip install torch diffusers transformers accelerate")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
