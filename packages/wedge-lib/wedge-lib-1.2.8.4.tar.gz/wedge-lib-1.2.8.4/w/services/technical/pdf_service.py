from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from w.services.technical.filesystem_service import FilesystemService


class PdfService:
    @classmethod
    def write_file(cls, filename, content) -> bytes:
        """
        Create a PDF file

        Args:
            filename: string output file path
            content (str|dict): message or template (as dict) :
                {"template_name": <str>, "context": <dict> }

        Returns:
            bytes: pdf binary
        """

        if not content:
            return None

        font_config = FontConfiguration()

        # html content
        if isinstance(content, dict):
            content = render_to_string(**content)
        html = HTML(string=content)

        # create pdf content
        pdf = html.write_pdf(None, font_config=font_config)

        # create file
        FilesystemService.write_binary_file(filename, pdf)

        return pdf
