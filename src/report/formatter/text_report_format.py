from src.model.post import Post
from src.report.formatter.interface.report_format import ReportFormat
from src.utils.data_utils import DataUtils


class TextReportFormat(ReportFormat):
    def format_header(self, count_posts: int) -> str:
        return f"Всего постов: {count_posts}\n"

    def format_category_header(self, category_name: str, count_posts: int, category_point: int) -> str:
        return f"\n{category_name}\n" \
               f"Постов в категории: {count_posts}\n" \
               f"Количество баллов: {category_point}\n" \
               f"{'-' * 40}\n"

    def format_post(self, post: Post) -> str:
        post_date = DataUtils.format_date(post.date)

        return f"Название: {post.title}\n" \
               f"Дата: {post_date}\n" \
               f"Количество символов: {post.len_text}\n" \
               f"Ссылка на пост: {post.url}\n" \
               f"{'-' * 40}\n"

    def format_category_posts(self, posts: list[Post]) -> str:
        return "".join(self.format_post(post) for post in posts)
