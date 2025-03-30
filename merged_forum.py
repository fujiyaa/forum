import os
import re
def remove_topic_starter(directory):
    pattern = re.compile(r"^Topic Starter\n", re.MULTILINE)
    
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

def merge_txt_files(directory, output_file):
    files = sorted(
        [f for f in os.listdir(directory) if f.startswith("forum_") and f.endswith(".txt")],
        key=lambda x: (
            int(re.search(r"forum_(\d+)", x).group(1)) if re.search(r"forum_(\d+)", x) else float("inf"),
            x
        )
    )
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in files:
            filepath = os.path.join(directory, filename)
            
            with open(filepath, "r", encoding="utf-8") as infile:
                content = infile.read()
                
                # Удаляем все, кроме первого символа, в последовательностях из 5+ символов с переносами
                content = re.sub(r"(\S)(?:\n\S){4,}", r"\1", content)
                
                outfile.write(content + "\n\n")  # Добавляем два переноса строки между файлами
                print(f"Добавлен: {filename}")
    
    print(f"Объединённый файл сохранён как {output_file}")

# Укажи путь к папке с txt файлами и имя выходного файла
folder_path = "I:\OT"
output_filename = "оффтоп - часть 18.txt"

merge_txt_files(folder_path, output_filename)
remove_topic_starter(folder_path)
