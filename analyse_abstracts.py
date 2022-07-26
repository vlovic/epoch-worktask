import feedparser
from pathlib import Path
import pickle

# Load metadata as a string
DIR = Path(__file__).parent.absolute()
with open(DIR / 'metadata.txt') as f:
    metadata = f.read()

parsed_metadata = feedparser.parse(metadata)

#KEYWORDS = ["value align", "safety", "align", "bias", "fair", "human values", " AGI ", "general intelligence", "generality", "AI safety", "interpretab", "transparent", "discriminat", "accountab", "privacy", "weapon", "lethal", "killer", "ethic", "beneficial", "convergence", "power-seeking", "AI-complete", "AI-hard", "transformative", "superintelligence", "human compatible", "human-compatible", "provably beneficial", "inverse reinforcement learning", "value alignment", "human-like", "general", "existential risk", "existential-risk", "x-risk", "control problem", "friendly", "explainab"]
more_keywords = True
keywords = []
while more_keywords:
    keyword = input("Specify a keyword, or enter q to stop:")
    if keyword == "q":
        more_keywords = False
        break
    keywords.append(keyword)

CUTOFF_YEAR = 2002

# Initialise dicts to store results
keywords_counter = {}
for keyword in keywords:
    keywords_counter[keyword] = {}

    for year in range(CUTOFF_YEAR, 2022 + 1):
        keywords_counter[keyword][year] = 0

total_papers_counter = {}

for entry in parsed_metadata.entries:
    year_published = int(entry.published[0:4])

    if int(year_published) < CUTOFF_YEAR:
        break

    if year_published not in total_papers_counter:
        total_papers_counter[year_published] = 0

    total_papers_counter[year_published] += 1

    for keyword in keywords:
        if keyword in entry.summary:
            keywords_counter[keyword][year_published] += 1


# Pickle results
with open(DIR / 'keywords_counter.pickle', 'wb') as handle:
    pickle.dump(keywords_counter, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(DIR / 'total_papers_counter.pickle', 'wb') as handle:
    pickle.dump(total_papers_counter, handle, protocol=pickle.HIGHEST_PROTOCOL)
