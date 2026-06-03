from common.lab_test import KNOWN_UNITS
from extraction.normalizer import normalize_test_name, parse_reference_range
from extraction.schema import ExtractedReport, LabValue
from llm.service import LLMClient


def enrich_lab_value(
        lab_value: LabValue,
) -> LabValue:
    normalized_name, confidence = (
        normalize_test_name(
            lab_value.raw_name
        )
    )

    low_ref, high_ref = (
        parse_reference_range(
            lab_value.reference_range
        )
    )

    if (
            lab_value.unit
            and lab_value.unit not in KNOWN_UNITS
    ):
        confidence -= 0.2

    lab_value.normalized_name = (
        normalized_name
    )

    lab_value.low_ref = low_ref
    lab_value.high_ref = high_ref

    lab_value.confidence = max(
        confidence,
        0.0,
    )

    return lab_value


def enrich_report(
        report: ExtractedReport,
) -> ExtractedReport:
    for item in report.results:
        enrich_lab_value(item)

    return report


def process_uploaded_report(
        report_text: str,
        llm: LLMClient
):
    extracted = llm.extract_lab_values(
        report_text
    )

    return enrich_report(
        extracted
    )
