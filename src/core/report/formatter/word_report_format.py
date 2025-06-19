from src.core.model.post import Post
from src.core.report.formatter.interface.report_format import ReportFormat
from src.infrastructure.utils.data_utils import DateUtils


class WordReportFormat(ReportFormat):
    def format_header(self, count_posts: int) -> str:
        return f"Всего постов: {count_posts}\n"

    def format_category_header(
        self, category_name: str, count_posts: int, category_point: int
    ) -> str:
        return (
            f"\n{category_name}\n"
            f"Постов в категории: {count_posts}\n"
            f"Количество баллов: {category_point}\n"
        )

    def format_post(self, post: Post) -> dict:
        # Converts a Post object into a dictionary
        return {
            "title": f"Пост «{post.title}»",
            "date": DateUtils.datetime_to_string(post.date),
            "link": post.url,
        }

    def format_category_posts(self, posts: list[Post]) -> str:
        # Extract individual parts of the post information
        post_titles = [
            f"Пост «{post.title}»".replace("« ", "«").replace("»»", "»")
            for post in posts
        ]
        post_dates = [f"{DateUtils.datetime_to_string(post.date)}" for post in posts]
        post_links = [f"{post.url}" for post in posts]

        # Combines the extracted parts into readable sections
        posts_section = "\nПосты:\n" + "\n".join(post_titles)
        dates_section = "Даты:\n" + "\n".join(post_dates)
        links_section = "Ссылки:\n" + "\n".join(post_links) + "\n"

        # Returns the complete formatted section for the category
        return f"{posts_section}\n\n{dates_section}\n\n{links_section}"
