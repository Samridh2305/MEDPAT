LAB_COLUMNS = [
    "SEQN",

    # CBC
    "LBXHGB",
    "LBXRBCSI",
    "LBXWBCSI",

    # Biochemistry
    "LBXSGL",
    "LBXSCR",
    "LBXSBU",
    "LBXSAL",

    # Diabetes
    "LBXGH",

    # Lipids
    "LBDHDD",
    "LBXTC",

    # ApoB
    "LBXAPB",

    # Triglycerides / LDL
    "LBXTR",
    "LBDLDL",

    # Kidney markers
    "URDACT",
    "URXOAV",

    # Vitamin D
    "LBXVIDMS",
]

LAB_RENAME_MAP = {
    # CBC
    "LBXHGB": "hemoglobin",
    "LBXRBCSI": "rbc",
    "LBXWBCSI": "wbc",

    # Biochemistry
    "LBXSGL": "glucose",
    "LBXSCR": "creatinine",
    "LBXSBU": "bun",
    "LBXSAL": "albumin",

    # Diabetes
    "LBXGH": "hba1c",

    # Lipids
    "LBDHDD": "hdl",
    "LBXTC": "cholesterol",

    # Additional lipids
    "LBXAPB": "apob",
    "LBXTR": "triglycerides",
    "LBDLDL": "ldl",

    # Kidney
    "URDACT": "urine_albumin_creatinine_ratio",
    "URXOAV": "urine_osmolality",

    # Vitamin D
    "LBXVIDMS": "vitamin_d",
}

FEATURES = [
    # CBC
    "hemoglobin",
    "rbc",
    "wbc",

    # Biochemistry
    "glucose",
    "creatinine",
    "bun",
    "albumin",

    # Diabetes
    "hba1c",

    # Lipids
    "hdl",
    "cholesterol",
    "apob",
    "triglycerides",
    "ldl",

    # Kidney
    "urine_albumin_creatinine_ratio",
    "urine_osmolality",

    # Vitamin D
    "vitamin_d",

    # Demographics
    "age",
    "gender",
    "race",
]