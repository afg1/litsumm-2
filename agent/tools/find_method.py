import lmql
from dataclasses import dataclass
from typing import List
from agent.tools.functions.epmc import get_method
from agent.tools.functions.ols import search_ols

@dataclass
class Result:
    terms: List[str]



@lmql.query(decoder="sample", n=1, temperature=0.1, max_len=16384)
async def select_ontology_term(terms: List[str]):
    '''lmql
    
    """Q: Among {terms}, which are the best ontology terms? \n
    Choose only one per keyword, and give only the ontology ID with no other characters.
    A: Let's think step by step.
    [REASONING]
    
    Return the terms as a comma separated list with no [[]]:
    [TERM_ID]

    """ where STOPS_AT(TERM_ID, "\n")
    
    return TERM_ID.strip().split(',')
    '''
#and type(TERM_ID) is Result STOPS_AT(TERM_ID, "}") and
@lmql.query(decoder="sample", n=1, temperature=0.1, max_len=16384)
def evaluate_method(pmcid):
    '''lmql
    """
    Q: What type of method is used in {pmcid}?

    """
    method = await get_method(pmcid)
    keywords = []
    """
    {pmcid} method section: {method}\n
    Action: Select three keywords/phrases from the method that describe the most important techniques and assays used 
    Keywords: 
    """
    for i in range(4):
        "[KEYWORD]\n" where STOPS_AT(KEYWORD, '\n') and len(KEYWORD) > 2
        keywords.append(KEYWORD)
    keywords = [k.strip() for k in keywords]

    """
    {keywords}
    Action: Select the best ontology term for the keywords

    Action: Query the ontology lookup service to find candidate terms for {keywords}
    """
    term_ids, descriptions = await search_ols(keywords, k=3)
    flat_termids = [item for sublist in term_ids for item in sublist]
    if len(flat_termids) == 0:
        return ["NONE"]
    if isinstance(term_ids[0], list):
        for termid_q, desc_q, keyword_q in zip(term_ids, descriptions, keywords):
            "{keyword_q}:\n"
            for termid, desc in zip(termid_q, desc_q):
                "{termid}: {desc}\n"
    else:
        for termid, desc in zip(term_ids, descriptions):
            "{termid}: {desc}\n"

    """
    Q: Which are the best ontology terms for this method?
    [TERM_IDS: select_ontology_term(terms=flat_termids)] 
    """
    return TERM_IDS
    '''

if __name__ == "__main__":
    import asyncio
    # kw = evaluate_method("PMC9360041", output_writer=lmql.printing)
    terms = evaluate_method("PMC1762435", output_writer=lmql.printing)
    print(terms)
    # asyncio.run(select_ontology_term("1. Transfection\n", output_writer=lmql.printing))
