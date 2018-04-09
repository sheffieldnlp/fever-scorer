import unittest
import json
from fever.scorer import *

class TestRealData(unittest.TestCase):

    def setUp(self):
        self.predictions = []
        self.actual = []
        with open('dev.jsonl') as f:
            for ix,line in enumerate(f):
                line = json.loads(line)
                self.predictions.append({"predicted_label":line["label"],
                                         "predicted_evidence":[[e[2],e[3]]
                                                               for e in line["all_evidence"] if e[2] is not None]})

        with open('dev.jsonl') as f:
            for line in f:

                line = json.loads(line)
                self.actual.append({"label":line["label"],
                                    "evidence":line["evidence"]})


    def test_scores(self):
        score,_ = fever_score(self.predictions,self.actual)
        self.assertEqual(score,1.0)

    def test_acc(self):
        _,acc = fever_score(self.predictions,self.actual)
        self.assertEqual(acc,1.0)
