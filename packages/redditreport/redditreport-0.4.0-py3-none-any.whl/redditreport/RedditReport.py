from redditreport import RedditPost as rp


class RedditReport:
    def __init__(self, reddit_instance, subs_list, lines_per_sub, order_posts_by='hot'):
        self.reddit = reddit_instance
        self.subs_list = subs_list
        self.lines_per_sub = lines_per_sub
        self.order_posts_by = order_posts_by
        self.report_data = {}


    def generate_data(self):
        """Get the data from Reddit and returns it as a dictionary."""

        for sub in self.subs_list:
            self.report_data[sub] = []

            if self.order_posts_by == 'new':
                self.submissions = self.reddit.subreddit(sub).new(limit=self.lines_per_sub)
            elif self.order_posts_by == 'top':
                self.submissions = self.reddit.subreddit(sub).top(limit=self.lines_per_sub)
            else:         # if value == 'hot' or is not valid
                self.submissions = self.reddit.subreddit(sub).hot(limit=self.lines_per_sub)
            
            for submission in self.submissions:
                reddit_post = rp.RedditPost(submission, sub)

                self.report_data[sub].append(reddit_post)

    
    def serialize(self):
        """Serializes report_data to a dict of strings"""

        for sub in self.report_data.keys():
            i = 0
            for post_object in self.report_data[sub]:
                self.report_data[sub][i] = post_object.__dict__
                i += 1

