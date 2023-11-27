from agent.settings import EUROPE_PMC

import requests
from lxml import etree as ET
import re

def get_text(sec):
    """
    Takes a given section's node in the XML tree and iterates over all paragraphs, joining the text together.

    This implicitly removes any tags present, so if we need them we might have to do something more fancy
    """
    # common tags: 'title', 'p', 'italic', 'bold', 'sup', 'sub', 'underline', 'sc', 'named-content',
    # 'list', 'list-item', 'uri', 'abbrev'

    # avoid text from the following tags as they result in bad sentences
    avoid_tags = [
        'xref', 'ext-link', 'media', 'caption', 'monospace', 'label', 'disp-formula', 'inline-formula',
        'inline-graphic', 'def', 'def-list', 'def-item', 'term', 'funding-source', 'award-id', 'graphic',
        'alternatives', 'tex-math', 'sec-meta', 'kwd-group', 'kwd', 'object-id',
        '{http://www.w3.org/1998/Math/MathML}math', '{http://www.w3.org/1998/Math/MathML}mrow',
        '{http://www.w3.org/1998/Math/MathML}mi', '{http://www.w3.org/1998/Math/MathML}mo',
        '{http://www.w3.org/1998/Math/MathML}msub', '{http://www.w3.org/1998/Math/MathML}mn',
        '{http://www.w3.org/1998/Math/MathML}msup', '{http://www.w3.org/1998/Math/MathML}mtext',
        '{http://www.w3.org/1998/Math/MathML}msubsup', '{http://www.w3.org/1998/Math/MathML}mover',
        '{http://www.w3.org/1998/Math/MathML}mstyle', '{http://www.w3.org/1998/Math/MathML}munderover',
        '{http://www.w3.org/1998/Math/MathML}mspace', '{http://www.w3.org/1998/Math/MathML}mfenced',
        '{http://www.w3.org/1998/Math/MathML}mpadded', '{http://www.w3.org/1998/Math/MathML}mfrac',
        '{http://www.w3.org/1998/Math/MathML}msqrt'
    ]

    # get sentences
    # use iter method to iterate over all nodes below sec and extract text from p tags
    sec_sentences = [
        "".join(item.itertext()) for item in sec.iter(tag="p") if item.text and item.tag not in avoid_tags
    ]

    # remove multiple spaces and items with a single string
    sec_sentences = [" ".join(item.split()) for item in sec_sentences if len(item.split()) > 1]

    return " ".join(sec_sentences) if sec_sentences else ""

def get_title(tree):
    """
    Expects tree to be the root xml tree from ET.
    """
    title = tree.find("./front/article-meta/title-group/article-title")
    return title.text if title is not None else ""

def get_sections(tree, include_abstract=False):
    """
    Expects tree to be the root xml tree from ET.

    This should be easier. The XPath way, using the attribute sec-type= should be able to get what I need
    but it is totally inconsistent between articles. Hence this method gets the title in each section, then
    string matches on it. 
    """
    sections = tree.findall("./body/sec")
    section_map = {}

    # use a counter to prevent a section from being overwritten. This is mainly needed for the "other" section,
    # but will also be used for the rest of the sections as it is not possible to predict how they are named
    count = 0

    for sec in sections:
        if len(get_text(sec)) == 0:
            continue
        sec_title = sec.find("title")
        try:
            if re.match(".*intro.+", sec_title.text.lower()):
                section_map['intro' + str(count)] = sec
            elif re.match(".*results", sec_title.text.lower()):
                section_map['results' + str(count)] = sec
            elif re.match(".*discussion", sec_title.text.lower()):
                section_map['discussion' + str(count)] = sec
            elif re.match(".*conclusion.*", sec_title.text.lower()):
                section_map['conclusion' + str(count)] = sec
            elif re.match(".*method.+", sec_title.text.lower()):
                section_map['method' + str(count)] = sec
            else:
                section_map['other' + str(count)] = sec
        except AttributeError:
            # No title - don't know what it is, put it in other
            section_map['other' + str(count)] = sec

        count += 1

    if include_abstract:
        abstract = tree.find("./front/article-meta/abstract")
        section_map['abstract'] = abstract

    return section_map



def get_article(pmcid):
    """
    Given a PMCID, call epmc API to get the fulltext XML, then parse it to get the article text.
    """

    url = f"{EUROPE_PMC}{pmcid.strip()}/fullTextXML"
    r = requests.get(url)

    if r.ok:
        # parse the XML
        tree = ET.fromstring(r.content)

        title = get_title(tree)

        sections = get_sections(tree, include_abstract=False)

        full_text = "\n".join([f"{sec_name}\n" + get_text(sec) for sec_name, sec in sections.items()])
        

        return f"Title: {title}\n\nMain Text:\n{full_text}"
    else:
        print(f"Error getting article {pmcid}: {r.status_code}")
        return ""



async def get_method(pmcid):
    url = f"{EUROPE_PMC}{pmcid.strip()}/fullTextXML"
    r = requests.get(url)

    if r.ok:
        # parse the XML
        tree = ET.fromstring(r.content)

        sections = get_sections(tree, include_abstract=False)

        for key in sections.keys():
            if key.startswith("method"):

                return get_text(sections[key])
            
    else:
        print(f"Error getting article {pmcid}: {r.status_code}")
        return ""
    

if __name__ == "__main__":
    pmcid = "PMC3467063"
    url = f"{EUROPE_PMC}{pmcid.strip()}/fullTextXML"
    r = requests.get(url)
    tree = ET.fromstring(r.content)
    print(get_title(tree))