#!/usr/bin/env python3
"""去除 Markdown 文件的 frontmatter 和 HTML 标签，输出纯文本供 TTS 使用。"""
import sys
import re

def strip_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. 去除 YAML frontmatter (--- ... ---)
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    
    # 2. 去除 HTML 标签 (<audio>, <source>, <div> 等)
    text = re.sub(r'<[^>]+>', '', text)
    
    # 2.5. 去除代码块（```...``` 和 ``...``）
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'``[\s\S]*?``', '', text)
    
    # 3. 去除 Markdown 格式标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)       # *italic*
    text = re.sub(r'`([^`]+)`', r'\1', text)       # `code`
    text = re.sub(r'~~(.*?)~~', r'\1', text)       # ~~strikethrough~~
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)     # images
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # [text](url) → text
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # headings
    text = re.sub(r'^>+\s?', '', text, flags=re.MULTILINE)      # blockquotes
    text = re.sub(r'-{3,}', '', text)              # horizontal rules
    text = re.sub(r'\|\s*', '', text)              # table pipes
    text = re.sub(r'^\s*[-*+]\s+', '• ', text, flags=re.MULTILINE)  # list items
    
    # 4. 压缩多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 5. 输出到 scripts/_tts_<filename>.txt
    import os
    out_dir = os.path.join(os.path.dirname(filepath), os.pardir, 'scripts')
    basename = os.path.splitext(os.path.basename(filepath))[0]
    out_path = os.path.join(out_dir, f'_tts_{basename}.txt')
    
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else out_dir, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text.strip())
    
    print(f'✅ {out_path}')

if __name__ == '__main__':
    strip_md(sys.argv[1])
