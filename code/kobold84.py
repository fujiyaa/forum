import re

def filter_messages(input_file, output_file, target_nick):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = infile.read()
    
    pattern = re.compile(r'(^.+?)\n(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})\n(.*?)\n\n', re.DOTALL | re.MULTILINE)
    
    filtered_messages = []
    count = 0
    for match in pattern.finditer(data):
        nick, timestamp, message = match.groups()
        if nick == target_nick:
            filtered_messages.append(f"{nick}\n{timestamp}\n{message}\n\n")
            count += 1
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_messages)
    
    print(f"Сообщений от {target_nick}: {count}")



filter_messages('.//offtop/txt/text.txt', 'filtered.txt', 'Fujiya')
