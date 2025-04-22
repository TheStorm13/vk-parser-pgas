from .post_processor import PostProcessor


class PostCategorizer:
    def __init__(self):
        self.categories = {
            "Пост (менее 400 знаков)": [],
            "Пост (от 400 до 1200 знаков)": [],
            "Пост (от 1200 до 2500 знаков)": [],
            "Пост (свыше 2500 знаков)": [],
        }

    def categorize_posts(self, posts, fio):
        """
        Группирует посты по количеству символов и сортирует их по дате.
        """
        post_processor = PostProcessor(fio)

        for post in posts:
            text_length = post_processor.count_chars_before_pattern(post['text'])
            if text_length < 400:
                self.categories["Пост (менее 400 знаков)"].append(post)
            elif 400 <= text_length < 1200:
                self.categories["Пост (от 400 до 1200 знаков)"].append(post)
            elif 1200 <= text_length < 2500:
                self.categories["Пост (от 1200 до 2500 знаков)"].append(post)
            else:
                self.categories["Пост (свыше 2500 знаков)"].append(post)

        # Сортируем посты в каждой категории по дате
        for category in self.categories:
            self.categories[category].sort(key=lambda x: x['date'])

        return self.categories
