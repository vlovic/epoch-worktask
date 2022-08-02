import requests
import feedparser
import time
from pathlib import Path

SAVE_DIR = Path(__file__).parent.absolute()
with open(SAVE_DIR / "paper summaries.txt", "w") as f:
    f.write("# Paper summaries that contain a keyword \n\n")

KEYWORDS = ["safety", "align", "bias", "fair", "human values", "AGI", "general intelligence", "generality", "AI safety", "interpretab", "transparent", "discriminat", "accountab", "privacy", "weapon", "lethal", "killer", "ethic", "beneficial", "convergence", "power-seeking", "AI-complete",
            "AI-hard", "transformative", "superintelligence", "human compatible", "human-compatible", "provably beneficial", "inverse reinforcement learning", "value alignment", "human-like", "general", "existential risk", "existential-risk", "x-risk", "control problem", "friendly", ]

keywords_counter = {}
for keyword in KEYWORDS:
    keywords_counter[keyword] = {}

total_papers_counter = {}

exit_program = False

start = time.time()
TOTAL_RESULTS = 1e6
RESULTS_PER_QUERY = 1e3
URL = "http://export.arxiv.org/api/query"
PARAMS = {"search_query": "cat:cs.AI", "max_results": str(
    int(RESULTS_PER_QUERY)), "sortBy": "submittedDate"}
for i in range(int(round(TOTAL_RESULTS / RESULTS_PER_QUERY))):
    print(i)
    PARAMS["start"] = int(round(RESULTS_PER_QUERY * i))
    num_entries = 0
    counter = 0
    # Sometimes the API request returns 0 entries, in which case we try again.
    while num_entries != RESULTS_PER_QUERY:
        print("Trying to get papers...")
        papers = requests.get(URL, PARAMS)
        parsed_papers = feedparser.parse(papers.text)
        num_entries = len(parsed_papers.entries)
        if num_entries != RESULTS_PER_QUERY:
            time.sleep(1)
        print("Number of entries: ", num_entries)
        counter += 1
        if counter > 100:
            exit_program = True
            break

    if exit_program:
        break

    if int(parsed_papers.entries[0].published[0:4]) < 2010:
        break

    for entry in parsed_papers.entries:
        if entry.published[0:4] not in total_papers_counter:
            total_papers_counter[entry.published[0:4]] = 0

        total_papers_counter[entry.published[0:4]] += 1

        for keyword in KEYWORDS:
            summary_saved = False
            if keyword in entry.summary:

                year_published = entry.published[0:4]
                if year_published not in keywords_counter[keyword]:
                    keywords_counter[keyword][year_published] = 0

                keywords_counter[keyword][year_published] += 1

                if not summary_saved:
                    with open(SAVE_DIR / "paper summaries.txt", "a") as f:
                        f.write(
                            f"{entry.title}, {entry.published}\n{entry.summary}\n\n")

                    summary_saved = True

print(time.time() - start)
print(total_papers_counter)
print(keywords_counter)


'''
TODO: 
- change the year cut off date to look at the last paper, rather than the first (change the index from [0] to [-1])
- change to script to accept user input to define the keywords to search for
- Save the plots to a plots foler (and create the folder)
- Separate the data collection and analysis: one script for obtaining all the papers for the past X number of years and saving the resulting Atom formatted text in a .txt file. A second script then loads that text, parses it and analyses it.
- Make all dicts have years from 2002-2022. Define a variable which is the cutoff year. 
'''
