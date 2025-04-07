import os
import re
import csv
from collections import defaultdict

def remove_topic_starter(directory):
    pattern = re.compile(r"^Topic Starter\n", re.MULTILINE)
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            new_content = re.sub(pattern, "", content)
            
            if new_content != content:  
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Changed: {filename}")
            else:
                print(f"Skipped: {filename}")

def remove_reply(directory):
    pattern = re.compile(
        r"^Last edited by\n" 
        r".+\n" 
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}\n" 
        r", edited \d+ time(?:s)? in total\.$", 
        re.MULTILINE
    )
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            new_content = re.sub(pattern, "", content)
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Обработан: {filename}")
            else:
                print(f"Без изменений: {filename}")

def merge_txt_files(directory, output_file):
    # files = sorted(
    #     [f for f in os.listdir(directory) if f.startswith("forum_") and f.endswith(".txt")],
    #     key=lambda x: (
    #         int(re.search(r"forum_(\d+)", x).group(1)) if re.search(r"forum_(\d+)", x) else float("inf"),
    #         x
    #     )
    # )

    files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".txt")]
    )
    
    # with open(output_file, "w", encoding="utf-8") as outfile:
    #     for filename in files:
    #         filepath = os.path.join(directory, filename)
            
    #         with open(filepath, "r", encoding="utf-8") as infile:
    #             content = infile.read()
                               
    #             content = re.sub(r"(\S)(?:\n\S){4,}", r"\1", content)
    #             if content.strip():
    #                 outfile.write(content + "\n\n")
    #                 print(f"Добавлено из {filename}")
    #             else:
    #                 print(f"Пропущен пустой {filename}")
    #             outfile.write(content + "\n\n")  
    #             print(f"Добавлен: {filename}")
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file in files:
            with open(os.path.join(directory, file), "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")

    print(f"Merged and Saved as {output_file}")

def to_csv_statistics(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}")

    nickname_counts = defaultdict(int)

    i = 0
    while i < len(lines) - 1:
        nickname = lines[i].strip()
        date = lines[i + 1].strip()
        
        if date_pattern.fullmatch(date):
            nickname_counts[nickname] += 1
            i += 2  
        else:
            i += 1 

    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nickname", "Count"])
        
        for nickname, count in sorted(nickname_counts.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([nickname, count])

folder_path = "I:\OT\master\\"
output_filename = "оффтоп - часть XX.txt"

remove_reply(folder_path)
remove_topic_starter(folder_path)
merge_txt_files(folder_path, output_filename)

if(input('Create .csv stats?   1 - Yes / 2 - No\n')=='1'):
    to_csv_statistics(output_filename)


print('Job done')
