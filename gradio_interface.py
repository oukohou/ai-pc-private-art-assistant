#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gradio Web界面
为AI PC端侧私密绘画助手提供友好的用户界面
"""

import gradio as gr
import numpy as np
from PIL import Image
from typing import Optional
import time


class GradioInterface:
    """Gradio界面管理器"""
    
    def __init__(self, generator):
        self.generator = generator
        self.interface = None
        
    def generate_image(
        self,
        prompt,
        negative_prompt,
        steps,
        guidance_scale,
        width,
        height,
        seed
    ):
        """生成图像的回调函数"""
        if not prompt.strip():
            return None, "请输入提示词"
            
        try:
            # 调用生成器
            image_array, actual_seed = self.generator.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                seed=seed
            )
            
            # 转换为PIL Image
            image = Image.fromarray(image_array)
            
            # 生成性能信息
            info = f"""
生成成功！
- 随机种子: {actual_seed}
- 步数: {steps}
- 引导比例: {guidance_scale}
- 设备: {self.generator.device}
            """
            
            return image, info
            
        except Exception as e:
            return None, f"生成失败: {str(e)}"
    
    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
            title="Intel AI PC端侧私密绘画助手",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .title {
                text-align: center;
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 20px;
                color: white;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                margin-bottom: 30px;
                color: rgba(255, 255, 255, 0.8);
            }
            """
        ) as interface:
            # 标题
            gr.HTML("""
                <div class="title">🎨 Intel AI PC端侧私密绘画助手</div>
                <div class="subtitle">基于OpenVINO™优化的Stable Diffusion • 本地运行保护隐私</div>
            """)
            
            with gr.Row():
                # 左侧面板：参数设置
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 生成参数")
                    
                    prompt = gr.Textbox(
                        label="提示词 (Prompt)",
                        placeholder="例如: a beautiful sunset over mountains, high quality, detailed",
                        lines=3,
                        max_lines=5
                    )
                    
                    negative_prompt = gr.Textbox(
                        label="负面提示词 (Negative Prompt)",
                        placeholder="例如: low quality, blurry, bad anatomy",
                        lines=2,
                        value="low quality, blurry, bad anatomy, watermark, text, signature"
                    )
                    
                    with gr.Group():
                        gr.Markdown("#### ⚙️ 高级参数")
                        
                        with gr.Row():
                            steps = gr.Slider(
                                label="推理步数",
                                minimum=10,
                                maximum=50,
                                value=20,
                                step=1,
                                info="步数越多质量越高，但速度越慢"
                            )
                            
                            guidance_scale = gr.Slider(
                                label="引导比例",
                                minimum=1.0,
                                maximum=20.0,
                                value=7.5,
                                step=0.5,
                                info="越高越遵循提示词"
                            )
                        
                        with gr.Row():
                            width = gr.Dropdown(
                                label="宽度",
                                choices=[512, 768, 1024],
                                value=512,
                                info="图像宽度"
                            )
                            
                            height = gr.Dropdown(
                                label="高度",
                                choices=[512, 768, 1024],
                                value=512,
                                info="图像高度"
                            )
                        
                        seed = gr.Number(
                            label="随机种子 (-1为随机)",
                            value=-1,
                            precision=0,
                            info="固定种子可重现结果"
                        )
                    
                    generate_btn = gr.Button(
                        "🚀 生成图像",
                        variant="primary",
                        size="lg"
                    )
                    
                    # 性能信息
                    performance_info = gr.Markdown(
                        f"""
                        ### 📊 系统信息
                        - 推理设备: **{self.generator.device}**
                        - 量化优化: **{'启用' if self.generator.quantize else '未启用'}**
                        - 可用设备: {', '.join(self.generator.core.available_devices)}
                        """
                    )
                
                # 右侧面板：结果展示
                with gr.Column(scale=1):
                    gr.Markdown("### 🖼️ 生成结果")
                    
                    output_image = gr.Image(
                        label="生成的图像",
                        type="pil",
                        show_label=True,
                        show_download_button=True
                    )
                    
                    result_info = gr.Textbox(
                        label="生成信息",
                        lines=6,
                        interactive=False,
                        show_copy_button=True
                    )
                    
                    # 示例提示词
                    gr.Markdown("### 💡 示例提示词")
                    with gr.Group():
                        examples = [
                            "a beautiful sunset over mountains, high quality, detailed, 8k",
                            "a cute cat wearing a hat, cartoon style, colorful",
                            "futuristic cityscape, cyberpunk, neon lights, night",
                            "portrait of a beautiful woman, photography, soft lighting",
                            "a magical forest with glowing mushrooms, fantasy art"
                        ]
                        
                        example_dropdown = gr.Dropdown(
                            label="选择示例",
                            choices=examples,
                            value=examples[0],
                            interactive=True
                        )
                        
                        def load_example(example):
                            return example
                        
                        example_dropdown.change(
                            fn=load_example,
                            inputs=example_dropdown,
                            outputs=prompt
                        )
            
            # 绑定事件
            generate_btn.click(
                fn=self.generate_image,
                inputs=[
                    prompt,
                    negative_prompt,
                    steps,
                    guidance_scale,
                    width,
                    height,
                    seed
                ],
                outputs=[output_image, result_info]
            )
            
            # 示例画廊
            gr.Markdown("### 🎨 示例画廊 (点击可查看提示词)")
            
            gallery_examples = [
                ["example1.jpg", "a beautiful sunset over mountains, high quality, detailed"],
                ["example2.jpg", "a cute cat wearing a hat, cartoon style"],
                ["example3.jpg", "futuristic cityscape, cyberpunk, neon lights"],
                ["example4.jpg", "portrait of a beautiful woman, photography"],
                ["example5.jpg", "a magical forest with glowing mushrooms, fantasy"],
            ]
            
            gallery = gr.Dataset(
                components=[gr.Image(type="filepath", height=150), gr.Textbox(visible=False)],
                samples=gallery_examples,
                label="",
                headers=None,
                samples_per_page=5
            )
            
            def load_gallery_example(evt: gr.SelectData):
                return gallery_examples[evt.index][1]
            
            gallery.select(load_gallery_example, None, prompt)
            
            # 页脚
            gr.HTML("""
                <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <p>🚀 Powered by <strong>OpenVINO™</strong> | 🎨 Built for <strong>Intel AI PC</strong></p>
                    <p style="font-size: 0.9em; opacity: 0.8;">所有计算在本地完成，保护您的隐私数据</p>
                </div>
            """)
        
        self.interface = interface
        return interface


def create_gradio_interface(generator):
    """
    创建Gradio界面的工厂函数
    
    Args:
        generator: ImageGenerator实例
        
    Returns:
        Gradio Blocks界面
    """
    interface_manager = GradioInterface(generator)
    return interface_manager.create_interface()
