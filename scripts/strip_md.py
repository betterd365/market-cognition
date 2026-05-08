#!/usr/bin/env python3
"""去除 Markdown 文件的 frontmatter 和 HTML 标签，输出纯文本供 TTS 使用。
Usage: python scripts/strip_md.py _posts/2026-05-08-article.md
Output: scripts/_tts_2026-05-08-article.txt
"""
import sys
import re

def strip_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. 去除 YAML frontmatter (--- ... ---)
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    
    # 2. 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 3. 去除 Markdown 格式标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>+\s?', '', text, flags=re.MULTILINE)
    text = re.sub(r'-{3,}', '', text)
    text = re.sub(r'\|\s*', '', text)
    text = re.sub(r'^\s*[-*+]\s+', '? ', text, flags=re.MULTILINE)
    
    # 4. 去除参考来源区块（"📎 参考来源" 及之后所有内容）
    text = re.split(r'(?:📎\s*)?参考来源', text, maxsplit=1)[0]
    
    # 5. 压缩多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 6. 输出
    import os
    out_dir = os.path.join(os.path.dirname(filepath), os.pardir, 'scripts')
    basename = os.path.splitext(os.path.basename(filepath))[0]
    out_path = os.path.join(out_dir, f'_tts_{basename}.txt')
    
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else out_dir, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text.strip())
    
    print(f'OK {out_path}')

if __name__ == '__main__':
    strip_md(sys.argv[1])
