**Program to collect and analyse metadata of arXiv papers.** 

`get_abstracts.py`  requests paper metadata from the arXiv API and saves them to metadata.txt.
`analyse_abstracts.py`  parses the metadata and performs a word frequency analysis on the paper abstracts. Given a number of keywords, it counts how many abstracts contain each keyword as a function of year of publication. Results are saved as pickled Python dicts. 
`plot_results.py`  unpickles the results and plots as bar charts using `matplotlib`. 

To reproduce my results
 - Call `python get_abstracts.py` and set CUTOFF_YEAR to 2002, and CATEGORY to cs.AI when prompted. You can select other categories according to the arXiv [Category Taxonomy](https://arxiv.org/category_taxonomy).
 - Call `python analyse_abstracts.py` and specify your desired keywords when prompted.
 - Call `python plot_results.py` to plot the results in a `plots` folder. 
