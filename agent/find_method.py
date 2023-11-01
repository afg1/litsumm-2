import lmql
from dataclasses import dataclass
from typing import List
from agent.agent_tools import get_method, search_ols

model = lmql.model("local:llama.cpp:/Users/agreen/LLMs/sciphi-mistral-7b-32k.Q4_K_M.gguf", n_ctx=4096, n_gpu_layers=1, tokenizer='mistralai/Mistral-7B-v0.1')

@dataclass
class MethodKeywords:
    tasks: List[str] 


@lmql.query(model=model, decoder="sample", n=1, temperature=0.3, max_len=4096)
async def select_ontology_term(terms: List[str]):
    '''lmql
    
    "Q: Among {terms}, which are the best ontology terms? Choose only one per keyword, and give only the ontology ID with no other characters."

    "A: Let's think step by step. \n [REASONING]\n"
    
    "The comma separated list of the best terms is therefore: [TERM_ID]"
    return TERM_ID.strip()
    '''

@lmql.query(model=model, decoder="sample", n=1, temperature=0.3, max_len=4096)
def evaluate_method(pmcid):
    '''lmql
    """
    Q: What type of method is used in {pmcid}?

    """
    method = await get_method(pmcid)
    keywords = []
    """
    {pmcid} method section: {method}\n
    Action: Select three keywords/phrases from the method that adequately describe the techniques and assays used in it
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
    [TERM_IDS: select_ontology_term(terms=[flat_termids])]
    """
    '''



# best_terms = []
#     for keyword in keywords:
#         term_id = await select_ontology_term(keyword, output_writer=lmql.printing)
#         best_terms.append(term_id)
    
#     return best_terms



if __name__ == "__main__":
    import asyncio
    kw = evaluate_method("PMC9360041", output_writer=lmql.printing)
    print(kw)
    # asyncio.run(select_ontology_term("1. Transfection\n", output_writer=lmql.printing))
