"""
Ground truth dataset for RAGAS evaluation.
These are question/answer pairs we know the correct answer to
based on the Synthea data.
"""

EVAL_DATASET = [
    {
        "question": "Which patients have diabetes mellitus type 2?",
        "ground_truth": "Dannielle300 Goldner995 and Dwain139 Hoppe518 have diabetes mellitus type 2.",
    },
    {
        "question": "What active medications is Dannielle300 Goldner995 taking?",
        "ground_truth": "Dannielle300 Goldner995 is taking medications related to diabetes management.",
    },
    {
        "question": "Which patients have known allergies?",
        "ground_truth": "Some patients have allergies including drug and environmental allergies recorded in their records.",
    },
    {
        "question": "What conditions does Dwain139 Hoppe518 have?",
        "ground_truth": "Dwain139 Hoppe518 has diabetes mellitus type 2 diagnosed on 2016-06-28.",
    },
    {
        "question": "Which patients are deceased?",
        "ground_truth": "Patients with a recorded death date are deceased.",
    },
    {
        "question": "What lab results are available for patients with diabetes?",
        "ground_truth": "Lab results including blood glucose, HbA1c, and other metabolic panels are available for diabetic patients.",
    },
    {
        "question": "Which patients have hypertension?",
        "ground_truth": "Patients diagnosed with essential hypertension are recorded in the conditions table.",
    },
    {
        "question": "What medications are prescribed for hypertension?",
        "ground_truth": "Medications such as lisinopril and amlodipine are commonly prescribed for hypertension.",
    },
    {
        "question": "Which patients have both diabetes and hypertension?",
        "ground_truth": "Patients with comorbid diabetes and hypertension can be identified by cross-referencing their conditions.",
    },
    {
        "question": "What is the most recent encounter for Dannielle300 Goldner995?",
        "ground_truth": "The most recent encounter date for Dannielle300 Goldner995 is recorded in the encounters table.",
    },
]