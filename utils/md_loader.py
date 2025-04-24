import frontmatter
from pathlib import Path
import os
import markdown
from bs4 import BeautifulSoup

# Парсит Markdown в структурированный текст с иерархией h2 → h3 + списки
def parse_markdown_to_text(content: str) -> dict:
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, 'html.parser')

    sections = {}
    current_section = None
    buffer = []

    for tag in soup.find_all(['h1', 'h2', 'h3', 'ul']):
        if tag.name in ['h1', 'h2']:
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = tag.get_text(strip=True)
            buffer = [f"📍 {current_section}"]
        elif tag.name == 'h3':
            buffer.append(tag.get_text(strip=True))
        elif tag.name == 'ul':
            for li in tag.find_all('li'):
                buffer.append(f"• {li.get_text(strip=True)}")
    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections

# Парсит один Markdown-файл
def parse_program_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    program_data = {
        "title": post.get("title"),
        "description": post.get("description"),
        "duration": post.get("duration"),
        "duration_weeks": post.get("duration_weeks"),
        "gender": post.get("gender"),
        "age_group": post.get("age_group"),
        "level": post.get("level"),
        "sections": parse_markdown_to_text(post.content)
    }

    return program_data

# Загружает все программы из папки
def load_all_programs():
    programs_dir = Path('data/programs')
    result = {}

    for file in os.listdir(programs_dir):
        file_path = programs_dir / file
        if file_path.suffix == '.md':
            program_name = Path(file).stem
            print(f"Загружена программа: {program_name}")
            result[program_name] = parse_program_md(file_path)

    print(f"Всего загружено программ: {len(result)}")
    return result
