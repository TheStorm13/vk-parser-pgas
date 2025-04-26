from config import PATH_REPORT
from src.model.post import Post
from src.model.post_category import PostCategory
from src.report.formatter.markdown_report_format import MarkdownReportFormat
from src.report.formatter.text_report_format import TextReportFormat
from src.report.formatter.word_report_format import WordReportFormat
from src.report.report_builder import ReportBuilder
from src.report.report_writer import ReportWriter


class ReportCreator:
    def generate_reports(self, posts: dict[PostCategory, list[Post]], output_path: str = PATH_REPORT):
        # Initialize ReportWriter for managing file output
        writer = ReportWriter(output_path)

        # Iterate through each report format and generate the corresponding report
        for format_name, report_format in {
            "posts.txt": TextReportFormat(),  # Plain text format
            "posts.md": MarkdownReportFormat(),  # Markdown format
            "posts_word.txt": WordReportFormat(),  # Custom word-like format
        }.items():
            builder = ReportBuilder(report_format)  # Configure the report builder with the format
            content = builder.build_report(posts)  # Generate the report content
            writer.write_report(format_name, content)  # Write the generated report to a file
