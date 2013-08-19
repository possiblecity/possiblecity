import urlparse

from django.conf import settings

import requests
import twitter


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class Provider(object):
    
    def __init__(self, user, provider):
        self.user = user
        self.social_auth = user.social_auth.get(provider=provider)
        if provider == "twitter":
            self.friends = self.twitter_friends
        elif provider == "linkedin-oauth2":
            self.friends = self.linkedin_friends
        elif provider == "facebook":
            self.friends = self.facebook_friends
        elif provider == "google-oauth2":
            self.friends = self.google_friends
        else:
            self.friends = lambda: []
    
    def twitter_friends(self):
        # Currently will hit a rate limit exception if the user is following > 18,000 people
        # https://dev.twitter.com/docs/api/1.1/get/friends/ids
        # https://dev.twitter.com/docs/api/1.1/get/users/lookups
        tokens = urlparse.parse_qs(
            self.social_auth.extra_data["access_token"]
        )
        tw = twitter.Twitter(auth=twitter.OAuth(
            tokens["oauth_token"][0],
            tokens["oauth_token_secret"][0],
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET
        ))
        ids_cursor = -1
        page = tw.friends.ids(cursor=ids_cursor)
        ids_cursor = page["next_cursor"]
        user_request_size = 100
        while True:
            ids = [str(x) for x in page["ids"]]
            user_sets = [
                ",".join(y)
                for y in chunks(ids, user_request_size)
            ]
            for user_set in user_sets:
                users = tw.users.lookup(user_id=user_set)
                for user in users:
                    yield user
            if ids_cursor == 0:
                break
            page = tw.friends.ids(cursor=ids_cursor)
            ids_cursor = ids_cursor["next_cursor"]
    
    def facebook_friends(self):
        # https://developers.facebook.com/docs/reference/api/user/
        params = self.social_auth.tokens
        url = "https://graph.facebook.com/me/friends/"
        r = requests.get(url, params=params)
        friends = r.json()
        while True:
            for friend in friends["data"]:
                yield friend
            next = friends["paging"].get("next")
            if next:
                friends = requests.get(next).json()
            else:
                break
    
    def google_friends(self):
        # access_token
        params = self.social_auth.tokens
        params.update({"orderBy": "alphabetical"})
        url = "https://www.googleapis.com/plus/v1/people/me/people/visible/"
        r = requests.get(url, params=params)
        data = r.json()
        while True:
            for friend in data["items"]:
                friend["name"] = friend["displayName"]
                yield friend
            next = data.get("nextPageToken")
            if next:
                params.update({"pageToken": next})
                data = requests.get(url, params=params).json()
            else:
                break
    
    def linkedin_friends(self):
        # http://developer.linkedin.com/documents/connections-api
        start = 0
        count = 500
        url = "https://api.linkedin.com/v1/people/~/connections/"
        headers = {"x-li-format": "json"}
        params = {
            "oauth2_access_token": self.social_auth.tokens["access_token"],
            "start": start,
            "count": count
        }
        r = requests.get(url, params=params, headers=headers)
        connections = r.json()
        to_read = connections.get("_total")
        while to_read > 0:
            for connection in connections["values"]:
                connection["name"] = u"{firstName} {lastName}".format(**connection)
                yield connection
            to_read -= count
            if to_read > 0:
                params["start"] += count
                connections = requests.get(url, params=params, headers=headers).json()
