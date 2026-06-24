from extraction.schema import ExtractedReport


def extracted_report_to_dict(
    report: ExtractedReport,
) -> dict:

    values = {}

    for result in report.results:

        if (
            result.normalized_name
            and result.value is not None
        ):
            values[
                result.normalized_name
            ] = result.value

    return values