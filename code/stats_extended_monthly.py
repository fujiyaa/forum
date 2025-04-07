import re
import csv
from collections import defaultdict

def to_csv_statistics(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}")

    month_nickname_counts = defaultdict(lambda: defaultdict(int))

    i = 0
    while i < len(lines) - 1:
        nickname = lines[i].strip()
        date = lines[i + 1].strip()

        match = date_pattern.fullmatch(date)
        if match:
            formatted_month = f"{match.group(1)}-{match.group(2)}"
            month_nickname_counts[formatted_month][nickname] += 1
            i += 2
        else:
            i += 1

    with open("output_m.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        all_nicknames = sorted(set(nick for month in month_nickname_counts for nick in month_nickname_counts[month]))

        writer.writerow(["Month"] + all_nicknames)

        for month in sorted(month_nickname_counts.keys()):
            row = [month] + [month_nickname_counts[month].get(nick, 0) for nick in all_nicknames]
            writer.writerow(row)

file_path = r"I://OT/master/text.txt"
to_csv_statistics(file_path)