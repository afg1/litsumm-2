async def wikipedia(q):
   from lmql.http import fetch
   try:
      q = q.strip("\n '.")
      print(f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={q}&origin=*")
      pages = await fetch(f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={q}&origin=*", "query.pages")
      return list(pages.values())[0]["extract"][:280]
   except:
      return "No results"