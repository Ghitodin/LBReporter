
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

    @staticmethod
    def parse_from_json(json):
        new_user = User()
        if json is None:
            return new_user

        if 'error' in json:
            return new_user

        json_data = json['data']
        new_user.username = str(json_data['username'])
        new_user.url = str('<a href=\"' + json_data['url'] + '\"''>Link</a>')
        new_user.feedback_score = str(json_data['feedback_score'])
        new_user.feedback_count = str(json_data['feedback_count'])
        new_user.trade_volume = str(json_data['trade_volume_text'])
        new_user.created_at = str(json_data['created_at'])
        return new_user
