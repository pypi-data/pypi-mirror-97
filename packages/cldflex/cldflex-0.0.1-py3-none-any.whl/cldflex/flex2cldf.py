from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import sys
import os
import csv
from pycldf import Wordlist             
import re
import logging
logging.basicConfig(level=logging.INFO)

delimiters = ["-","="]
def xify(text):
    ids = []
    for word in text.split(" "):
        ids.append(re.sub(r'([X])\1+', r'\1', re.sub("[^(\-|\=|\~)|]", "X", word)))
    return " ".join(ids)

#This splits an object word into its morphemes, i.e. "apa-ne" -> ["apa", "-", "ne"]
def split_obj_word(word):
    output = []
    char_list = list(word)
    for i, char in enumerate(char_list):
        if len(output) == 0 or (char in delimiters or output[-1] in delimiters):
            output.append(char)
        else:
            output[-1]+=char
    return output
    
#compare forms, ignoring spaces, periods and delimiters
def form_match(str1, str2):
    var1 = [str1, str1.replace(".", " "), str1.replace(" ", ""), str1.replace("-", ""), str1.replace("=", "")]
    var2 = [str2, str2.replace(".", " "), str2.replace(" ", ""), str2.replace("-", ""), str2.replace("=", "")]
    return list(set(var1) & set(var2)) != []
     
def search_lexicon(form, meaning):

    # if form != "MISSING": print(form)
    if len(lexicon) == 0:
        return("X")
    # if meaning.upper() != meaning:
    #     new_meaning = meaning.replace(".", " ")
    # else:
    #     new_meaning = meaning
    # new_meaning = re.sub(r"(\d)\ ", r"\1.", meaning)
    new_meaning = meaning
    # form = form.replace("-", "").replace("=", "")
    for morph_id, morpheme in lexicon.items():
        lex_forms = []
        for lex_form in morpheme["forms"]:
            for sub_meaning in morpheme["meanings"]:
                if form_match(form, lex_form) and form_match(new_meaning, sub_meaning):
                    return(morph_id)
    return("X")
                    
def extractFromFlex(example, key, lang, title, fallback_exno="1"):
    start = ""
    end = ""
    speaker = ""
    if len(example.keys()) == 1:
        print("Too short")
        return None
    for i in example:
        if i == "@begin-time-offset":
            start = example[i]
        if i == "@end-time-offset":
            end = example[i]
        if i == "@speaker":
            speaker = example[i]
            
    note = ""
    exno = fallback_exno
    trans = "Missing translation"
    # print(f"Parsing {exno}…")
    if "item" in example:        
        for why_is_this_an_item in example["item"]:
            if why_is_this_an_item["@type"] == "segnum":
                exno = why_is_this_an_item["$"]
            if why_is_this_an_item["@type"] == "note" and "$" in why_is_this_an_item:
                note = why_is_this_an_item["$"]
            if why_is_this_an_item["@type"] == "gls":
                if "$"  in why_is_this_an_item.keys() and trans == "Missing translation":
                    trans = why_is_this_an_item["$"]
    sentence = ""
    obj_words = []
    gloss_words = []
    morph_id_words = []
    if type(example["words"]["word"]) == list:
        words = example["words"]["word"]
    else:
        words = [example["words"]["word"]]
    for word in words:
        if type(word["item"]) == list:
            surface_form = word["item"][0]["$"]
        else:
            surface_form = word["item"]["$"]
        obj = []
        gloss = []
        morph_ids = []
        sentence += " " + str(surface_form)
        if "morphemes" not in word.keys():
            obj_sentence = "-"
            gloss_sentence = "?"
        else:
            if type(word["morphemes"]["morph"]) == list:
               morphemes = word["morphemes"]["morph"]
            else:
               morphemes = [word["morphemes"]["morph"]]
            for morpheme in morphemes:
                if "@type" in morpheme.keys():
                    morph_type = morpheme["@type"]
                else:
                    morph_type = "stem"
                if type(morpheme["item"]) == list:
                   items = morpheme["item"]
                else:
                   items = [morpheme["item"]]
                gloss_found = False
                for item in items:
                    if item["@type"] == "txt":
                        morpheme_form = item["$"]
                        # print(f"{morph_type}: {morpheme_form}")
                        obj.append(item["$"].replace(" ",".").replace("<","").replace(">",""))
                    if item["@type"] == "gls":
                        gloss_string = ""
                        gloss_found = True
                        if "$" not in item.keys():
                            gloss_string = "?"
                        else:
                            gloss_string = str(item["$"]).replace(" ", ".")
                if not gloss_found:
                    gloss_string = "?"
                if morph_type == "prefix":
                    gloss_string += "-"
                elif morph_type == "suffix":
                    gloss_string = "-" + gloss_string
                gloss.append(gloss_string)
        for i in range(0,len(obj)-1):
            if obj[i][-1] not in delimiters and obj[i+1][0] not in delimiters:
                obj[i]+="="
        for i in range(0,len(gloss)-1):
            if gloss[i][-1] not in delimiters and gloss[i+1][0] not in delimiters:
                gloss[i]+="="
        obj_word_string = "".join(obj)
        obj_words.append(obj_word_string)
        gloss_words.append("".join(gloss))
    obj_sentence = " ".join(obj_words).replace("  "," ").replace("  "," ").replace("- ","-").replace(" -","-").replace("  ", " ").strip()
    gloss_sentence = " ".join(gloss_words).replace("  "," ").replace("  "," ").replace("- ","-").replace(" -","-").replace("  ", " ").strip()
    sentence = sentence.replace("“ ","“").replace(" ”","”")
    # print(obj_sentence)
    # print(gloss_sentence)
    # if "morphemes" not in word.keys():
    #     print(f"Word {word} is missing morphemes?")
    #     obj_sentence = "MISSING"
    #     gloss_sentence = "MISSING"
    #logging.info(xify(obj_sentence))
    for i, word in enumerate(obj_sentence.split()):
        if word == "MISSING": continue
        morph_ids = []
        gloss_word = gloss_sentence.split(" ")[i]
        #logging.info("%s '%s'" % (word, gloss_word))
        for j, component in enumerate(split_obj_word(word)):
            if component in ["-","="]:
                morph_ids.append(component)
                continue
            else:
                morph_id = search_lexicon(component, split_obj_word(gloss_word)[j])
            morph_ids.append(morph_id)
        morph_id_words.append("".join(morph_ids))
    #logging.info("Successfully parsed (%s-%s)!" % (key, exno))
    return {
        "Example_ID": "%s-%s" % (key, str(exno).replace(".","_")),
        "Language_ID": lang,
        "Segmentation": obj_sentence,
        "Gloss": gloss_sentence,
        "Translation": trans,
        "Sentence": sentence.strip(),
        "Notes": note,
        "Text_ID": key,
        "Part": exno,
         "Text_Title": title,
         "Time_Start": start,
         "Time_End": end,
         "Speaker": speaker,
         "Morpheme_IDs": " ".join(morph_id_words)
    }
    
