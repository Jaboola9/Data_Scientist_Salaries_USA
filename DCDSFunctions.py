"""Functions for parsing DC Data Science Data."""
def stackoverflow_feed_sorter(feed, master_keys=['id', 'title', 'summary',
                                                 'location', 'updated',
                                                 'published']):
    """Standardize feedparser.parse output from stackoverflow RSS feed."""
    out_all = []
    for entry in feed.entries:
        out = standardize_dict(entry, master_keys)
        out_all.append(out)
    return out_all


def standardize_dict(dictionary, master):
    """Check dictionary keys against master list. Return standardized output."""
    out = dict()
    for entry in master:
        if entry in dictionary.keys():
            out[f'{entry}'] = dictionary[f'{entry}']
        else:
            out[f'{entry}'] = 'None'
    return out

def load_proxies():
    url = 'https://free-proxy-list.net/'
    resp = requests.get(url)