from src.post_processing import PostCategorizer
from src.utils.data_utils import DataUtils


class ReportBuilder:
    @staticmethod
    def create_txt_report(result_posts):
        output = f"Всего постов: {sum(len(posts) for posts in result_posts.values())}"

        for category, posts in result_posts.items():

            output += (f"\n\n\n{category}. Постов в категории: {len(posts)}\n")
            # Выводим результаты в консоль и записываем в файл
            for post in posts:
                title = post.title.replace("|", r"\|")  # Экранируем символы Markdown
                len_text = post.len_text
                post_date = DataUtils.format_date(post.date)
                post_link = post.url

                output += (f"Название: {title}\n"
                           f"Дата: {post_date}\n"
                           f"Количество символов: {len_text}\n"
                           f"Ссылка на пост: {post_link}\n"
                           f"{'-' * 40}\n")
        return output

    @staticmethod
    def create_md_report(result_posts):
        """
        Создаёт таблицу в формате Markdown из списка постов.
        """
        output = f"## Всего постов: {sum(len(posts) for posts in result_posts.values())}\n"

        for category, posts in result_posts.items():
            output += f"### {category}. Постов в категории: {len(posts)}\n"
            output += f"### Количество баллов в этой категории: {PostCategorizer.calculate_points(category, len(posts))}\n"

            # Создаем заголовки таблицы
            output += "\n| Название | Длина | Дата | Ссылка |\n"
            output += "|------|------|------|------|\n"

            # Добавляем строки с данными
            for post in posts:
                title = post.title.replace("|", r"\|")  # Экранируем символы Markdown
                len_text = post.len_text
                post_date = DataUtils.format_date(post.date)
                post_link = post.url
                output += f"| {title} | {len_text} | {post_date} | [{post_link}]({post_link}) |\n"

        return output

    @staticmethod
    def create_word_report(result_posts):
        """
        Создаёт таблицу из списка постов, используя знак новой строки для разделения строк.
        """
        output = f"Всего постов: {sum(len(posts) for posts in result_posts.values())}\n"

        for category, posts in result_posts.items():
            output += (f"\n\n\n{category}. Постов в категории: {len(posts)}\n")
            output += "Название\nДата\nСсылка\n"  # Используем табуляцию для разделения столбцов
            title_list = ""
            post_date_list = ""
            post_link_list = ""
            # Добавляем строки с данными
            for post in posts:
                title = post.title
                post_date = DataUtils.format_date(post.date)
                post_link = post.url

                title_list += f"\nПост «{title}»"
                post_date_list += f"\n{post_date}"
                post_link_list += f"\n{post_link}"

            # Форматируем строку
            output += title_list + post_date_list + post_link_list  # Добавляем новую строку

        return output

    def report_builder(self, posts):
        # Открываем файлы для записи
        posts_txt = open("result/posts.txt", "w", encoding="utf-8")
        posts_md = open("result/posts.md", "w", encoding="utf-8")
        posts_word = open("result/posts_word.txt", "w", encoding="utf-8")

        # Итоговое количество постов
        posts_txt.write(ReportBuilder.create_txt_report(posts))
        posts_md.write(ReportBuilder.create_md_report(posts))
        posts_word.write(ReportBuilder.create_word_report(posts))

        posts_txt.close()
        posts_md.close()
        posts_word.close()

        print("\nРезультаты успешно записаны в файл posts.txt")
        print("\nРезультаты успешно записаны в файл posts.md")
        print("\nРезультаты успешно записаны в файл posts_word.txt")
