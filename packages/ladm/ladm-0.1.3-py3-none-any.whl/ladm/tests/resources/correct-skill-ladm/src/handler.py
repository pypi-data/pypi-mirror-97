"""
Skill implementation of spacy named entity extraction.
The spacy model can be configured by the env property SPACY_MODEL.
"""

# Skill calls will begin at the evaluate() method, with the skill payload passed as 'payload'
# and the skill context passed as 'context'.
# For more details, see TODO: url
def evaluate(payload: dict, context: dict) -> dict:
    print(payload)
    print(context)
    message = payload["request"]
    return {"response" : "ECHO (from={}/{}): {}".format(context["owner"], context["name"], message)}

def on_started(context: dict):
    print("on_started triggered!")

def on_stopped(context: dict):
    print("on_stopped triggered!")