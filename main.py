"""
This is the main event loop for the agent, it will read the description of its task, decide on the tools to use, and then execute the task.
"""

import click
import json
import lmql
from tqdm import tqdm
from agent.tools.find_method import evaluate_method

@click.command()
@click.option("--input", default="input", help="Input filename")
@click.option("--output", default="output", help="Output filename")
@click.option("--model", default="sciphi-mistral-7b-32k.Q4_K_M.gguf", help="Path to model file")
@click.option("--tokenizer", default='mistralai/Mistral-7B-v0.1', help="Name of tokenizer")
@click.option("--n_gpu", default=1, help="Number of layers to offload (1 for Metal, ~40 for GPU)")
def main(input, output, model, tokenizer, n_gpu):
    pmcids = [p.strip() for p in open(input, 'r').readlines()]
    print(pmcids)
    model = lmql.model(f"local:llama.cpp:{model}", n_ctx=16384, n_gpu_layers=n_gpu, tokenizer=tokenizer)
    ## First process each pmcid and annotate it with some ontology terms
    results = {}
    for pmcid in tqdm(pmcids):
        results[pmcid] = {}

        methods = evaluate_method(pmcid, model=model)
        
        results[pmcid]["methods"] = methods

    with open(output, 'w') as o:
        json.dump(results, o)



if __name__ == "__main__":
    main()