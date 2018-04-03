# FEVER Scorer

[![Build Status](https://travis-ci.org/sheffieldnlp/fever-scorer.svg?branch=master)](https://travis-ci.org/sheffieldnlp/fever-scorer)

Scoring function for the Fact Extraction and VERification shared task

This scorer produces two outputs: the strict score considering the requirement for evidence and the label accuracy.

The evidence is considered to be correct if there exists a complete list of actual evidence that is a subset of the predicted evidence.

## Example 1
```python
from fever.eval.scorer import fever_score

instance1 = {"label": "refutes", "predicted_label": "refutes", "predicted_evidence": [ #is not strictly correct - missing (page2,2)
        ["page1", 1]                                    #page name, line number
    ], 
    "evidence":
    [
        [
            [None, None, "page1", 1],           #[annotation id, evidence id, page name, line number]
            [None, None, "page2", 2],
        ]
    ]
}

instance2 = {"label": "refutes", "predicted_label": "refutes", "predicted_evidence": [
        ["page1", 1],                                   
        ["page2", 2],
        ["page3", 3]                                    
    ], 
    "evidence":
    [
        [
            [None, None, "page1", 1],   
            [None, None, "page2", 2],
        ]
    ]
}

predictions = [instance1, instance2]
strict_score, label_accuracy = fever_score(predictions)

print(strict_score)     #0.5
print(label_accuracy)   #1.0
```



## Example 2 - (e.g. blind test set)
```python
from fever.eval.scorer import fever_score

instance1 = {"predicted_label": "refutes", "predicted_evidence": [ #is not strictly correct - missing (page2,2)
    ["page1", 1]                                    #page name, line number
]}

instance2 = {"predicted_label": "refutes", "predicted_evidence": [
    ["page1", 1],                                   #page name, line number
    ["page2", 2],
    ["page3", 3]
]}

actual = [
    {"label": "refutes", "evidence":
        [
            [
                [None, None, "page1", 1],           #[annotation id, evidence id, page name, line number]
                [None, None, "page2", 2],
            ]
        ]},
    {"label": "refutes", "evidence":
        [
            [
                [None, None, "page1", 1],
                [None, None, "page2", 2],
            ]
        ]}
]

predictions = [instance1, instance2]
strict_score, label_accuracy = fever_score(predictions, actual)

print(strict_score)     #0.5
print(label_accuracy)   #1.0
```
