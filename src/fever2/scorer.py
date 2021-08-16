from collections import defaultdict
from fever.scorer import fever_score


def potency(actual, *all_systems_predictions):
    if len(all_systems_predictions) == 0:
        return 0
    system_scores = map(lambda system_predictions: 1-fever_score(system_predictions, actual)[0], all_systems_predictions)
    return sum(system_scores)/len(all_systems_predictions)


def resilience(actual, predictions):
    return fever_score(predictions, actual)[0]



if __name__ == "__main__":
    import argparse, json, os

    parser = argparse.ArgumentParser()
    parser.add_argument("--actual-files")
    parser.add_argument("--breaker-dirs")
    parser.add_argument("--correct-scores")
    args = parser.parse_args()

    actual_part = []
    all_breakers_actual = []
    all_systems = defaultdict(list)


    final_scores = [float(score) for score in args.correct_scores.split(",")]
    system_potencies = {}

    for corr_score, actual_file, breaker in zip(final_scores, args.actual_files.split(","), args.breaker_dirs.split(",")):
        all_submissions = []
        actual = []

        for filename in os.listdir(breaker):
            with open(breaker+"/"+filename,"r") as file:
                file_lines = []
                for line in file:
                    line_text = json.loads(line)
                    if not "predicted_evidence" in line_text and "predicted_sentences" in line_text:
                       line_text["predicted_evidence"] = line_text["predicted_sentences"]
                    file_lines.append(line_text)
                all_submissions.append(file_lines)
                all_systems[filename].append(file_lines)

        with open(actual_file, "r") as file:
            for idx,line in enumerate(file):
                try:
                    actual.append(json.loads(line))
                except Exception as e:
                    print(idx,line)
                    raise e
            all_breakers_actual.extend(actual)
            actual_part.append(actual)

        p_score = potency(actual,*all_submissions)
        print("Breaker {0}. Potency: {1}. Correct Rate: {2}. Adjusted Potency: {3}".format(breaker,p_score, corr_score, p_score*corr_score))


    for system_name in all_systems.keys():
        system_predictions = all_systems[system_name]
        scores = []
        for breaker,breaker_correctness, breaker_actual, breaker_predictions in zip(args.breaker_dirs.split(","),final_scores,actual_part, system_predictions):
            print("Breaker {} - System {}".format(breaker,system_name))
            print(list(zip(["fever","acc","p","r","f1"],fever_score(breaker_predictions, breaker_actual))))
            scores.append(fever_score(breaker_predictions, breaker_actual)[0]*breaker_correctness)

        print("System {0}. Resilience {1}".format(system_name, sum(scores)/sum(final_scores)))
        print(list(zip(args.actual_files.split(","),scores)))
        print()
    print(" & ".join(args.breaker_dirs.split(",")))
    for system_name in all_systems.keys():
        system_predictions = all_systems[system_name]
        scores = []
        for breaker_correctness, breaker_actual, breaker_predictions in zip(final_scores,actual_part, system_predictions):
            scores.append(fever_score(breaker_predictions, breaker_actual)[0])


        print(" & ".join([system_name]+[str(round(a*100,2)) for a in scores])+ " \\\\")
