from openai import OpenAI

from common.config import settings
from extraction.schema import ExtractedReport
from llm.lab_extraction import build_extraction_prompt, LAB_EXTRACTION_SYSTEM_PROMPT
from llm.prompt import (
    SYSTEM_PROMPT,
    build_prompt,
)


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.model = settings.OPENAI_MODEL
        self.extraction_model=settings.OPENAI_EXTRACTION_MODEL

    def generate(
            self,
            question: str,
            report_text: str,
            lab_context: str,
            context: str,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_prompt(
                question,
                report_text,
                lab_context,
                context,
            ),
        )

        return response.output_text

    def extract_lab_values(
            self,
            report_text: str,
    ) -> ExtractedReport:
        prompt = build_extraction_prompt(
            report_text
        )

        response = self.client.responses.parse(
            model=self.extraction_model,
            instructions=LAB_EXTRACTION_SYSTEM_PROMPT,
            input=prompt,
            text_format=ExtractedReport,
        )

        return response.output_parsed

