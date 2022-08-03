import feedparser
from pathlib import Path
import matplotlib.pyplot as plt

# Load metadata as a string
DIR = Path(__file__).parent.absolute()
with open(DIR / 'metadata.txt') as f:
    metadata = f.read()

parsed_metadata = feedparser.parse(metadata)

KEYWORDS = ["safety", "align", "bias", "fair", "human values", "AGI", "general intelligence", "generality", "AI safety", "interpretab", "transparent", "discriminat", "accountab", "privacy", "weapon", "lethal", "killer", "ethic", "beneficial", "convergence", "power-seeking", "AI-complete",
            "AI-hard", "transformative", "superintelligence", "human compatible", "human-compatible", "provably beneficial", "inverse reinforcement learning", "value alignment", "human-like", "general", "existential risk", "existential-risk", "x-risk", "control problem", "friendly", ]

keywords_counter = {}
for keyword in KEYWORDS:
    keywords_counter[keyword] = {}

total_papers_counter = {}


for entry in parsed_metadata.entries:
    year_published = entry.published[0:4]

    if year_published not in total_papers_counter:
        total_papers_counter[year_published] = 0

    total_papers_counter[year_published] += 1

    for keyword in KEYWORDS:
        summary_saved = False
        if keyword in entry.summary:

            if year_published not in keywords_counter[keyword]:
                keywords_counter[keyword][year_published] = 0

            keywords_counter[keyword][year_published] += 1

# Plot results
PLOTS_DIR = DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

for keyword in keywords_counter:

    normalised_counts = {}
    for year in keywords_counter[keyword]:
        normalised_counts[year] = keywords_counter[keyword][year] / \
            total_papers_counter[year]

    x = list(normalised_counts.keys())
    y = list(normalised_counts.values())

    x_pos = list(range(len(x)))

    plt.bar(x_pos, y)
    plt.xticks(x_pos, x)
    plt.title(keyword)

    plt.savefig(PLOTS_DIR / keyword)
    plt.show()
