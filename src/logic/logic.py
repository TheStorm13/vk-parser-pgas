import time

from config import VK_TOKEN, VK_GROUP
from src.api_handlers.vk_api_handler import VKAPIHandler
from src.post_processing.post_analyzer import PostAnalyzer
from src.report.report_builder import ReportBuilder


class MainLogic:
    def __init__(self):
        pass

    # Основной скрипт
    def run(self, fio, start_date, end_date, update_progress=None, group_name=VK_GROUP):  # Читаем токен из файла

        try:
            # Инициализация классов
            vk_handler = VKAPIHandler(VK_TOKEN)
            post_analyzer = PostAnalyzer(fio)
            report_builder = ReportBuilder()

            # Получаем ID группы
            group_id = vk_handler.get_group_id(group_name)

            # Получаем посты
            start_time = time.time()
            posts = vk_handler.get_posts(group_id, start_date, end_date, update_progress)
            print("Время на Получение постов: ", time.time() - start_time)

            # Анализируем посты
            start_time = time.time()
            filtered_posts = post_analyzer.posts_analyze(posts)
            print("Время на Обработку постов: ", time.time() - start_time)

            for post in filtered_posts:
                print(post.__str__())

            report_builder.report_builder(filtered_posts)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
