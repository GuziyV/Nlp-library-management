import oauth2 as oauth
import urllib.parse as urlparse

from freetype import unicode

client_id = "IC5itDAhtayZ9ZIRc77qrQ"
secret = "dLvs9iojQZX3KayoSKnkpxJIhkQq1kuPxhl636pCI"

request_token_url = "https://www.goodreads.com/oauth/request_token"
authorize_url = "https://www.goodreads.com/oauth/authorize"
access_token_url = "https://www.goodreads.com/oauth/access_token"
base_url = "https://www.goodreads.com/"

#hardcoded for my machine, vova zamytu sobi sviy token, use getToken()
oauth_token_secret = '63jA8OJCgd7rG00UfzAjyPrPZSbFu9pQvaZiMHewQ'
oauth_token = 'UR13Cr1IIDWUNoOiuEtDpg'

class OAuthService:

    def getToken(self):                     #use if using first time on machine, else -> hardcoded value
        consumer = oauth.Consumer(key=client_id,
                                  secret=secret)

        client = oauth.Client(consumer)

        response, content = client.request(unicode(request_token_url, "utf-8"), 'GET')

        request_token = dict(urlparse.parse_qsl(content))

        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        client = oauth.Client(consumer, token)

        authorize_link = '%s?oauth_token=%s' % (authorize_url,
                                                request_token['oauth_token'])
        print ('Use to uathorize your MACHINA WROOOM ' + authorize_link)
        #
        accepted = 'n'
        while accepted.lower() == 'n':
            # you need to access the authorize_link via a browser,
            # and proceed to manually authorize the consumer
            accepted = input('Accepted? (y/n) ')

        response, content = client.request(unicode(access_token_url, "utf-8"), 'POST')

        access_token = dict(urlparse.parse_qsl(content))
        token = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
        return token

    def getClient(self):
        consumer = oauth.Consumer(key=client_id,secret=secret)
        #token = self.getToken()   #use if 401
        token = oauth.Token(oauth_token, oauth_token_secret)
        client = oauth.Client(consumer, token)
        return client;
