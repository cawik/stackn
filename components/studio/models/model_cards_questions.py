# Questions for model cards. If questions are added here you must also modify ModelCardForm in models/forms.py

section_1 = [
    "Person or organization developing model",
    "Model type", 
    "Information about training algorithms, parameters, fairness constraints or other applied approaches, and features",
    "Paper or other resource for more information",
    "Citation details",
    "License",
    "Where to send questions or comments about the model"
]

section_2 = [
    "Primary intended uses",
    "Primary intended users",
    "Out-of-scope use cases"
]

section_3 = [
    "Relevant factors",
    "Evaluation factors"
]

section_4 = [
    "Model performance measures",
    "Decision thresholds",
    "Variation approaches"
]

section_5 = [
    "Ethical Considerations"
]

section_6 = [
    "Caveats and Recommendations"
]

sections = section_1 + section_2 + section_3 + section_4 + section_5 + section_6
