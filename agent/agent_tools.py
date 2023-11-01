import requests
from ingestion.from_epmc import get_sections, get_text
from agent.settings import EUROPE_PMC, OLS4_API
from lxml import etree as ET
import asyncio
import re

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
    

async def search_ols(query, k=1):
    """
    Queries the OLS and retrieves the top k definitions and their term IDs
    """
    query = re.sub('\d\.','',query).strip().lower()
    print(query)
    url = f"{OLS4_API}search?q={{{query}}}&ontology=bao"
    print(url)
    r = requests.get(url)

    term_ids = []
    descriptions = []
    if r.ok:
        data = r.json()['response']
        if len(data['docs']) == 0:
            return [], []
        elif len(data['docs']) < k:
            k = len(data['docs'])
        for i in range(k):
            if len(data['docs'][i]['description']) == 0:
                continue
            ontology_id = data['docs'][i]['obo_id']
            description = data['docs'][i]['label'] + ": " + data['docs'][i]['description'][0]
            term_ids.append(ontology_id)
            descriptions.append(description)

    print(f"Found {len(term_ids)} terms for {query}")
    return term_ids, descriptions


if __name__ == "__main__":
    query = "1. Transfection\n"
    term_ids, descriptions = asyncio.run(search_ols(query, k=10))
    print(descriptions)
    print(term_ids)