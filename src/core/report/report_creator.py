from src.core.manager.state_manager import StateManager
from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.core.report.formatter.markdown_report_format import MarkdownReportFormat
from src.core.report.formatter.text_report_format import TextReportFormat
from src.core.report.formatter.word_report_format import WordReportFormat
from src.core.report.report_builder import ReportBuilder
from src.core.report.report_writer import ReportWriter


class ReportCreator:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

    def generate_reports(self, posts: dict[PostCategory, list[Post]]):
        # Initialize ReportWriter for managing file output

        writer = ReportWriter()

        # Iterate through each report format and generate the corresponding report
        for format_name, report_format in {
            "posts.txt": TextReportFormat(),  # Plain text format
            "posts.md": MarkdownReportFormat(),  # Markdown format
            "posts_word.txt": WordReportFormat(),  # Custom word-like format
        }.items():
            builder = ReportBuilder(
                report_format
            )  # Configure the report builder with the format
            content = builder.build_report(posts)  # Generate the report content
            writer.write_report(
                format_name, content
            )  # Write the generated report to a file
