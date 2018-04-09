def check_predicted_evidence_format(instance):
    if 'predicted_evidence' in instance.keys() and len(instance['predicted_evidence']):
        assert all(isinstance(prediction, list) or isinstance(prediction, tuple)
                   for prediction in instance["predicted_evidence"]), \
            "Predicted evidence must be a list of (page,line) tuples"

        assert all(len(prediction) == 2
                   for prediction in instance["predicted_evidence"]), \
            "Predicted evidence must be a list of (page,line) tuples"

        assert all(isinstance(prediction[0], str)
                   for prediction in instance["predicted_evidence"]), \
            "Predicted evidence must be a list of (page<string>,line<int>) tuples"

        assert all(isinstance(prediction[1], int)
                   for prediction in instance["predicted_evidence"]), \
            "Predicted evidence must be a list of (page<string>,line<int>) tuples"


def is_correct_label(instance):
    return instance["label"].upper() == instance["predicted_label"].upper()

def is_strictly_correct(instance):
    #Strict evidence matching is only for NEI class

    check_predicted_evidence_format(instance)

    if instance["label"].upper() != "NOT ENOUGH INFO" and is_correct_label(instance):

        assert 'predicted_evidence' in instance, "Predicted evidence must be provided for strict scoring"

        for evience_group in instance["evidence"]:
            #Filter out the annotation ids. We just want the evidence page and line number
            actual_sentences = [[e[2], e[3]] for e in evience_group]
            #Only return true if an entire group of actual sentences is in the predicted sentences
            if all([actual_sent in instance["predicted_evidence"] for actual_sent in actual_sentences]):
                return True

    #If the class is NEI, we don't score the evidence retrieval component
    elif instance["label"].upper() == "NOT ENOUGH INFO" and is_correct_label(instance):
        return True

    return False


def fever_score(predictions,actual=None):
    correct = 0
    strict = 0


    for idx,instance in enumerate(predictions):
        assert 'predicted_evidence' in instance.keys(), 'evidence must be provided for the prediction'

        #If it's a blind test set, we need to copy in the values from the actual data
        if 'evidence' not in instance or 'label' not in instance:
            assert actual is not None, 'in blind evaluation mode, actual data must be provided'
            assert len(actual) == len(predictions), 'actual data and predicted data length must match'
            assert 'evidence' in actual[idx].keys(), 'evidence must be provided for the actual evidence'
            instance['evidence'] = actual[idx]['evidence']
            instance['label'] = actual[idx]['label']

        assert 'evidence' in instance.keys(), 'gold evidence must be provided'

        if is_correct_label(instance):
            correct += 1

            if is_strictly_correct(instance):
                strict+=1

    total = len(predictions)

    strict_score = strict / total
    acc_score = correct / total

    return strict_score, acc_score