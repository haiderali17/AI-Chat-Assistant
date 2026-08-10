"""
PDF generation utility for the AI Chat Assistant.

This module is responsible only for converting
conversation data into a PDF document.
"""

from io import BytesIO

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer
)


class PDFGenerator:
    """Generate PDF documents from chat conversations."""

    def generate_conversation_pdf(self, messages):
        """
        Generate a PDF containing the conversation.

        Args:
            messages (list): Conversation history.

        Returns:
            bytes: Generated PDF content.
        """

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ConversationTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=28,
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "ConversationSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=10,
            leading=14,
            spaceAfter=20
        )

        user_style = ParagraphStyle(
            "UserMessage",
            parent=styles["Normal"],
            fontSize=11,
            leading=17,
            spaceAfter=12
        )

        assistant_style = ParagraphStyle(
            "AssistantMessage",
            parent=styles["Normal"],
            fontSize=11,
            leading=17,
            spaceAfter=12
        )

        elements = []

        elements.append(
            Paragraph(
                "AI Chat Assistant",
                title_style
            )
        )

        elements.append(
            Paragraph(
                "Conversation Export",
                subtitle_style
            )
        )

        # =================================================
        # ADD CONVERSATION
        # =================================================

        for message in messages:

            role = message["role"]
            content = message["content"]

            # Escape characters that have special meaning
            # inside ReportLab's Paragraph markup.

            content = (
                str(content)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>")
            )

            if role == "user":

                elements.append(
                    Paragraph(
                        f"<b>USER</b><br/>{content}",
                        user_style
                    )
                )

            elif role == "assistant":

                elements.append(
                    Paragraph(
                        f"<b>ASSISTANT</b><br/>{content}",
                        assistant_style
                    )
                )

            elements.append(
                Spacer(1, 6)
            )

        # =================================================
        # BUILD PDF
        # =================================================

        document.build(elements)

        buffer.seek(0)

        return buffer.getvalue()