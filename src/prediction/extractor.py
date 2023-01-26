import regex as re
import spacy
from spacy.tokens import Doc, Span
from copy import deepcopy

class Extractor:
    def __init__(self, model_path: str) -> None:
        self.nlp = spacy.load(model_path)

    def extract_discourses(self, text: str, keep_first_ds: bool = True, keep_first_de: bool = False) -> tuple[Doc, list[str]]:
        doc = self.nlp(text)
        doc = self.fix_consecutive_tags(doc, True, False)
        spacy.displacy.render(doc, style="ent", jupyter=True)
        return doc, self._extract_discourses(doc)

    def fix_consecutive_tags(self, doc: Doc, keep_first_ds=True, keep_first_de=False):
        new_doc = deepcopy(doc)
        ents = doc.ents
        prev = None
        new_ents = []
        for ent in ents:
            if ent.label_ == "DS":
                if keep_first_ds:
                    if prev != "DS":
                        new_ents.append(Span(new_doc, ent.start, ent.end, "DS"))
                        prev = ent.label_
                    else:
                        continue
                else:
                    if prev == "DS":
                        new_ents[len(new_ents)-1] = Span(new_doc, ent.start, ent.end, "DS")
                        prev = ent.label_
                    else:
                        new_ents.append(Span(new_doc, ent.start, ent.end, "DS"))
                        prev = ent.label_
            else:
                if keep_first_de:
                    if prev != "DE":
                        new_ents.append(Span(new_doc, ent.start, ent.end, "DE"))
                        prev = ent.label_
                    else:
                        continue
                else:
                    if prev == "DE":
                        new_ents[len(new_ents)-1] = Span(new_doc, ent.start, ent.end, "DE")
                        prev = ent.label_
                    else:
                        new_ents.append(Span(new_doc, ent.start, ent.end, "DE"))
                        prev = ent.label_
        if new_ents[0].label_ == "DE":
            new_ents = new_ents[1:]
        if new_ents[-1].label_ == "DS":
            new_ents = new_ents[:-1]
        
        new_doc.set_ents(new_ents)

        return new_doc

    def _extract_discourses(self, doc: Doc, keep_first_ds: bool = True, keep_first_de: bool = False) -> list[str]:
        discourses = []
        tokens = [token.text for token in doc]

        last_ent = None
        ents = []
        deleted_offset = 0
        for ind, ent in enumerate(doc.ents):
            if ent.label_ == "DS" and last_ent == "DS":
                if not keep_first_ds:
                    ents[ind - deleted_offset - 1] = ent

                deleted_offset += 1
                continue

            if ent.label_ == "DE" and last_ent == "DE":
                if not keep_first_de:
                    ents[ind - deleted_offset - 1] = ent

                deleted_offset += 1
                continue

            ents.append(ent)
            last_ent = ent.label_

        last_tag = None
        for ind, ent in enumerate(ents):
            if ent.label_ == "DS":
                start_pos = ent.start
                last_tag = "DS"
                continue

            if ent.label_ == "DE":
                assert last_tag == "DS", "DE without DS"
                disc = " ".join(tokens[start_pos : ent.end])
                disc = re.sub(r" \.", ".", disc)
                discourses.append(disc)
                start_pos = None
                last_tag = "DE"
                continue

        return discourses
