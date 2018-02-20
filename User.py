class User:
    username = None
    url = None
    feedback_score = None
    feedback_count = None
    trade_volume = None
    created_at = None

    def __init__(self, username=None, url=None, feedback_score=None,
                 feedback_count=None, trade_volume=None, created_at=None):
        self.username = username
        self.url = url
        self.feedback_score = feedback_score
        self.feedback_count = feedback_count
        self.trade_volume = trade_volume
        self.created_at = created_at

    def is_empty(self):
        return self.username is None or\
               self.url is None or\
               self.feedback_score is None or\
               self.feedback_count is None or\
               self.created_at is None
