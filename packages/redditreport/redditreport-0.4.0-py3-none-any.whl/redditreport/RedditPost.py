class RedditPost:
    def __init__(self, submission, sub_name):
        self.submission = submission
        self.sub_name = sub_name
        self.title = self.submission.title
        self.url = self.submission.url
        self.score = self.submission.score
        self.num_comments = self.submission.num_comments

    def as_dict(self):
        return {
            'submission': self.submission,
            'sub_name': self.sub_name,
            'title': self.title,
            'url': self.url,
            'score': self.score,
            'num_comments': self.num_comments
            }