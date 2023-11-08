from agent.settings import OLS4_API
import requests
import re

async def search_ols(query, k=1):
    """
    Queries the OLS and retrieves the top k definitions and their term IDs
    """
    term_ids = []
    descriptions = []
    if isinstance(query, list):
        for q in query:
            term_ids_q = []
            descriptions_q = []
            q = re.sub('\d\.','',q).strip().lower()
            url = f"{OLS4_API}search?q={{{q}}}&ontology=bao"
            r = requests.get(url)
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
                    term_ids_q.append(ontology_id)
                    descriptions_q.append(description)
                term_ids.append(term_ids_q)
                descriptions.append(descriptions_q)
            else:
                print(f"Error getting ontology terms for query {q}: {r.status_code}")
                return ["NONE"], ["NONE"]

    elif isinstance(query, str):
        query = re.sub('\d\.','',query).strip().lower()
        print(query)
        url = f"{OLS4_API}search?q={{{query}}}&ontology=bao"
        print(url)
        r = requests.get(url)
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