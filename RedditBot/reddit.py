# RedditBot - Reddit API
import praw

"""
simple script which implements the methods required to start using `praw`
(Python Reddit API Wrapper)
"""


class RedditBot:

    def __init__(self,
                 _client_id, _client_secret, _user_agent,
                 _refresh_token=None, _username=None, _password=None):
        """
        intialise the reddit bot
        :param _client_id: value needed to access Reddit’s API https://www.reddit.com/prefs/apps/
        :param _client_secret: value needed to access Reddit’s API https://www.reddit.com/prefs/apps/
        :param _user_agent: user agent is a unique identifier that helps Reddit determine the source of network requests
        :param _refresh_token:  permenant refresh token obtained using username and password
        """
        self._username = _username
        self._password = _password
        self.reddit = praw.Reddit(client_id=_client_id,
                                  client_secret=_client_secret,
                                  user_agent=_user_agent,
                                  redirect_uri='http://localhost:8080',
                                  refresh_token=_refresh_token,
                                  username=_username,
                                  password=_password)
        self.veify_authentication()

    def get_auth_url_for_scope(self, scopes=None, state='permenant'):
        """
        get authentication url for certain scopes and state
        :param state: temporary or permenant state
        :param scopes: list of OAuth scopes (see OAuth docs for list of scopes)
        :return:
        """
        if scopes is None:
            scopes = ['*']
        if self._username is None or self._password is None:
            raise NotImplementedError('Username and Password must be supplied')
        print(self.reddit.auth.url(scopes=scopes, state=state))

    def get_auth_refresh_token(self, _code):
        """
        get the refresh token from the authorization code
        the auth code is obtained in the redirect auth url
        :param _code: authorization code
        """
        print(self.reddit.auth.authorize(_code))

    def veify_authentication(self):
        """
        verify user authentication and print session scope
        """
        try:
            print(f'authentication successful for {self.reddit.user.me()}')
            print(self.reddit.auth.scopes())
        except Exception as e:
            print('Check credentials are valid and token is correct:', e)

    def hot_media_submissions(self, _subreddit, _limit):
        """
        get the top `x` hotteset submissions for a single subreddit or multiple
        subreddits by combining them with the `+` operator
        :param _limit: number of submissions to return
        :param _subreddit: name(s) of the subreddits
        """
        media_types = ['jpg', 'jpeg', 'png', 'gif']
        subreds = self.reddit.subreddit(_subreddit)
        for submission in subreds.hot(limit=_limit):
            if submission.is_self:
                continue
            if submission.url.split('.')[-1] in media_types:
                print(submission.url)


# program driver
# procedure to obtain permenant refresh token to use reddit api
if __name__ == '__main__':
    """
    username and password required for initial setup.
    obtain client_id and client_secret from https://www.reddit.com/prefs/apps/    
    1.
    call get_auth_url_for_scope with the bot initialised with username and password.
    visit the url printed in the console.
    copy the code supplied from the url in the browser.
    """

    # client params
    username = ''  # remove once refresh key is obtained
    password = ''  # remove once refresh key is obtained

    client_id = ''
    client_secret = ''
    user_agent = 'testscript u/test'

    # comment out when complete #
    # bot = RedditBot(client_id, client_secret, user_agent, _username=username, _password=password)
    # bot.get_auth_url_for_scope()

    """
    2.
    set the code variable below equal to the code copied from the url.
    obtained from the previous step.
    run this command to obtain the request token for the specified scope and state.
    """
    # comment out when complete #
    # code = '------------------'
    # bot.get_auth_refresh_token(code)

    """
    3.
    save the refresh token printed in the console.
    use the token to access reddit api without storing username or password.
    """
    # refresh_token = '-------------------'
    # bot = RedditBot(client_id, client_secret, user_agent, _refresh_token=refresh_token)

    # test api
    # bot.hot_media_submissions('news', 100)
