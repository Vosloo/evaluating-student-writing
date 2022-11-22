# import spacy visualizer
from spacy import displacy

from src.model import Text, DiscourseType


class Visualizer:
    def visualize_text(self, text: Text) -> None:
        # Use spacy displacy to visualize the text - all text with marked discourses and their types
        ents = []
        for part in text.non_classified_parts:
            ents.append({"start": part[0], "end": part[1], "label": "Non-classified"})

        for discourse in text.discourses:
            ents.append(
                {
                    "start": discourse.ind_start,
                    "end": discourse.ind_end,
                    "label": discourse.type.value,
                }
            )

        doc = {
            "text": text.text,
            "ents": ents,
        }

        colors = {
            DiscourseType.LEAD.value: "#ba5656",
            DiscourseType.POSITION.value: "#c27ba0",
            DiscourseType.CLAIM.value: "#92c57d",
            DiscourseType.EVIDENCE.value: "#8cd8d2",
            DiscourseType.COUNTERCLAIM.value: "#e79139",
            DiscourseType.CONCLUDING_STATEMENT.value: "#ffd966",
            DiscourseType.REBUTTAL.value: "#eb9899",
            "Non-classified": "#969696",
        }
        options = {"colors": colors, "ents": [typ.value for typ in DiscourseType] + ["Non-classified"]}

        displacy.render(doc, style="ent", manual=True, options=options, jupyter=True)
