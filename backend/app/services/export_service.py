from html import escape
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.database.models import GeneratedProject, Repository


def project_zip(project: GeneratedProject) -> BytesIO:
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for filename, contents in project.files.items():
            archive.writestr(filename, contents)
    output.seek(0)
    return output


def repository_pdf(repository: Repository, architecture: str) -> BytesIO:
    output = BytesIO()
    styles = getSampleStyleSheet()
    story = [Paragraph(repository.name, styles["Title"]), Spacer(1, 14)]
    story.append(Paragraph("Architecture Report", styles["Heading2"]))
    for paragraph in architecture.splitlines():
        if paragraph.strip():
            story.append(Paragraph(escape(paragraph), styles["BodyText"]))
            story.append(Spacer(1, 5))
    story.append(Paragraph("Repository Metrics", styles["Heading2"]))
    story.append(Paragraph(str(repository.summary), styles["BodyText"]))
    SimpleDocTemplate(output, pagesize=letter).build(story)
    output.seek(0)
    return output
