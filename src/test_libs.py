import numpy as np
import pandas as pd
import spacy
import xgboost as xgb
from flair.data import Sentence
from flair.models import SequenceTagger
from sklearn.tests.test_init import test_import_skl

print("----")
print("Testing Flair:")
print("----")

# make a sentence
sentence = Sentence("I love Berlin .")

# load the NER tagger
tagger = SequenceTagger.load("ner")

# run NER over sentence
tagger.predict(sentence)

print("----")
print("Testing Spacy:")
print("----")

nlp = spacy.load("en_core_web_trf")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

print("----")
print("Testing numpy:")
print("----")

print(np.array([1, 2, 3]))

print("----")
print("Testing pandas:")
print("----")

print(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))

print("----")
print("Testing sklearn:")
print("----")

test_import_skl()

print("----")
print("Testing xgboost:")
print("----")

print(xgb.get_config())
