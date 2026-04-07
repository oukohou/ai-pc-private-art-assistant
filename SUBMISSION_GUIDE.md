# 比赛提交指南

## 比赛提交三步骤

### Step 1: 上传代码到GitHub (需要您的GitHub账号)

#### 方法一：使用GitHub网页（推荐新手）

1. **登录GitHub**
   - 访问 https://github.com
   - 登录您的账号（如果没有请先注册）

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 填写仓库信息：
     - **Repository name**: `ai-pc-private-art-assistant`
     - **Description**: `基于OpenVINO的端侧AI绘画助手 - Intel AI PC创新应用比赛作品`
     - **Public** (选择公开)
     - **不要**勾选 "Add a README file"（我们已有）
   - 点击 "Create repository"

3. **上传代码**
   - 在仓库页面点击 "uploading an existing file"
   - 拖拽以下文件到上传区域：
     ```
     main.py
     image_generator.py
     gradio_interface.py
     openclaw_skill.py
     requirements.txt
     README.md
     technical_article.md
     PROJECT_SUMMARY.md
     QUICKSTART.md
     test_project.py
     ```
   - 点击 "Commit changes"

4. **复制仓库地址**
   - 仓库创建完成后，复制仓库URL
   - 格式如：`https://github.com/您的用户名/ai-pc-private-art-assistant`

#### 方法二：使用Git命令行

```bash
# 1. 进入项目目录
cd "e:/interest/contest/modelscope/Intel AI PC-openclaw"

# 2. 初始化Git仓库（如果还没有）
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Intel AI PC创新应用比赛作品提交"

# 5. 添加远程仓库（创建仓库后使用）
git remote add origin https://github.com/您的用户名/ai-pc-private-art-assistant.git

# 6. 推送代码
git branch -M main
git push -u origin main
```

---

### Step 2: 发布技术文章到魔搭社区

1. **登录魔搭社区**
   - 访问 https://www.modelscope.cn
   - 登录您的账号

2. **进入个人中心**
   - 点击右上角头像 → "我的主页"

3. **发布文章**
   - 点击 "创作" → "写文章"
   - 填写文章信息：
     - **标题**: 【Intel AI PC】基于OpenVINO的端侧AI绘画助手实战
     - **分类**: 技术文章 / AI / OpenVINO
     - **标签**: OpenVINO, Stable Diffusion, AI PC, 端侧AI
   - 将 `technical_article.md` 的内容复制到编辑器
   - 添加代码块和图片
   - 点击 "发布"

4. **获取文章链接**
   - 发布后复制文章URL

---

### Step 3: 在比赛页面提交作品

1. **访问比赛页面**
   - 打开 https://modelscope.cn/events/196

2. **提交作品**
   - 点击 "立即报名" 或 "提交作品"
   - 填写信息：
     - **作品名称**: AI PC端侧私密绘画助手
     - **项目简介**: 基于OpenVINO的端侧AI绘画助手
     - **技术栈**: Python, OpenVINO, Stable Diffusion, Gradio
     - **GitHub仓库地址**: (填入Step 1的仓库地址)
     - **文章链接**: (填入Step 2的文章链接)
     - **创新点**:
       - 端侧大模型部署
       - 异构计算加速(CPU/GPU/NPU)
       - 隐私保护设计
       - OpenClaw技能封装
   - 点击 "提交"

---

## 需要您提供的信息

为了帮助您完成提交，请提供以下信息：

1. **GitHub用户名**: _______________
2. **是否需要我帮您创建仓库**: 是/否

3. **魔搭社区账号**: 是否已登录
4. **文章标题确认**: 【Intel AI PC】基于OpenVINO的端侧AI绘画助手实战

---

## 提交清单

- [ ] GitHub仓库已创建
- [ ] 代码已上传
- [ ] 技术文章已发布到魔搭社区
- [ ] 比赛页面已提交

---

## 截止日期提醒

**比赛截止日期**: 2026年4月30日

请尽快完成提交！

---

## 联系支持

如果遇到问题：
- 魔搭社区: https://www.modelscope.cn
- OpenVINO社区: 微信号 OpenVINO-China
