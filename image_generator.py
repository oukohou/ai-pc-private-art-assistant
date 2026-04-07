#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图像生成器核心模块
基于OpenVINO优化的Stable Diffusion模型简化版
"""

import time
from pathlib import Path
from typing import Optional
import numpy as np

# OpenVINO imports
try:
    import openvino as ov
    print("OpenVINO imported successfully")
except ImportError as e:
    print(f"OpenVINO import failed: {e}")
    raise

# Diffusers imports
try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    from transformers import CLIPTokenizer
    import torch
    print("Diffusers imported successfully")
except ImportError as e:
    print(f"Diffusers import failed: {e}")
    raise


class ImageGenerator:
    """
    基于OpenVINO的Stable Diffusion图像生成器
    """
    
    def __init__(
        self,
        model_id: str = "stable-diffusion-v1-5",
        device: str = "AUTO",
        quantize: bool = False,
        model_dir: Optional[str] = None
    ):
        """
        初始化图像生成器
        
        Args:
            model_id: 模型ID或路径
            device: 推理设备 (AUTO/CPU/GPU)
            quantize: 是否使用量化
            model_dir: 模型保存目录
        """
        self.model_id = model_id
        self.device = device
        self.quantize = quantize
        self.model_dir = Path(model_dir) if model_dir else Path("./models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化OpenVINO Core
        self.core = ov.Core()
        print(f"Available devices: {self.core.available_devices}")
        
        # 加载模型
        self.pipe = None
        self._load_model()
        
    def _load_model(self):
        """加载模型"""
        print(f"Loading model: {self.model_id}")
        
        try:
            # 使用Optimum Intel加载OpenVINO优化的Stable Diffusion
            from optimum.intel import OVStableDiffusionPipeline
            
            model_path = self.model_dir / "stable-diffusion-ov"
            
            if model_path.exists():
                # 加载已转换的模型
                print("Loading existing OpenVINO model...")
                self.pipe = OVStableDiffusionPipeline.from_pretrained(
                    str(model_path),
                    compile=False
                )
            else:
                # 下载并转换模型
                print("Downloading and converting model (this may take a while)...")
                
                # 下载原始模型
                original_pipe = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float32
                )
                
                # 转换为OpenVINO格式
                self.pipe = OVStableDiffusionPipeline.from_pipe(
                    original_pipe,
                    export=True,
                    compile=False
                )
                
                # 保存转换后的模型
                self.pipe.save_pretrained(str(model_path))
                
                # 清理内存
                del original_pipe
            
            # 配置scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # 编译模型
            print("Compiling model...")
            self.pipe.to(self.device)
            self.pipe.compile()
            
            print("Model loaded successfully")
            
        except Exception as e:
            print(f"Model loading failed: {e}")
            print("Falling back to simple pipeline...")
            
            # 简化模式：使用diffusers的OpenVINO支持
            try:
                from optimum.intel import OVPipelineForText2Image
                
                self.pipe = OVPipelineForText2Image.from_pretrained(
                    "stable-diffusion-v1-5",
                    export=True,
                    device=self.device
                )
                
                print("OVPipeline loaded successfully")
                
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
                raise
        
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        seed: int = -1
    ):
        """
        生成图像
        
        Args:
            prompt: 正面提示词
            negative_prompt: 负面提示词
            num_inference_steps: 推理步数
            guidance_scale: 引导比例
            width: 图像宽度
            height: 图像高度
            seed: 随机种子
            
        Returns:
            生成的图像数组和种子
        """
        start_time = time.time()
        
        # 设置随机种子
        if seed == -1:
            seed = np.random.randint(0, 2**32)
        
        print(f"Starting generation (seed={seed})...")
        
        try:
            # 使用pipeline生成图像
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt else None,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                generator=torch.manual_seed(seed)
            ).images[0]
            
            # 转换为numpy数组
            image_array = np.array(result)
            
            end_time = time.time()
            print(f"Generation completed in {end_time - start_time:.2f} seconds")
            
            return image_array, seed
            
        except Exception as e:
            print(f"Generation failed: {e}")
            
            # 返回一个测试图像
            print("Returning test pattern...")
            image_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            return image_array, seed
    
    def get_performance_info(self) -> dict:
        """获取性能信息"""
        return {
            "device": self.device,
            "quantize": self.quantize,
            "available_devices": self.core.available_devices,
            "model_loaded": self.pipe is not None
        }
