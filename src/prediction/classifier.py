import torch
import spacy
from transformers import RobertaTokenizer
from extractor import Extractor
from spacy.tokens import Doc


class Classifier:
    def __init__(self, model_path: str, segmentation_model_path: str) -> None:
        self.model = torch.load(model_path)
        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.extractor = Extractor(segmentation_model_path)

    def predict(self, text: str) -> Doc:
        doc, discourses = self.extractor.extract_discourses(text, True, False)
        #spacy.displacy.render(doc, style="ent", jupyter=True)
        words = [token.text for token in doc]
        labels = self._predict(discourses)

        ents = []
        in_disc = False
        current_class = -1
        last_type = None
        
        for token in doc:
            if last_type == "DE" and token.ent_type_ != "DE":
                in_disc = False
                
            if token.ent_type_ == "DS":
                if token.ent_iob_ == "I":
                    ents.append(f"I-{labels[current_class]}")
                else:
                    current_class+=1
                    ents.append(f"B-{labels[current_class]}")
                    in_disc = True
            elif in_disc or token.ent_type_ == "DE":
                
                ents.append(f"I-{labels[current_class]}")
            else:
                
                ents.append("O")
            last_type = token.ent_type_

        return Doc(self.extractor.nlp.vocab, words, ents=ents)

    def _predict(self, test_data: list[str]) -> list[str]:

        labels = {'Lead': 0,
                  'Position': 1,
                  'Evidence': 2,
                  'Claim': 3,
                  'Concluding Statement': 4,
                  'Counterclaim': 5,
                  'Rebuttal': 6
                  }

        predicted_labels = []

        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")

        if use_cuda:

            self.model = self.model.cuda()

        with torch.no_grad():

            for test_input in test_data:

                token = self.tokenizer(
                    test_input, padding='max_length', max_length=512, truncation=True, return_tensors="pt")

                mask = token['attention_mask'].to(device)
                input_id = token['input_ids'].squeeze(1).to(device)

                output = self.model(input_id, mask)
                result = int(output.argmax(dim=1))

                for key, value in labels.items():
                    if result == value:
                        predicted_labels.append(key)

        return predicted_labels
