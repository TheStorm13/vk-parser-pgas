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
        writer = ReportWriter(output_path)

        for format_name, report_format in {
            "posts.txt": TextReportFormat(),
            "posts.md": MarkdownReportFormat(),
            "posts_word.txt": WordReportFormat(),
        }.items():
            builder = ReportBuilder(report_format)
            content = builder.build_report(posts)
            writer.write_report(format_name, content)
