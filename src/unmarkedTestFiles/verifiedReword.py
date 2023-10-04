import os
import random

directory = "../assets/doc_parsed"
sentences = []
for filename in os.listdir(directory):
    with open(os.path.join(directory, filename), "r", encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:
            line = line.split("\t")
            if len(line) == 1 or line[1] == "bra":
                continue
            lineLength = len(line)-1
            # if len(line[lineLength]) > 700 or len(line[lineLength]) < 100:
            #     continue
            if line[0] == "FP":
                line[0] = "TP"
            if line[0] == "FN":
                line[0] = "TN"
            # if line[0] == "TN":
            #     a = random.randrange(1, 10)
            #     if a<7:
            #         continue
            newline = line[0] + "\t" + line[lineLength]
            sentences.append(newline)

with open(os.path.join("../..", "output", "training_file.txt"), "w", encoding='utf-8') as outfile:
    for line in sentences:
        outfile.write(line)
