import os
import shutil
import argparse
import random
random.seed(47297)

parser = argparse.ArgumentParser(description="Split train data into train and validation sets.")
parser.add_argument('task', type=str, help="Possible values are: decompensation, "\
                            "in-hospital-mortality, length-of-stay, phenotyping, multitask.")
args, _ = parser.parse_known_args()
assert args.task in ['decompensation', 'in-hospital-mortality', 'length-of-stay',
                     'phenotyping', 'multitask']

has_header = False
if args.task in ['phenotyping', 'multitask']:
    has_header = True

DATA_PATH = os.path.join(os.path.expanduser('~'), 'staging', 'data', 'mimic3-benchmarks')

header = None
with open(DATA_PATH + "/%s/train/listfile.csv" % args.task) as listfile:
    lines = listfile.readlines()
    if has_header:
        header = lines[0]
        lines = lines[1:]

patients = list(set([x[:x.find('_')] for x in lines]))

random.shuffle(patients)
train_cnt = int(0.82 * len(patients)) # this will became 70% of all data
train_patients = set(patients[:train_cnt])
val_patients = set(patients[train_cnt:])
assert len(train_patients & val_patients) == 0

train_lines = [x for x in lines if x[:x.find("_")] in train_patients]
val_lines = [x for x in lines if x[:x.find("_")] in val_patients]
assert len(train_lines) + len(val_lines) == len(lines)

if not os.path.exists(DATA_PATH + "/%s/" % args.task):
    os.makedirs(DATA_PATH + "/%s/" % args.task)

with open(DATA_PATH + "/%s/train_listfile.csv" % args.task, "w") as train_listfile:
    if has_header:
        train_listfile.write(header)
    for line in train_lines:
        train_listfile.write(line)

with open(DATA_PATH + "/%s/val_listfile.csv" % args.task, "w") as val_listfile:
    if has_header:
        val_listfile.write(header)
    for line in val_lines:
        val_listfile.write(line)

shutil.copy(DATA_PATH + "/%s/test/listfile.csv" % args.task,
            DATA_PATH + "/%s/test_listfile.csv" % args.task)
