from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import sys
import os
import re
import csv
import unicodedata
import logging
logging.basicConfig(level=logging.INFO)

def listify(item):
    if type(item) is not list:
        return [item]
    else:
        return item
        
def convert(lift_file="", lg_id=None):
    logging.info(f"Processing lift file {lift_file}")
    dir_path = os.path.dirname(os.path.realpath(lift_file))
    name = lift_file.split("/")[-1].split(".")[0]
    cldf_db = dir_path + "/%s_from_lift.csv" % name
    f = open(lift_file, "r")
    content = f.read().replace("http://www.w3.org/1999/xhtml","")
    morphemes = {}
    for entry in bf.data(fromstring(content))["lift"]["entry"]:
        morph_id = entry["@guid"].replace("-", "_")
        if "relation" in entry.keys():
            continue
        trait_entry = listify(entry["trait"])
        morph_type = trait_entry[0]["@value"]
        forms = [entry["lexical-unit"]["form"]["text"]["$"]]
        if not lg_id:
            lg_id = entry["lexical-unit"]["form"]["@lang"]
        sense_entries = listify(entry["sense"])
        glosses = []
        for sense_entry in sense_entries:
            if "gloss" not in sense_entry:
                continue
            glosses.append(str(sense_entry["gloss"]["text"]["$"]))
        gloss = "; ".join(glosses)
        if "variant" in entry.keys():
            if type(entry["variant"]) != list:
                variants = [entry["variant"]]
            else:
                variants = entry["variant"]
            for variant in variants:
                if "form" not in variant.keys():
                    continue
                variant_form = variant["form"]["text"]["$"]
                variant_morph_type = variant["trait"]["@value"]
                forms.append(variant_form)
        # print("%s '%s'" % ("; ".join(forms), gloss))
        if gloss != "" and "".join(forms) != "":
            ascii_form = unicodedata.normalize("NFKD", "".join(forms)).encode("ascii", "ignore").decode("ascii")
            my_id = re.sub(r'[^A-Za-z0-9_]+', '', ascii_form).replace(" ","_").replace("*","_")
            append = ""
            c = 0
            while my_id + append in morphemes.keys():
                c += 1
                append = str(c)
            morphemes[my_id + append] = {
                "Form": "; ".join(forms),
                "ID": morph_id,#my_id + append,
                "Meaning": "; ".join([str(gloss)]),
                "Language_ID": lg_id,
                # "FLEx_ID": morph_id
            }
    with open(cldf_db, 'w') as csvfile:
        headers = ["ID", "Language_ID", "Form", "Meaning"]
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL, fieldnames=headers)
        writer.writeheader()
        for i, m in enumerate(morphemes.values()):
            # print("%s. %s : %s" % (i, m["Form"], m["Meaning"]))
            writer.writerow(m)