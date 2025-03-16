"""
Odoo模块翻译工具 - 将POT文件自动翻译成中文(zh_CN.po)的Python工具

使用说明:
---------
1. 创建并配置Python虚拟环境:
   # 安装虚拟环境工具
   sudo apt install python3-venv
   
   # 创建虚拟环境
   python3 -m venv ~/translate_env
   
   # 激活虚拟环境
   source ~/translate_env/bin/activate
   
   # 安装必要的包
   pip install googletrans==3.1.0a0

2. 准备翻译模板:
   # 对于非Odoo原生的第三方应用或模块:
   - 进入Odoo开发者模式
   - 在"翻译"菜单中导出最新的翻译模板(.pot文件)
   - 将导出的.pot文件替换到模块的i18n目录中
   注意：这一步很重要，因为第三方模块的i18n目录中的pot文件可能是旧版本的
   （例如：应用是18.0版本，但pot文件可能还是15.0版本的）

3. 运行翻译程序:
   # 翻译当前目录下所有模块
   python translate_po.py --dir .
   
   # 翻译指定目录下所有模块
   python translate_po.py --dir /path/to/modules
   
   # 翻译指定模块
   python translate_po.py --dir /path/to/modules --module module_name

4. 完成后退出虚拟环境:
   deactivate

注意事项:
---------
1. 确保运行程序前已激活虚拟环境
2. 程序会自动查找目录下包含 __manifest__.py 的Odoo模块
3. 每个模块必须有 i18n 目录和对应的 .pot 文件
4. 翻译结果将保存为 i18n/zh_CN.po 文件
5. 对于第三方模块，建议先从Odoo系统中导出最新的翻译模板，以确保翻译的准确性和完整性
6. 程序会自动跳过以下类型的词条：
   - 包含Python代码的字符串
   - 包含HTML/XML标签的字符串
   - 纯数字或符号的字符串
   - 空字符串
7. 程序会保持英文引号格式，不会将引号转换为中文引号
8. 程序会保留已有的翻译内容，不会重复翻译或覆盖已翻译的词条
9. 程序会保持原文中换行符(\n)的格式不变
"""
import re
from googletrans import Translator
import time
import os
import argparse
import glob

def find_pot_files(base_dir):
    """
    遍历目录查找所有的POT文件
    
    Args:
        base_dir (str): 基础目录路径
        
    Returns:
        list: 包含所有找到的POT文件信息的列表，每项为(模块路径, pot文件路径)
    """
    pot_files = []
    
    # 查找所有可能的Odoo模块目录（包含__manifest__.py的目录）
    for manifest_path in glob.glob(os.path.join(base_dir, "*/__manifest__.py")):
        module_dir = os.path.dirname(manifest_path)
        module_name = os.path.basename(module_dir)
        i18n_dir = os.path.join(module_dir, "i18n")
        
        # 检查是否存在i18n目录
        if os.path.exists(i18n_dir):
            # 查找POT文件
            pot_path = os.path.join(i18n_dir, f"{module_name}.pot")
            if os.path.exists(pot_path):
                pot_files.append((module_dir, pot_path))
    
    return pot_files

def should_translate(text):
    """
    判断文本是否需要翻译
    
    Args:
        text (str): 待判断的文本
        
    Returns:
        bool: True表示需要翻译，False表示不需要翻译
    """
    # 空字符串不翻译
    if not text:
        return False
        
    # 包含Python代码的不翻译
    if any(code_sign in text for code_sign in [
        '(', ')', '_', '{', '}', '+', '=', '[', ']'
    ]):
        return False
        
    包含HTML/XML标签的不翻译
    if any(html_sign in text for html_sign in [
        '<', '>', '/', '</', '/>', 'style=', 'class='
    ]):
        return False
        
    # 纯数字或符号的不翻译
    if all(char.isdigit() or char in '.,:-_/\\' for char in text.strip()):
        return False
        
    return True

