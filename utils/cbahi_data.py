# utils/cbahi_data.py
# Complete CBAHI Standards Reference Data
# DentEdTech™ — CBAHI Reviewer Platform

PROGRAMS = {
    "ambulatory": "Ambulatory Care Center (ACC)",
    "phc": "Primary Healthcare Center (PHC)",
    "hospital": "Hospital"
}

CHAPTERS = {
    "ambulatory": [
        {"code": "LD",  "name": "Leadership of the Organization",    "standards": 36, "esrs": 2},
        {"code": "PC",  "name": "Provision of Care",                  "standards": 15, "esrs": 1},
        {"code": "LB",  "name": "Laboratory Services",                "standards": 12, "esrs": 0},
        {"code": "RD",  "name": "Radiology Services",                 "standards": 3,  "esrs": 1},
        {"code": "DN",  "name": "Dental Services",                    "standards": 5,  "esrs": 0},
        {"code": "MM",  "name": "Medication Management",              "standards": 14, "esrs": 0},
        {"code": "MOI", "name": "Management of Information",          "standards": 7,  "esrs": 1},
        {"code": "IPC", "name": "Infection Prevention and Control",   "standards": 14, "esrs": 2},
        {"code": "FMS", "name": "Facility Management and Safety",     "standards": 9,  "esrs": 0},
        {"code": "DPU", "name": "Day Procedure Unit",                 "standards": 12, "esrs": 0},
        {"code": "DA",  "name": "Dermatology & Aesthetics Medicine",  "standards": 6,  "esrs": 0},
    ],
    "phc": [
        {"code": "LD",  "name": "Leadership",                         "standards": 34, "esrs": 0},
        {"code": "QM",  "name": "Quality Management & Patient Safety","standards": 26, "esrs": 1},
        {"code": "MP",  "name": "Manpower",                           "standards": 24, "esrs": 0},
        {"code": "MOI", "name": "Management of Information",          "standards": 14, "esrs": 0},
        {"code": "HR",  "name": "Health Records",                     "standards": 24, "esrs": 1},
        {"code": "PFR", "name": "Patient and Family Rights",          "standards": 25, "esrs": 0},
        {"code": "GC",  "name": "General Clinics",                    "standards": 29, "esrs": 2},
        {"code": "RF",  "name": "Referral",                           "standards": 9,  "esrs": 0},
        {"code": "CP",  "name": "Community Participation",            "standards": 6,  "esrs": 0},
        {"code": "HPE", "name": "Health Promotion and Education",     "standards": 11, "esrs": 0},
        {"code": "MCH", "name": "Maternity and Child Health",         "standards": 8,  "esrs": 0},
        {"code": "IM",  "name": "Immunization",                       "standards": 8,  "esrs": 0},
        {"code": "NCD", "name": "Non-Communicable Diseases",          "standards": 7,  "esrs": 0},
        {"code": "GRC", "name": "Geriatric Care",                     "standards": 7,  "esrs": 0},
        {"code": "CD",  "name": "Communicable Diseases",              "standards": 7,  "esrs": 0},
        {"code": "DOH", "name": "Dental and Oral Health",             "standards": 9,  "esrs": 0},
        {"code": "ES",  "name": "Emergency Services",                 "standards": 14, "esrs": 1},
        {"code": "EH",  "name": "Environmental Health",               "standards": 10, "esrs": 0},
        {"code": "LB",  "name": "Laboratory Services",                "standards": 11, "esrs": 1},
        {"code": "RS",  "name": "Radiological Services",              "standards": 10, "esrs": 1},
        {"code": "PH",  "name": "Pharmaceutical Services",           "standards": 31, "esrs": 1},
        {"code": "FMS", "name": "Facility Management and Safety",     "standards": 12, "esrs": 4},
        {"code": "IPC", "name": "Infection Prevention and Control",   "standards": 28, "esrs": 2},
    ],
    "hospital": [
        {"code": "LD",  "name": "Leadership",                         "standards": 45, "esrs": 3},
        {"code": "HR",  "name": "Human Resources",                    "standards": 22, "esrs": 1},
        {"code": "MOI", "name": "Management of Information",          "standards": 12, "esrs": 0},
        {"code": "MR",  "name": "Medical Records",                    "standards": 18, "esrs": 0},
        {"code": "QM",  "name": "Quality Management & Patient Safety","standards": 30, "esrs": 5},
        {"code": "SC",  "name": "Social Care Services",               "standards": 8,  "esrs": 0},
        {"code": "PFR", "name": "Patient and Family Rights",          "standards": 18, "esrs": 0},
        {"code": "MS",  "name": "Medical Staff",                      "standards": 20, "esrs": 2},
        {"code": "RD",  "name": "Radiology Services",                 "standards": 12, "esrs": 1},
        {"code": "PT",  "name": "Physiotherapy Services",             "standards": 8,  "esrs": 0},
        {"code": "RS",  "name": "Respiratory Care Services",          "standards": 6,  "esrs": 0},
        {"code": "DT",  "name": "Dietary Services",                   "standards": 10, "esrs": 0},
        {"code": "NR",  "name": "Nursing Care",                       "standards": 14, "esrs": 1},
        {"code": "PFE", "name": "Patient and Family Education",       "standards": 10, "esrs": 0},
        {"code": "PC",  "name": "Provision of Care",                  "standards": 50, "esrs": 4},
        {"code": "AN",  "name": "Anesthesia Care",                    "standards": 20, "esrs": 2},
        {"code": "ER",  "name": "Emergency Care",                     "standards": 16, "esrs": 2},
        {"code": "ICU", "name": "Critical Care (ICU/CCU/PICU)",       "standards": 18, "esrs": 3},
        {"code": "OR",  "name": "Operating Room",                     "standards": 15, "esrs": 2},
        {"code": "MM",  "name": "Medication Management",              "standards": 45, "esrs": 5},
        {"code": "IPC", "name": "Infection Prevention and Control",   "standards": 45, "esrs": 5},
        {"code": "LB",  "name": "Laboratory",                         "standards": 80, "esrs": 3},
        {"code": "FMS", "name": "Facility Management and Safety",     "standards": 50, "esrs": 5},
    ],
}

