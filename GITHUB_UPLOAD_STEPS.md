# GitHub上传详细步骤

## 步骤1: 在GitHub上创建仓库

### 1.1 访问GitHub
- 打开浏览器访问: https://github.com
- 登录您的GitHub账号

### 1.2 创建新仓库
1. 点击右上角 **+** 号
2. 选择 **New repository**
3. 填写信息:
   - **Repository name**: `ai-pc-private-art-assistant`
   - **Description**: 基于OpenVINO的端侧AI绘画助手 - Intel AI PC创新应用比赛作品
   - 选择 **Public** (公开)
   - **不要勾选** "Add a README file"
   - **不要勾选** "Add .gitignore"
   - **不要勾选** "Choose a license"
4. 点击 **Create repository**

### 1.3 获取仓库地址
创建完成后，复制显示的仓库地址:
```
https://github.com/您的用户名/ai-pc-private-art-assistant.git
```

---

## 步骤2: 推送本地代码到GitHub

### 2.1 配置Git远程仓库

在命令行中执行以下命令（替换为您的用户名）:

```bash
cd "e:/interest/contest/modelscope/Intel AI PC-openclaw"

# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-pc-private-art-assistant.git

# 验证远程仓库
git remote -v
```

### 2.2 推送代码

```bash
# 重命名分支为main
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

### 2.3 验证上传成功

1. 刷新GitHub页面
2. 应该能看到所有代码文件
3. 检查文件列表:
   - main.py
   - image_generator.py
   - gradio_interface.py
   - openclaw_skill.py
   - requirements.txt
   - README.md
   - technical_article.md
   - 其他文档

---

## 步骤3: 复制仓库链接

上传成功后，复制仓库首页的URL:
```
https://github.com/YOUR_USERNAME/ai-pc-private-art-assistant
```

这个链接将用于比赛提交。

---

## 常见问题

### Q1: 推送时提示需要登录

**解决**: Git会弹出窗口让您输入GitHub用户名和密码，或使用Token认证。

### Q2: 提示权限不足

**解决**: 
1. 检查仓库是否创建正确
2. 确认您有写入权限
3. 或者使用HTTPS方式推送

### Q3: 推送失败

**解决**:
```bash
# 强制推送（如果确定本地代码是最新的）
git push -f origin main
```

---

## 下一步

完成GitHub上传后，请继续:
1. 在魔搭社区发布技术文章
2. 在比赛页面提交作品

详细步骤请参考 SUBMISSION_GUIDE.md