def translate_po_file(input_file, output_file):
    """
    将PO文件从英文翻译成中文
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    # 读取现有的翻译（如果存在）
    existing_translations = {}
    if os.path.exists(output_file):
        print(f"发现现有翻译文件: {output_file}")
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
            # 提取现有的msgid和msgstr对
            existing_pairs = re.finditer(r'msgid "(.*?)"\nmsgstr "(.*?)"', existing_content, re.DOTALL)
            for pair in existing_pairs:
                if pair.group(1) and pair.group(2):  # 只保存非空翻译
                    existing_translations[pair.group(1)] = pair.group(2)
        print(f"已加载 {len(existing_translations)} 个现有翻译")
        
    # 读取源文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建翻译器实例
    translator = Translator()
    
    # 使用正则表达式，匹配所有msgid和msgstr对
    pattern = r'(msgid ")(.*?)(")\n(msgstr ")(.*?)(")'
    
    def translate_match(match):
        nonlocal current_count
        english_text = match.group(2)
        existing_translation = match.group(5)
        
        # 如果是空字符串，直接返回原文
        if not english_text:
            return match.group(0)
            
        # 如果在现有翻译中找到，使用现有翻译
        if english_text in existing_translations:
            return f'{match.group(1)}{english_text}{match.group(3)}\nmsgstr "{existing_translations[english_text]}"'
            
        # 如果已经有翻译，保留现有翻译
        if existing_translation:
            return match.group(0)
            
        # 判断是否需要翻译
        if not should_translate(english_text):
            return match.group(0)
            
        try:
            # 翻译成中文
            chinese_text = translator.translate(english_text, dest='zh-cn').text
            
            # 将翻译结果中的中文引号替换回英文引号
            chinese_text = chinese_text.replace('“', '"').replace('”', '"')
            chinese_text = chinese_text.replace('‘', "'").replace('’', "'")

            # 修复换行符，确保保持 \n 的格式
            chinese_text = chinese_text.replace('\ n', '\n').replace(' \n', '\n')
            
            # 添加延迟以避免请求过快
            time.sleep(0.3)
            
            current_count += 1
            print(f"[{current_count}/{total_untranslated}] 翻译: {english_text} -> {chinese_text}")
            
            return f'{match.group(1)}{english_text}{match.group(3)}\nmsgstr "{chinese_text}"'
        except Exception as e:
            print(f"翻译出错: {english_text}")
            print(f"错误信息: {str(e)}")
            return match.group(0)
    
    # 计算需要翻译的总数（排除已翻译和不需要翻译的词条）
    matches = list(re.finditer(pattern, content, flags=re.DOTALL))
    total_untranslated = sum(1 for m in matches 
                            if should_translate(m.group(2)) 
                            and not m.group(5)  # msgstr为空
                            and m.group(2) not in existing_translations)  # 不在现有翻译中
    current_count = 0
    
    print(f"共发现 {total_untranslated} 个需要翻译的词条")
    
    # 替换所有匹配项
    translated_content = re.sub(pattern, translate_match, content, flags=re.DOTALL)
    
    # 修改文件头信息
    translated_content = translated_content.replace(
        '"Project-Id-Version: Odoo Server',
        '"Project-Id-Version: Odoo Server\n"'
        '"Language: zh_CN\\n"'
    )
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存翻译后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)
        
    # 显示最终统计信息
    print(f"\n翻译统计:")
    print(f"总词条数: {total_untranslated}")
    print(f"成功翻译: {current_count}")
    print(f"未翻译/失败: {total_untranslated - current_count}")
    
    # 如果有未翻译的词条，给出提示
    if current_count < total_untranslated:
        print("\n注意: 有部分词条未能成功翻译，请检查输出文件并手动处理这些词条。")

def main():
    parser = argparse.ArgumentParser(description='将PO文件从英文翻译成中文')
    parser.add_argument('--dir', '-d', default='.',
                        help='Odoo模块所在的基础目录路径')
    parser.add_argument('--module', '-m',
                        help='指定要翻译的模块名称，不指定则翻译所有模块')
    
    args = parser.parse_args()
    
    try:
        # 查找所有POT文件
        pot_files = find_pot_files(args.dir)
        
        if not pot_files:
            print(f"在目录 {args.dir} 中未找到任何可翻译的模块")
            return
        
        print(f"找到 {len(pot_files)} 个可翻译的模块:")
        for module_dir, pot_path in pot_files:
            module_name = os.path.basename(module_dir)
            print(f"- {module_name}")
        
        # 如果指定了模块名，只翻译指定模块
        if args.module:
            pot_files = [(d, p) for d, p in pot_files if os.path.basename(d) == args.module]
            if not pot_files:
                print(f"未找到指定的模块: {args.module}")
                return
        
        print("\n开始翻译...")
        
        # 遍历翻译每个模块
        for module_dir, pot_path in pot_files:
            module_name = os.path.basename(module_dir)
            output_path = os.path.join(module_dir, "i18n", "zh_CN.po")
            
            print(f"\n正在翻译模块: {module_name}")
            print(f"输入文件: {pot_path}")
            print(f"输出文件: {output_path}")
            
            translate_po_file(pot_path, output_path)
            print(f"模块 {module_name} 翻译完成")
        
        print("\n所有模块翻译完成！")
        
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

if __name__ == '__main__':
    main() 
