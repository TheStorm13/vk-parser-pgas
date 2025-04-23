import time

from config import VK_TOKEN, VK_GROUP
from src.logic.api_handlers.vk_api_handler import VKAPIHandler
from src.logic.post_processing.post_analyzer import PostAnalyzer
from src.report.report_creator import ReportCreator


class MainLogic:
    def __init__(self):
        pass

    # Основной скрипт
    def run(self, fio, start_date, end_date, update_progress=None, group_name=VK_GROUP):  # Читаем токен из файла

        try:
            # Инициализация классов
            vk_handler = VKAPIHandler(VK_TOKEN)
            post_analyzer = PostAnalyzer(fio)
            report_creator = ReportCreator()

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

            report_creator.generate_reports(filtered_posts, "result")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
