"""
Query the Litscan API to get all PMCIDs for a given RNA ID.
"""
import furl
import requests
from agent.settings import LITSCAN_API

def query_litscan(job_id):
    """
    Query Litscan for a job ID
    Check it is in lowercase and lowercase if not
    """
    
    url = furl.furl(LITSCAN_API)
    query = f"job_id:\"{job_id}\""
    url.add({"query":query, "format":"json", "fields":"pmcid"})
    print(url.url)
    r = requests.get(url.url)
    if r.ok:
        return r.json()
    else:
        print(f"Error getting job {job_id}: {r.status_code}")
        return ""
    
def extract_pmcids(result):
    pmcids = []
    for res in result['entries']:
        pmcid = res['fields']['pmcid']
        if len(pmcid) > 0:
            pmcids.append(pmcid[0])
    return pmcids

def get_pmcids(rna_id):
    rna_id = rna_id.lower()

    r = query_litscan(rna_id)
    pmcids = extract_pmcids(r)
    return pmcids

if __name__ == "__main__":
    r = query_litscan("pral")
    pmcids = extract_pmcids(r)
    print(pmcids)