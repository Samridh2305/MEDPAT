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

    # Lipids (core only)
    "LBDHDD",
    "LBXTC",
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

    # Lipids (core only)
    "LBDHDD": "hdl",
    "LBXTC": "cholesterol",
}

CLINICAL_RENAME_MAP = {
    "URDACT": "urine_albumin_creatinine_ratio",
    "URXOAV": "urine_osmolality",
    "LBXTR": "triglycerides",
    "LBDLDL": "ldl",
    "LBXAPB": "apob",
    "LBXVIDMS": "vitamin_d",
}

FEATURES = [
    # Lab features
    "hemoglobin",
    "rbc",
    "wbc",
    "glucose",
    "creatinine",
    "bun",
    "albumin",
    "hba1c",
    "hdl",
    "cholesterol",

    # Clinical features (from clinical module)
    "avg_sys_bp",
    "avg_dia_bp",
    "pulse_rate",
    "hypertension_stage1",
    "hypertension_stage2",

    "apob",
    "triglycerides",
    "ldl",
    "tg_ldl_ratio",

    "urine_albumin_creatinine_ratio",
    "urine_osmolality",

    "vitamin_d",
    "vitamin_d_deficient",

    "activity_score",

    # Demographics
    "age",
    "gender",
    "race",

]