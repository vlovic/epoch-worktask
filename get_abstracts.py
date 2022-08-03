import requests
import feedparser
import time
from pathlib import Path

# Create file in the same directory as this script to save all metadata
DIR = Path(__file__).parent.absolute()
with open(DIR / "metadata.txt", "w") as f:
    pass

CUTOFF_YEAR = 2002

MAX_RESULTS = 1e6
RESULTS_PER_QUERY = 1e3

URL = "http://export.arxiv.org/api/query"
PARAMS = {"search_query": "cat:cs.AI", "max_results": str(
    int(RESULTS_PER_QUERY)), "sortBy": "submittedDate"}

for i in range(int(round(MAX_RESULTS / RESULTS_PER_QUERY))):
    print(i)
    PARAMS["start"] = int(round(RESULTS_PER_QUERY * i))
    num_entries = 0
    counter = 0
    # Sometimes the API request returns 0 entries, in which case we try again.
    while num_entries != RESULTS_PER_QUERY:
        print("Trying to get papers...")
        metadata = requests.get(URL, PARAMS)
        parsed_metadata = feedparser.parse(metadata.text)
        num_entries = len(parsed_metadata.entries)
        if num_entries != RESULTS_PER_QUERY:
            time.sleep(1)
        print("Number of entries: ", num_entries)
        counter += 1
        if counter > 100:
            print("Quit program after making 100 unsuccessful API requests")
            import sys
            sys.exit()

    # Save metadata to text file
    with open(DIR / "metadata.txt", "a") as f:
        f.write(metadata.text)

    if int(parsed_metadata.entries[-1].published[0:4]) < CUTOFF_YEAR:
        break


'''
TODO: 
- change to script to accept user input to define the keywords to search for
'''
