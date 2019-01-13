'''
Exercise 1.
Given the contents of the GT home page as above, write a function that returns a list of links (URLs) of the "top stories" on the page.
'''

import re

def get_gt_top_stories(webpage_text):

    pattern = '''<a class="slide-link" href="(?P<url>[^"]+)"'''
    return re.findall(pattern, webpage_text)

'''
Exercise 2. 
Given a search topic, location, and a rank  kk , return the name of the  kk -th item of a Yelp! search. 
If there is no  kk -th item, return None.
'''


def find_yelp_item(topic, location, k):
    """Returns the k-th suggested item from Yelp! in Atlanta for the given topic."""
    # ANSWER:
    import re
    if k < 1: return None

    # Download page
    url_command = 'https://yelp.com/search'
    url_args = {'find_desc': topic,
                'find_loc': location,
                'start': k - 1
                }

    response = requests.get(url_command, params=url_args)

    if not response: return None
    print('Downloaded from: {}'.format(response.url))

    # Look for the line containing the name of the k-th item
    item_pattern = re.compile(
        '<span class="indexed-biz-name">{}\.[ \n\t]*.*<span >(?P<item_name>.*)</span></a>'.format(k))

    item_matches = item_pattern.findall(response.text)

    # Return the first match
    if (len(item_matches) > 0):
        return str(item_matches[0])

    # No matches, evidently
    return None