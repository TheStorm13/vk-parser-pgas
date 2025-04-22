import time

from config import VK_TOKEN, VK_GROUP
from src.api_handlers.vk_api_handler import VKAPIHandler
from src.post_processing import PostProcessor, PostCategorizer, TableCreator


class MainLogic:
    def __init__(self):
        pass

    # Основной скрипт
    def run(self, fio, start_date, end_date, update_progress=None, group_url=VK_GROUP):  # Читаем токен из файла

        try:
            # Инициализация классов
            vk_handler = VKAPIHandler(VK_TOKEN)
            post_processor = PostProcessor(fio)
            post_categorizer = PostCategorizer()
            table_creator = TableCreator()

            start_time = time.time()
            # Получаем ID группы
            group_id = vk_handler.get_group_id(group_url)
            print("Время на Получаем ID группы: ", time.time() - start_time)
            start_time = time.time()

            # Получаем посты
            posts = vk_handler.get_posts(group_id, start_date, end_date, update_progress)
            print("Время на Получаем посты: ", time.time() - start_time)
            start_time = time.time()

            # Фильтруем посты
            filtered_posts = post_processor.filter_posts(posts)
            print("Время на Фильтруем посты: ", time.time() - start_time)
            start_time = time.time()

            # Группируем посты
            categorized_posts = post_categorizer.categorize_posts(filtered_posts, fio)
            print("Время на Группируем посты: ", time.time() - start_time)
            start_time = time.time()

            # Открываем файлы для записи
            with open("posts.txt", "w", encoding="utf-8") as posts_file:
                with open("for_word_file.txt", "w", encoding="utf-8") as for_word_file:
                    # Выводим результаты в консоль и записываем в файл
                    for category, posts in categorized_posts.items():
                        # Запись в файл
                        for_word_file.write(f"\n{category}. Постов в категории: {len(posts)}\n")
                        table = table_creator.create_table(posts, group_id, post_processor)
                        for_word_file.write(table + "\n")  # Записываем таблицу в файл

                        # Вывод в консоль
                        posts_file.write(f"\n{category}. Постов в категории: {len(posts)}\n\n")
                        for post in posts:
                            title = post_processor.extract_title(post['text'])
                            post_date = post_processor.format_date(post['date'])
                            chars_before_pattern = post_processor.count_chars_before_pattern(post['text'])
                            post_link = post_processor.get_post_link(group_id, post['id'])

                            posts_file.write(f"Название: {title}\n"
                                             f"Дата: {post_date}\n"
                                             f"Количество символов: {chars_before_pattern}\n"
                                             f"Ссылка на пост: {post_link}\n"
                                             f"{'-' * 40}\n")

                    # Итоговое количество постов
                    total_posts = f"\nВсего подходящих постов: {len(filtered_posts)}"
                    print(total_posts)
                    posts_file.write(total_posts + "\n")

                print("\nРезультаты успешно записаны в файл for_word_file.txt")
                print("\nРезультаты успешно записаны в файл posts.txt")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
