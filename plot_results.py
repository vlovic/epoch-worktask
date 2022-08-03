import pickle
from pathlib import Path
import matplotlib.pyplot as plt

DIR = Path(__file__).parent.absolute()

# Unpickle results
with open(DIR / 'keywords_counter.pickle', 'rb') as handle:
    keywords_counter = pickle.load(handle)

with open(DIR / 'total_papers_counter.pickle', 'rb') as handle:
    total_papers_counter = pickle.load(handle)

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
    # plt.show()
    plt.close()
