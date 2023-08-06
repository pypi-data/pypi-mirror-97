from docx import Document
import pynterlinear
import csv


def convert(filename, example_ids, all=False):
    reader = csv.DictReader(open(filename))
    example_data = {}
    for row in reader:
        example_data[row['Example_ID']] = row
        
    examples = []
    for my_id, ex in example_data.items():
        examples.append({
            "id": ex["Example_ID"],
            "surf": ex["Sentence"],
            "obj": ex["Segmentation"],
            "gloss": ex["Gloss"],
            "trans": ex["Translation"],
        })
    if all:
        examples_to_print = examples
    else:
        examples_to_print = []
        for example in examples:
            if example["id"] in example_ids:
                examples_to_print.append(example)
    document = pynterlinear.convert_to_word(examples_to_print, use_tables=False)
    document.save('ex_from_csv.docx')