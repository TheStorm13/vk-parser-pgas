from src.core.manager.state_manager import StateManager
from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.core.report.formatter.markdown_report_format import MarkdownReportFormat
from src.core.report.formatter.text_report_format import TextReportFormat
from src.core.report.formatter.word_report_format import WordReportFormat
from src.core.report.report_builder import ReportBuilder
from src.core.report.report_writer import ReportWriter


class ReportCreator:
    """Создает отчеты в нескольких форматах."""

    def __init__(self, state_manager: StateManager):
        """Инициализирует создателя отчетов.

        Args:
            state_manager: Менеджер состояния приложения.

        """
        self.state_manager = state_manager

    def generate_reports(self, posts: dict[PostCategory, list[Post]]):
        """Генерирует отчеты и записывает файлы.

        Args:
            posts: Посты, сгруппированные по категориям.

        Returns:
            None

        """
        writer = ReportWriter()

        for format_name, report_format in {
            "posts.txt": TextReportFormat(),
            "posts.md": MarkdownReportFormat(),
            "posts_word.txt": WordReportFormat(),
        }.items():
            builder = ReportBuilder(report_format)
            content = builder.build_report(posts)
            writer.write_report(format_name, content)
