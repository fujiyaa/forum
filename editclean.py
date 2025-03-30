import os
import re

def process_txt_files(directory):
    pattern = re.compile(
        r"^Last edited by\n"  # Первая строка
        r".+\n"  # Вторая строка (любое имя)
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}\n"  # Третья строка (дата)
        r", edited \d+ time(?:s)? in total\.$",  # Четвертая строка (редактирования)
        re.MULTILINE
    )
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            new_content = re.sub(pattern, "", content)
            
            if new_content != content:  # Если были изменения, перезаписываем файл
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Обработан: {filename}")
            else:
                print(f"Без изменений: {filename}")

# Укажи путь к папке с txt файлами
folder_path = "I:\OT"
process_txt_files(folder_path)
