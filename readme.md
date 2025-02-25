## WordsMiner - 新闻文本分析词云生成工具

### 📌 项目简介

WordsMiner 是一个基于 Python 的新闻文本分析工具，能够自动抓取新闻网页内容，提取关键词并生成可视化词云。适用于新闻工作者、研究人员进行文本快速分析和内容摘要。

### ✨ 核心功能

🕸️ 网页内容抓取（支持越牛新闻/政府网站双模式）

🔠 中文分词与停用词过滤

🎨 可定制化词云生成（颜色主题/字体/尺寸）

💾 词云图片保存功能

🖥️ 直观的 GUI 操作界面

📦 环境要求：Python 3.9+

推荐环境：Windows 10/11 或 macOS 12+

### 📦基础依赖

pip install requests jieba matplotlib beautifulsoup4 wordcloud pillow

### 🖥️面板介绍

左侧控制面板：输入 URL/选择配置文件

右侧展示区：实时显示生成词云

主题切换：支持"抹茶绿"/"标准白"双主题

### 🛠️ 技术栈

核心框架：Tkinter GUI

文本处理：jieba 中文分词

网页解析：BeautifulSoup4

数据可视化：WordCloud + Matplotlib

流程图生成：Graphviz

### 📂 项目结构

WordsMiner/
├── assets/ # 静态资源
│ ├── fonts/ # 字体文件
│ └── stopwords/ # 停用词库
├── temp/ # 临时文件
├── WordsMinerGUI.py # 主界面逻辑
├── WordsMinerCore.py # 核心处理逻辑

### 🤝 参与贡献

欢迎通过 Issue 或 Pull Request 参与项目改进：

Fork 本仓库

创建特性分支 (git checkout -b feature/your-feature)

提交更改 (git commit -m 'Add some feature')

推送分支 (git push origin feature/your-feature)

创建 Pull Request

代码规范要求：

使用 Google 风格 Python 注释

重要函数需包含 docstring

变量命名采用下划线格式

### 📄 许可证

本项目采用 MIT License

温馨提示：使用前请确保已获得目标网站的爬虫授权，本工具仅用于学习交流，禁止用于商业用途。
