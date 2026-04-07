#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目测试脚本
验证AI PC端侧私密绘画助手是否正常工作
"""

import sys
import time
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    try:
        import openvino as ov
        print("OpenVINO导入成功")
    except Exception as e:
        print(f"✗ OpenVINO导入失败: {e}")
        return False
    
    try:
        from diffusers import StableDiffusionPipeline
        print("✓ Diffusers导入成功")
    except Exception as e:
        print(f"✗ Diffusers导入失败: {e}")
        return False
    
    try:
        from image_generator import ImageGenerator
        print("✓ ImageGenerator导入成功")
    except Exception as e:
        print(f"✗ ImageGenerator导入失败: {e}")
        return False
    
    try:
        from gradio_interface import create_gradio_interface
        print("✓ GradioInterface导入成功")
    except Exception as e:
        print(f"✗ GradioInterface导入失败: {e}")
        return False
    
    try:
        from openclaw_skill import OpenClawSkill
        print("✓ OpenClawSkill导入成功")
    except Exception as e:
        print(f"✗ OpenClawSkill导入失败: {e}")
        return False
    
    print("\n✓ 所有模块导入成功！")
    return True

def test_image_generator():
    """测试图像生成器初始化"""
    print("\n" + "=" * 60)
    print("测试ImageGenerator...")
    print("=" * 60)
    
    try:
        from image_generator import ImageGenerator
        
        # 创建实例（不加载实际模型）
        print("正在创建ImageGenerator实例...")
        generator = ImageGenerator(device="CPU")
        
        # 获取性能信息
        info = generator.get_performance_info()
        print(f"设备: {info['device']}")
        print(f"可用设备: {info['available_devices']}")
        print(f"模型加载: {info['model_loaded']}")
        
        print("\n✓ ImageGenerator测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ ImageGenerator测试失败: {e}")
        return False

def test_openclaw_skill():
    """测试OpenClaw Skill"""
    print("\n" + "=" * 60)
    print("测试OpenClawSkill...")
    print("=" * 60)
    
    try:
        from openclaw_skill import OpenClawSkill
        from image_generator import ImageGenerator
        
        # 创建生成器
        generator = ImageGenerator(device="CPU")
        
        # 创建技能
        skill = OpenClawSkill(generator)
        
        # 测试元数据
        metadata = skill.get_metadata()
        print(f"技能名称: {metadata['name']}")
        print(f"技能描述: {metadata['description']}")
        
        # 测试处理（模拟）
        test_input = {
            "prompt": "test",
            "steps": 1
        }
        result = skill.process(test_input)
        print(f"测试结果: {result['success']}")
        
        print("\n✓ OpenClawSkill测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ OpenClawSkill测试失败: {e}")
        return False

def test_files():
    """测试项目文件完整性"""
    print("\n" + "=" * 60)
    print("测试文件完整性...")
    print("=" * 60)
    
    required_files = [
        "main.py",
        "image_generator.py",
        "gradio_interface.py",
        "openclaw_skill.py",
        "requirements.txt",
        "README.md",
        "technical_article.md",
        "PROJECT_SUMMARY.md",
        "QUICKSTART.md"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} 缺失")
            all_exist = False
    
    if all_exist:
        print("\n✓ 所有必需文件都存在！")
    else:
        print("\n✗ 部分文件缺失！")
    
    return all_exist

def main():
    """主测试函数"""
    print("AI PC端侧私密绘画助手 - 项目测试")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 运行所有测试
    tests = [
        ("模块导入", test_imports),
        ("文件完整性", test_files),
        ("ImageGenerator", test_image_generator),
        ("OpenClawSkill", test_openclaw_skill),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name}测试发生异常: {e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 恭喜！所有测试通过，项目已准备好提交！")
        return 0
    else:
        print(f"\n⚠️ 有 {total - passed} 项测试失败，请检查")
        return 1

if __name__ == "__main__":
    sys.exit(main())
