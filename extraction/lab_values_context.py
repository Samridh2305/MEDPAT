def build_lab_context(
        lab_values,
) -> str:

    if not lab_values:
        return "No extracted lab values available."

    lines = []

    for lab in lab_values:

        lines.append(
            (
                f"Test: {lab.normalized_name}, "
                f"Value: {lab.value}, "
                f"Unit: {lab.unit}, "
                f"Reference Range: {lab.reference_range}"
            )
        )

    return "\n".join(lines)