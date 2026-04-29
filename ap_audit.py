import argparse
import sys
import re

# Database of topics and their "Must-Say" phrases
TOPICS = {
    "IMF": {
        "phrases": [
            r"polarizable",
            r"electron cloud",
            r"(london dispersion|ldfs?)"
        ],
        "upgrade": '"Molecule X has a LARGER, MORE POLARIZABLE ELECTRON CLOUD, leading to \nstronger LDFs and a higher boiling point."',
        "red_ink": [
            'Missing reference to electron cloud polarizability.',
            'Missing reference to London Dispersion Forces.'
        ]
    },
    "THERMO": {
        "phrases": [
            r"entropy",
            r"dispersed",
            r"microstates",
            r"favorab(le|ility)"
        ],
        "upgrade": '"The products are MORE DISPERSED and occupy a greater number of MICROSTATES, leading to an increase in ENTROPY."',
        "red_ink": [
            'Missing reference to particles being more dispersed or occupying more microstates.',
            'Missing reference to entropy.'
        ]
    },
    "ACID_BASE": {
        "phrases": [
            r"half-equivalence",
            r"pka",
            r"\[ha\]\s*=\s*\[a-\]"
        ],
        "upgrade": '"At the HALF-EQUIVALENCE point, [HA] = [A-], therefore pH = pKa."',
        "red_ink": [
            'Missing reference to the half-equivalence point or [HA] = [A-].'
        ]
    },
    "KINETICS": {
        "phrases": [
            r"linear",
            r"order",
            r"time"
        ],
        "upgrade": '"The plot of ln[A] versus time is the most LINEAR, indicating the reaction is FIRST ORDER."',
        "red_ink": [
            'Missing reference to the linearity of the graph to determine the order.'
        ]
    },
    "CALORIMETRY": {
        "phrases": [
            r"q\s*=\s*mc(delta|Δ)t",
            r"surroundings",
            r"limiting reactant"
        ],
        "upgrade": '"Calculate q_surr = mcΔT, then set q_rxn = -q_surr, and divide by moles of limiting reactant."',
        "red_ink": [
            'Missing reference to heat gained/lost by surroundings or limiting reactant.'
        ]
    }
}

# Mapping specific questions to topics
QUESTION_MAPPING = {
    ("2025", "5"): "IMF",
    ("2025", "2"): "ACID_BASE",
    ("2025", "3"): "THERMO",
    ("2024", "1"): "CALORIMETRY", # Calorimetry
    ("2024", "2"): "ACID_BASE",
    ("2024", "6"): "KINETICS",
}

def determine_topic(year, q, ans):
    # Try to map by year and question
    if (year, q) in QUESTION_MAPPING:
        return QUESTION_MAPPING[(year, q)]

    # Fallback to keyword matching in the answer
    ans_lower = ans.lower()
    if "boiling point" in ans_lower or "vapor pressure" in ans_lower or "bigger" in ans_lower:
        return "IMF"
    if "ph" in ans_lower or "acid" in ans_lower or "base" in ans_lower or "titration" in ans_lower:
        return "ACID_BASE"
    if "entropy" in ans_lower or "delta g" in ans_lower or "favorable" in ans_lower:
        return "THERMO"
    if "q=" in ans_lower or "calorimetry" in ans_lower or "heat" in ans_lower:
        return "CALORIMETRY"

    return "IMF" # Default

def grade_response(year, q, ans):
    topic_key = determine_topic(year, q, ans)
    topic_data = TOPICS.get(topic_key)

    ans_lower = ans.lower()

    points = 1
    red_inks = []

    # Custom check for "bigger" in IMF
    if topic_key == "IMF" and "bigger" in ans_lower:
        red_inks.append('"Bigger" is a size description, not a chemical mechanism.')
        points = 0

    # Check for missing phrases
    matched_count = 0
    for i, phrase in enumerate(topic_data["phrases"]):
        if re.search(phrase, ans_lower):
            matched_count += 1

    if matched_count < len(topic_data["phrases"]) // 2 + 1: # Require some of the phrases
        if points == 1:
            points = 0

        if topic_key == "IMF" and not re.search(r"polarizable", ans_lower):
            if 'Missing reference to electron cloud polarizability.' not in red_inks:
                red_inks.append('Missing reference to electron cloud polarizability.')
        elif len(red_inks) == 0: # Add generic if no specific
            red_inks.append(topic_data["red_ink"][0])

    if points == 1:
        status = "[ 1 / 1 ] Points"
        red_inks_text = "- Perfect response."
        upgrade_text = '"' + ans + '"'
    else:
        status = "[ 0 / 1 ] Points"
        red_inks_text = "\n".join([f"- {ink}" for ink in red_inks])
        upgrade_text = topic_data["upgrade"]

    report = f""">>> AP-AUDIT REPORT ({year} Q{q})
---------------------------------------
STATUS: {status}
USER: "{ans}"

RED INK:
{red_inks_text}

UPGRADE:
{upgrade_text}
---------------------------------------"""
    return report

def main():
    parser = argparse.ArgumentParser(description="AP Chemistry FRQ Auditor")
    parser.add_argument("--year", type=str, required=True, help="Year of the FRQ")
    # Accept either --q or --question
    parser.add_argument("--q", "--question", type=str, dest="question", required=True, help="Question number")
    # Accept either --ans or --user-answer
    parser.add_argument("--ans", "--user-answer", type=str, dest="user_answer", required=True, help="User's answer to grade")

    args = parser.parse_args()

    report = grade_response(args.year, args.question, args.user_answer)
    print(report)

if __name__ == "__main__":
    main()
