import lmql
from dataclasses import dataclass
from typing import List
from agent.agent_tools import get_method, search_ols

model = lmql.model("local:llama.cpp:/Users/agreen/LLMs/sciphi-mistral-7b-32k.Q4_K_M.gguf", n_ctx=4096, n_gpu_layers=1, tokenizer='mistralai/Mistral-7B-v0.1')

@dataclass
class MethodKeywords:
    tasks: List[str] 


@lmql.query(model=model, decoder="sample", n=1, temperature=0.3, max_len=4096)
async def select_ontology_term(keywords):
    '''lmql
    """
    Q: What is the best ontology term for {keywords.strip}?

    Action: Query the ontology lookup service to find candidate terms for {keywords}
    """
    term_ids, descriptions = await search_ols(keywords, k=3)
    """
    Action: Select the best term from the list of candidates
    """
    for termid, desc in zip(term_ids, descriptions):
        "{termid}: {desc}\n"
    """
    Answer: The best ontology term for {keywords} is [TERM_ID] where TERM_ID in set(term_ids)
    """
    return TERM_ID
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
        "[KEYWORD]\n" where STOPS_AT(KEYWORD, '\n')
        keywords.append(KEYWORD)

    """
    Action: Select the best ontology term for the keywords
    [BEST_TERMS: select_ontology_term(keywords)]
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
