# Questions for model cards. If questions are added here you must also modify ModelCardForm in models/forms.py

questions_1 = {
    "q11": "Person or organization developing model",
    "q12": "Model date",
    "q13": "Model version",
    "q14": "Model type", 
    "q15": "Information about training algorithms, parameters, fairness constraints or other applied approaches, and features",
    "q16": "Paper or other resource for more information",
    "q17": "Citation details",
    "q18": "License",
    "q19": "Where to send questions or comments about the model"
}

questions_2 = {
    "q21": "Primary intended uses",
    "q22": "Primary intended users",
    "q23": "Out-of-scope use cases"
}

questions_3 = {
    "q31":"Relevant factors",
    "q32": "Evaluation factors"
}

questions_4 = {
    "q41": "Model performance measures",
    "q42": "Decision thresholds",
    "q43": "Variation approaches"
}

questions_5 = {
    "q51": "Ethical Considerations"
}

questions_6 = {
    "q61": "Caveats and Recommendations"
}

categories = {
    "Model Details. Basic information about the model.": questions_1,
    "Intended Use. Use cases that were envisioned during development.": questions_2,
    "Factors. Factors could include demographic or phenotypic groups, environmental conditions, technical attributes.": questions_3,
    "Metrics. Metrics should be chosen to reflect potential real-world impacts of the model.": questions_4,
    "Ethical Considerations": questions_5,
    "Caveats and Recommendations": questions_6
}