ESR_LIST = {
    "ambulatory": [
        {"code": "LD.13",  "name": "Credentialing & Re-credentialing of Healthcare Providers", "chapter": "LD"},
        {"code": "LD.14",  "name": "Delineated Clinical Privileges for Medical Staff",         "chapter": "LD"},
        {"code": "PC.2",   "name": "Correct Patient Identification (≥2 identifiers)",          "chapter": "PC"},
        {"code": "RD.2",   "name": "Radiation Safety Program",                                  "chapter": "RD"},
        {"code": "IPC.7",  "name": "Sterilization Services — Rigorous Standards",              "chapter": "IPC"},
        {"code": "IPC.11", "name": "Waste Collection, Storage and Safe Disposal",              "chapter": "IPC"},
        {"code": "MOI.7",  "name": "Clinical Documentation Improvement (CDI) Program",         "chapter": "MOI"},
    ],
    "phc": [
        {"code": "GC.13",   "name": "Patient Allergy & Adverse Reaction Documentation",         "chapter": "GC"},
        {"code": "GC.19",   "name": "Care Plan Development for Every Patient",                  "chapter": "GC"},
        {"code": "LB.10",   "name": "Lab Results Reporting (TAT & Panic Values)",              "chapter": "LB"},
        {"code": "RS.5",    "name": "Radiation Safety Protocol",                                "chapter": "RS"},
        {"code": "PH.14",   "name": "Prescription Handling System",                            "chapter": "PH"},
        {"code": "QM.11",   "name": "International Patient Safety Goals Implementation",        "chapter": "QM"},
        {"code": "HR.2",    "name": "Unique Patient Identifier in Health Records",              "chapter": "HR"},
        {"code": "ES.12",   "name": "Crash Cart Monitoring and Checking",                       "chapter": "ES"},
        {"code": "FMS.6",   "name": "Interdisciplinary Safety Rounds (Quarterly)",             "chapter": "FMS"},
        {"code": "FMS.8a",  "name": "Fire Prevention — Staff Training & Evacuation",           "chapter": "FMS"},
        {"code": "FMS.8b",  "name": "Fire Prevention — Equipment & Alarm Systems",             "chapter": "FMS"},
        {"code": "IPC.14",  "name": "Safe Waste Collection, Storage and Disposal",             "chapter": "IPC"},
        {"code": "IPC.22a", "name": "Sterilization Room — Structural Requirements",            "chapter": "IPC"},
        {"code": "IPC.22b", "name": "Sterilization Room — Chemical & Biological Indicators",   "chapter": "IPC"},
    ],
    "hospital": [
        {"code": "PC.2",   "name": "Patient Identification",                                    "chapter": "PC"},
        {"code": "QM.16",  "name": "Patient Safety Program",                                    "chapter": "QM"},
        {"code": "QM.18",  "name": "Surgical Safety Checklist (SSC)",                          "chapter": "QM"},
        {"code": "QM.22",  "name": "Pressure Ulcer Prevention",                                "chapter": "QM"},
        {"code": "QM.23",  "name": "Fall Risk Assessment",                                     "chapter": "QM"},
        {"code": "IPC.14", "name": "Isolation and Transmission-Based Precautions",             "chapter": "IPC"},
        {"code": "IPC.19", "name": "CSSD Sterilization Standards",                             "chapter": "IPC"},
        {"code": "MM.5",   "name": "High-Alert and Hazardous Medications",                     "chapter": "MM"},
        {"code": "MS.6",   "name": "Medical Staff Credentialing and Privileging",              "chapter": "MS"},
        {"code": "FMS.19", "name": "Fire Safety Program",                                      "chapter": "FMS"},
        {"code": "LD.13",  "name": "Credentialing & Privileging Process",                      "chapter": "LD"},
        {"code": "NR.9",   "name": "Adequate Nursing Staffing",                                "chapter": "NR"},
    ],
}

SCORING_THRESHOLDS = {
    "ambulatory": {"accredited": 75, "conditional": 65},
    "phc":        {"accredited": 85, "conditional": 75},
    "hospital":   {"accredited": 85, "conditional": 75},
}

TOTAL_STANDARDS = {
    "ambulatory": 133,
    "phc": 400,
    "hospital": 600,
}
