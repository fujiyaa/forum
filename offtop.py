import requests
from bs4 import BeautifulSoup
import certifi

def get_forum_text(topic_id, max_batches=10):
    all_text = []
    last_post = 1  # Начинаем с первого поста
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    seen_posts = set()  # Чтобы отслеживать уникальные посты

    for batch in range(max_batches):
        print(f"🔄 Загружается партия {batch + 1} (посты {last_post}–{last_post + 49})...")
        url = f"https://osu.ppy.sh/community/forums/topics/{topic_id}?n={last_post}"

        try:
            response = requests.get(url, headers=headers, verify=certifi.where(), timeout=10)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            print(f"⚠️ SSL ошибка, пробуем без верификации...")
            response = requests.get(url, headers=headers, verify=False, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при загрузке: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", class_="forum-post__body")

        unique_posts = []
        for post in posts:
            text = post.get_text(strip=True, separator="\n")
            if text not in seen_posts:  # Проверяем, не повторяется ли пост
                unique_posts.append(text)
                seen_posts.add(text)

        if not unique_posts:
            print(f"✅ Конец темы: больше новых постов нет.")
            break

        all_text.extend(unique_posts)
        print(f"✅ Загружено {len(unique_posts)} уникальных постов.")

        # Если загружено меньше 50 уникальных постов, значит, конец темы
        if len(unique_posts) < 50:
            print(f"✅ Выгружено менее 50 новых постов, вероятно, достигнут конец темы.")
            break

        last_post += 50  # Переход к следующему блоку постов

    return "\n\n".join(all_text)

# Использование
topic_id = 1107801  # ID темы на форуме
forum_text = get_forum_text(topic_id, max_batches=200)

# Сохранение в файл
with open("forum_text.txt", "w", encoding="utf-8") as f:
    f.write(forum_text)

print("🎉 Сбор текста завершён, результат сохранён в forum_text.txt")
