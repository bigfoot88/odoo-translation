# Odoo Translator / Odoo翻译工具

[English](#english) | [中文](#中文)

## English

A Python tool for automatically translating Odoo POT files to Chinese (zh_CN).

### Features
- Automatically translates POT files to Chinese
- Preserves existing translations
- Skips technical content (Python code, HTML tags, etc.)
- Maintains original formatting (quotes, line breaks)
- Supports batch translation of multiple modules
- Command-line interface for easy use

### Prerequisites
- Python 3.6+
- Virtual environment (recommended)
- Internet connection for Google Translate API

### Installation
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/odoo-translator.git
cd odoo-translator
```

2. Create and activate virtual environment:
```bash
# Install virtual environment tool
sudo apt install python3-venv

# Create virtual environment
python3 -m venv ~/translate_env

# Activate virtual environment
source ~/translate_env/bin/activate

# Install required packages
pip install googletrans==3.1.0a0
```

### Usage
1. For third-party modules, first export the latest translation template from Odoo:
   - Enter developer mode in Odoo
   - Go to "Translations" menu
   - Export the latest POT file
   - Replace the POT file in the module's i18n directory

2. Run the translator:
```bash
# Translate all modules in current directory
python translate_po.py --dir .

# Translate modules in specified directory
python translate_po.py --dir /path/to/modules

# Translate specific module
python translate_po.py --dir /path/to/modules --module module_name
```

3. Deactivate virtual environment when done:
```bash
deactivate
```

### Notes
- The tool will automatically skip:
  - Python code strings
  - HTML/XML tags
  - Pure numbers or symbols
  - Empty strings
- Maintains English quote format
- Preserves existing translations
- Keeps original line break format (\n)

## 中文

一个用于将Odoo POT文件自动翻译成中文(zh_CN)的Python工具。

### 功能特点
- 自动将POT文件翻译成中文
- 保留已有翻译内容
- 跳过技术性内容（Python代码、HTML标签等）
- 保持原始格式（引号、换行符）
- 支持批量翻译多个模块
- 命令行界面，使用方便

### 前置要求
- Python 3.6+
- 虚拟环境（推荐）
- 网络连接（用于Google翻译API）

### 安装
1. 克隆仓库：
```bash
git clone https://github.com/YOUR_USERNAME/odoo-translator.git
cd odoo-translator
```

2. 创建并激活虚拟环境：
```bash
# 安装虚拟环境工具
sudo apt install python3-venv

# 创建虚拟环境
python3 -m venv ~/translate_env

# 激活虚拟环境
source ~/translate_env/bin/activate

# 安装必要的包
pip install googletrans==3.1.0a0
```

### 使用方法
1. 对于第三方模块，首先从Odoo导出最新的翻译模板：
   - 进入Odoo开发者模式
   - 进入"翻译"菜单
   - 导出最新的POT文件
   - 替换模块i18n目录中的POT文件

2. 运行翻译程序：
```bash
# 翻译当前目录下所有模块
python translate_po.py --dir .

# 翻译指定目录下所有模块
python translate_po.py --dir /path/to/modules

# 翻译指定模块
python translate_po.py --dir /path/to/modules --module module_name
```

3. 完成后退出虚拟环境：
```bash
deactivate
```

### 注意事项
- 程序会自动跳过：
  - Python代码字符串
  - HTML/XML标签
  - 纯数字或符号
  - 空字符串
- 保持英文引号格式
- 保留已有翻译内容
- 保持原始换行符格式(\n)
