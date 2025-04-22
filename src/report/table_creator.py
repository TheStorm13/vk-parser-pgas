class TableCreator:
    @staticmethod
    def create_table(posts, group_id, post_processor):
        """
        Создаёт таблицу из списка постов, используя знак новой строки для разделения строк.
        """
        # Заголовки таблицы
        table = "Название\nДата\nСсылка\n"  # Используем табуляцию для разделения столбцов
        title = ""
        post_date = ""
        post_link = ""
        # Добавляем строки с данными
        for post in posts:
            title += "\n" + "Пост «" + post_processor.extract_title(post['text']) + "»"
            post_date += "\n" + post_processor.format_date(post['date'])
            post_link += "\n" + post_processor.get_post_link(group_id, post['id'])

        # Форматируем строку
        table += title + post_date + post_link  # Добавляем новую строку

        return table
