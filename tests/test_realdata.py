import unittest
import json
from fever.eval.scorer import *

class TestRealData(unittest.TestCase):

    def setUp(self):
        self.predictions = []
        self.actual = []
        with open('predictions.jsonl') as f:
            for line in f:
                self.predictions.append(json.loads(line))

        with open('actual.jsonl') as f:
            for line in f:
                self.actual.append(json.loads(line))


    def test_scores(self):
        score,_ = fever_score(self.predictions,self.actual)
        self.assertAlmostEqual(score,0.32573257325732574)



    def test_acc(self):
        _,acc = fever_score(self.predictions,self.actual)
        self.assertAlmostEqual(acc,0.5208520852085209)