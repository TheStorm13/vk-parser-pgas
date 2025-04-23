from src.model.post import Post
from src.report.formatter.interface.report_format import ReportFormat
from src.utils.data_utils import DataUtils


class MarkdownReportFormat(ReportFormat):
    def format_header(self, count_posts: int) -> str:
        return f"# Всего постов: {count_posts}\n"

    def format_category_header(self, category_name: str, count_posts: int, category_point: int) -> str:
        return f"## {category_name}\n" \
               f"### Постов в категории: {count_posts}\n" \
               f"### Количество баллов: {category_point}\n" \
               "\n| Название | Длина | Дата | Ссылка |\n|------|------|------|------|\n"

    def format_post(self, post: Post) -> str:
        title = post.title.replace("|", r"\|")  # Экранируем Markdown символ
        post_date = DataUtils.format_date(post.date)
        return f"| {title} | {post.len_text} | {post_date} | [{post.url}]({post.url}) |\n"

    def format_category_posts(self, posts: list[Post]) -> str:
        return "".join(self.format_post(post) for post in posts)
