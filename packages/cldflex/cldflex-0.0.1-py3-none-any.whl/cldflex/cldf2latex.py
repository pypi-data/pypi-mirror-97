import csv
import pynterlinear
import pyperclip
import datetime
from string import Template

class DeltaTemplate(Template):
    delimiter = "%"
    
def get_time(str):
    fmt = '%H:%M:%S'
    tdelta = datetime.timedelta(seconds=int(str)/1000)
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)
    
def convert(filename, example_ids, all=False, from_corpus=True):
    reader = csv.DictReader(open(filename))
    example_data = {}
    for row in reader:
        example_data[row['Example_ID']] = row
    
    examples = []
    def get_example_hash(ex):
        print(ex)
        if "Speaker" not in ex.keys():
            from_corpus = False
        ex_hash = {
                "id": ex["Example_ID"],
                "obj": ex["Segmentation"],
                "language": ex["Language"],
                "gloss": ex["Gloss"],
                "trans": ex["Translation"],
                "surface": ex["Sentence"],
                "parnote": ex["Information"]
            }
        if from_corpus:
            ex_hash["speaker"] = ex["Speaker"]
            ex_hash["text_id"] = ex["Text_ID"]
            ex_hash["part"] = ex["Part"]
            if ex["Time_Start"] != "":
                ex_hash["start"] = get_time(ex["Time_Start"])
                ex_hash["end"] = get_time(ex["Time_End"])

        else:
            ex_hash["source"] = ex["Source"]
        return ex_hash
            
    if all:
        for key, ex in example_data.items():
            examples.append(get_example_hash(ex))
        output = ""
        for ex in examples:
            output += pynterlinear.convert_to_expex([ex], from_corpus=from_corpus, for_beamer=False) + "\n\n"
    else:
        for key in example_ids:
            ex = example_data[key]
            examples.append(get_example_hash(ex))
        if "Speaker" not in example_data[example_ids[0]].keys():
            from_corpus = False
        output = pynterlinear.convert_to_expex(examples, from_corpus=from_corpus, for_beamer=False)
    
    for form in pynterlinear.get_unknown_abbrevs():
        print("\\newGlossingAbbrev{%s}{%s}" % (form, form))
    pyperclip.copy(output)