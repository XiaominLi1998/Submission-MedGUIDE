
# Prompt to convert guideline image (decision tree) to JSON object:
template_guideline_to_json = '''You are given a clinical decision tree diagram (as a screenshot image) that outlines medical guidelines for diagnosis or treatment. Your task is to convert the decision tree into a structured JSON format that precisely mirrors the full logic and hierarchy presented in the figure.

* The JSON must accurately reflect all branching paths, decision points, conditions, and outcomes.
* All treatment options, diagnostic steps, and relevant notes (e.g. footnotes or eligibility criteria) must be preserved.
* Maintain the exact hierarchical relationships and nesting, so that the JSON could be used to programmatically reconstruct the original tree.
* Use clear and descriptive key names based on the text in the image.
* If treatments or conditions include multiple options or logical conditions (e.g. “A or B”), represent them using lists or nested structures as appropriate.

Example format:

{
    "First relapse (morphologic or molecular)": {
        "Early relapse (<6 mo) after ATRA and arsenic trioxide (no anthracycline)": {
            "Therapy": [
                "Anthracycline-based regimen as per APL-3",
                "Gemtuzumab ozogamicin"
            ]
        },
        "No prior exposure to arsenic trioxide OR early relapse (<6 mo) after ATRA + anthracycline-containing regimen": {
            "Therapy": [
                "Arsenic trioxide \u00b1 ATRA \u00b1 gemtuzumab ozogamicin"
            ]
        },
        "Late relapse (\u22656 mo) after arsenic trioxide-containing regimen": {
            "Therapy": [
                "Arsenic trioxide \u00b1 ATRA \u00b1 (anthracycline or gemtuzumab ozogamicin)"
            ]
        }
    },
    "Second remission (morphologic)": {
        "Consider CNS prophylaxis": "IT chemotherapy (methotrexate or cytarabine)",
        "PCR result (by BM)": {
            "PCR negative": {
                "Transplant candidate": "Autologous HCT",
                "Not transplant candidate": "Arsenic trioxide consolidation (total of 6 cycles)"
            },
            "PCR positive": {
                "Transplant candidate": "Matched sibling or alternative donor HCT",
                "Not transplant candidate": "Clinical trial"
            }
        }
    },
    "No remission": {
        "Next steps": [
            "Clinical trial",
            "Matched sibling or alternative donor HCT"
        ]
    }
}


Now, based on the uploaded decision tree image, generate the corresponding JSON structure.'''



# Prompt to convert guideline image (decision tree) to JSON object:
template_guideline_to_paths = '''
You are provided with an image of an NCCN clinical decision tree guideline, outlining detailed medical instructions for diagnosis and treatment. Your task is to precisely list all possible clinical decision paths depicted in the guideline.

Instructions:
* Represent each decision path as a Python list of strings.
* Each string must exactly match the text appearing in the decision nodes, conditions, or treatment steps from the image, without abbreviation, modification, or paraphrasing.
* Include every potential pathway from the initial decision node down to each final leaf node.

Now, generate all possible paths.'''




# Prompt to construct a question (with fabricated patient profile) based on a  given decision path:
# The path is a list of strings
def template_path_to_question(path):
    path_str = "[\n  " + ",\n  ".join(f'"{node}"' for node in path) + "\n]"
    return f'''You are provided with a clinical decision path derived from an NCCN guideline, presented as an ordered list of decision nodes (each node is a string). Your task is to generate a realistic patient vignette—a brief clinical case—including pertinent medical history, timing of relapse, previous treatments, test results, and clinical assessments required to match precisely each node in the provided decision path from root to leaf. Conclude your vignette with a clinical question asking explicitly about the appropriate next treatment step. The correct answer must correspond exactly to the final node of the provided path but should not be mentioned explicitly in either the vignette or the question.

Decision Path:
{path_str}

Formatting Instructions:
* Present the entire vignette and concluding question as a single paragraph.
* Do not reveal or imply the correct (leaf node) answer within the vignette or the question.'''