def convert(flextext_file="", lexicon_file=""):
    if flextext_file == "":
        print("No .flextext file provided")
        return
    else:
        dir_path = os.path.dirname(os.path.realpath(flextext_file))
    global lexicon
    lexicon = {}
    if lexicon_file == "":
        print("Warning: No lexicon file provided; there will be no morpheme IDs.")
    elif ".json" in lexicon_file:
        print("Adding lexicon from JSON file…")
        lg_data = Wordlist.from_metadata(lexicon_file)
        for row in lg_data["FormTable"]:
            lexicon[row["ID"]] = {
                "forms": row["Form"],
                "meanings": row["Parameter_ID"]
            }
    elif ".csv" in lexicon_file:
        print("Adding lexicon from CSV file…")
        for row in csv.DictReader(open(lexicon_file)):
            lexicon[row["ID"]] = {
                "forms": row["Form"].split("; "),
                "meanings": row["Meaning"].split("; ")
            }
    else:
        print("Warning: No valid lexicon file provided; please provide a CLDF json file or a csv file; there will be no morpheme IDs.")
    name = flextext_file.split("/")[-1].split(".")[0]
    cldf_db = dir_path + "/%s_from_flex.csv" % name
    f = open(flextext_file, "r")
    content = f.read()
    example_list = []
    texts = bf.data(fromstring(content))["document"]["interlinear-text"]
    if type(texts) is not list:
        texts = [texts]
    print("Parsing texts…")
    for i, bs in enumerate(texts):
        if type(bs["item"]) is not list:
            title_unit = [bs["item"]]
        else:
            title_unit = bs["item"]
        title = "UNKNOWN TITLE"
        key = "UNK" + str(i)
        text_label = "unknown_text"
        lang = "UNK"
        for item in title_unit:
            if item["@type"] == "title":
                title = item["$"]
            if item["@type"] == "title-abbreviation":
                if item["@lang"] == "en":
                    text_label = item["$"]
                else:
                    lang = item["@lang"]
                    key = item["$"]
        print(f"{i+1}/{len(texts)}: {title}", end="\r")
        print()
        examples = bs["paragraphs"]["paragraph"]
        if type(examples) is not list:
            examples = [examples]
        for ex_cnt, example in enumerate(examples):
            print(f"{ex_cnt+1}/{len(examples)}", end="\r")
            if len(example) == 0:
                continue
            if "phrase" not in example["phrases"]:
                example["phrases"]["phrase"] = example["phrases"]
            if type(example["phrases"]["phrase"]) is not list:
                sub_examples = [example["phrases"]["phrase"]]
            else:
                sub_examples = example["phrases"]["phrase"]
            for sub_count, sub_example in enumerate(sub_examples):
                example_list.append(extractFromFlex(sub_example, key, lang, title, str(ex_cnt)+"."+str(sub_count)))
    with open (cldf_db, 'w') as csvfile:
        headers = ["Example_ID", "Language_ID", "Sentence", "Segmentation", "Gloss", "Translation", "Notes", "Text_ID", "Part", "Text_Title", "Time_Start", "Time_End", "Speaker", "Morpheme_IDs"]
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL, fieldnames=headers)
        writer.writeheader()
        for example in example_list:
            writer.writerow(example)