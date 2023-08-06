# RedditReport
Python package created for [trendsreport.app](https://trendsreport.app)

This package relies on [praw](https://praw.readthedocs.io/en/latest/) library to communicate with Reddit API. To install it:
```
pip install praw==7.1.4
pip install redditreport
```

## Classes
### RedditUser
It represents a Reddit account to interact with the Reddit API. Its only method `get_reddit_instance` returns a `praw` Reddit instance.

### RedditPost
It represents the Reddit post. It contains a `praw` submission object and some post data:
* sub_name
* title
* url
* score
* num_comments

Its only method `as_dict` returns a Python dict object with the data stored in it.

You don't need to use this class unless you want to modify what the report contains.

### RedditReport
It represents the actual Reddit report. In order to work, it needs to be passed in some initial attributes:
* `reddit` -> a `praw` Reddit instance. You can get it usig RedditUser's `get_reddit_instance` method.
* `subs_list` -> a Python list object with the names (as strings) of the subreddits you do want to include in the report.
* `lines_per_sub` -> a maximum post limit per sub in the report. 

The report data is stored in its `report_data` attribute as a Python dict.

It has two methods:
* `generate_data` which populates `report_data` dict with RedditPost's objects.
* `serialize` which transform every object inside `report_data` into a dict of strings.

# Example

```
from redditreport.core import RedditUser as ru
from redditreport.core import RedditReport as rr

# Your Reddit API credentials.
# More info: https://www.geeksforgeeks.org/python-praw-python-reddit-api-wrapper/
client_id = 'your-client-id'
client_secret = 'your-client-secret'
user_agent = 'your-user-agent'
reddit_user = ru.RedditUser(client_id, client_secret, user_agent)

# Reddit object instance from praw library
reddit_instance = reddit_user.get_reddit_instance()

# RedditReport instance
subs_list = ['pics', 'askreddit']   # must be a list
lines_per_sub = 3   # must be an integer
reddit_report = rr.RedditReport(reddit_instance, subs_list, lines_per_sub)

# Pulls data from Reddit
report_data = reddit_report.generate_data()

# Serializes it
serialized_report_data = reddit_report.serialize()

```
