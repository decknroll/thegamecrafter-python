import copy
import requests

from . import responses
from functools import reduce
from .exceptions import ResponseError, TheGameCrafterError, TimeoutError

""" Add or remove methods and API calls here. """
#FIXME find a better data structure for all this nonsense
METHODS = {}
apigroups = {
    'board' : ['squareboard', 'accordionboard', 'dominoboard', 'quarterboard', 'halfboard', 
        'stripboard', 'sliverboard', 'skinnyboard', 'smallsquareboard', 'largesquareboard'],
    'booklet' : ['tarotbooklet', 'tallbooklet', 'largebooklet', 'mediumbooklet', 
        'smallbooklet', 'jumbobooklet'],
    'bookletpage' : ['tarotbookletpage', 'tallbookletpage', 'largebookletpage', 
        'mediumbookletpage', 'smallbookletpage', 'jumbobookletpage'],
    'card' : ['pokercard', 'eurosquarecard', 'usgamecard', 'dominocard', 'circlecard', 
        'bridgecard', 'squarecard', 'smallsquarecard', 'businesscard', 'hexcard', 
        'jumbocard', 'microcard', 'minicard', 'tarotcard'],
    'deck' : ['pokerdeck', 'eurosquaredeck', 'usgamedeck', 'dominodeck', 'circledeck', 
       'bridgedeck', 'squaredeck', 'smallsquaredeck', 'businessdeck', 'hexdeck', 
       'jumbodeck', 'microdeck', 'minideck', 'tarotdeck'],
    'dial' : ['smalldial', 'dualdial'],
    'punchout' : ['largesquarechit', 'largecirclechit', 'mediumcirclechit', 'mediumsquarechit', 
        'smallcirclechit', 'smallsquarechit', 'smallstandee', 'mediumstandee', 
        'largestandee', 'smallring', 'mediumring', 'largering', 'stripchit', 'dominochit', 
        'arrowchit', 'mediumtrianglechit'],
    'foldingboard' : ['bifoldboard', 'quadfoldboard', 'sixfoldboard'],
    'mat' : ['largehexmat', 'usgamemat', 'hexmat', 'stripmat', 'slivermat', 'squaremat', 
            'smallsquaremat', 'skinnymat', 'largesquaremat', 'bigmat', 'spinnermat', 'halfmat', 
            'quartermat', 'flowermat', 'invadermat'],
    'probox' : ['smallprobox', 'mediumprobox', 'largeprobox'],
    'scorepad' : ['smallscorepad', 'mediumscorepad', 'largescorepad'],
    'shard' : ['squareshard', 'hexshard', 'circleshard'],
    'sticker' : ['tokensticker', 'dicesticker', 'pawnsticker', 'meeplesticker', 'boxtopwrap', 
        'boxbottomwrap'],
    'tile' : ['largehextile', 'smallhextile', 'minihextile', 'largesquaretile', 
        'smallsquaretile', 'minisquaretile', 'dominotile', 'triangletile'],
    'tuckbox' : ['mediumgamebox', 'tarottuckbox40', 'tarottuckbox90', 'jumbotuckbox90', 'squaretuckbox48', 
        'squaretuckbox96', 'bridgetuckbox54', 'bridgetuckbox96', 'pokercardwrap18', 
        'pokertuckbox36', 'pokertuckbox54', 'pokertuckbox72', 'pokertuckbox90', 
        'pokertuckbox108'],
}

# all the APIs with create+fetch+update+delete
for apiname in (
        [
            'actionshot', 'announcement', 'cart', 'designer', 'designerassociate', 'document',
            'file', 'folder', 'game', 'gamedownload', 'gamepart', 'idea', 'opinion', 'part',
            'playmoney', 'largeretailbox', 'review', 'taxonomy', 'user', 'wishlist', 'address'
        ]
        +
        # also every apiname in every named group
        reduce(lambda l, key: l+apigroups[key], apigroups, [])
    ):
    METHODS[apiname] = {
        'create': ['POST', apiname],
        'fetch': ['GET', apiname, ''],
        'update': ['PUT', apiname, ''],
        'delete': ['DELETE', apiname, ''],
    }
# except user/create
del METHODS['user']['create']

# all the APIs with list
for apiname in ['announcement', 'designer', 'game', 'idea', 'part', 'review', 'user']:
    METHODS[apiname+'s'] = { 'list' : ['GET', apiname] }
METHODS['taxonomies'] = { 'list' :  ['GET', 'taxonomy'] }

# all the APIs with _options
for apiname in (
        ['cart', 'designer', 'document', 'game', 'part', 'user', 'wishlist', 'address']
        +
        apigroups['card']
    ):
    METHODS[apiname]['options'] = ['GET', apiname, '_options']

# additional methods for existing apis
for apiname in apigroups['deck']:
    METHODS[apiname]['cards'] = ['GET', apiname, '', 'cards']
METHODS['cart']['add'] = ['POST', 'cart', '', 'sku', '']
METHODS['cart']['adjust'] = ['PUT', 'cart', '', 'sku', '']
METHODS['cart']['shipping_method_options'] = ['GET', 'cart', '', 'shipping-method-options']
METHODS['cart']['attach_user'] = ['POST', 'cart', '', 'user']
METHODS['cart']['pay_shopcredit'] = ['POST', 'cart', '', 'payment', 'shopcredit']
METHODS['cart']['pay_invoice'] = ['POST', 'cart', '', 'payment', 'invoice']
METHODS['cart']['pay_creditcard'] = ['POST', 'cart', '', 'payment', 'invoice']
METHODS['cart']['convert_to_wishlist'] = ['POST', 'cart', '', 'wishlist']
METHODS['cart']['items'] = ['GET', 'cart', '', 'items']
METHODS['designer']['games'] = ['GET', 'designer', '', 'games']
METHODS['file']['references'] = ['GET', 'file', '', 'references']
METHODS['game']['review'] = ['POST', 'game', '', 'review']
METHODS['game']['copy'] = ['POST', 'game', '', 'copy']
METHODS['game']['publish'] = ['POST', 'game', '', 'public']
METHODS['game']['unpublish'] = ['DELETE', 'game', '', 'public']
METHODS['game']['similar_games'] = ['GET', 'game', '', 'similar']
METHODS['game']['bulk_pricing'] = ['GET', 'game', '', 'bulk-pricing']
METHODS['game']['cost_breakdown'] = ['GET', 'game', '', 'gameledgerentries']
METHODS['idea']['opinion'] = ['POST', 'idea', '', 'opinions']
METHODS['idea']['merge'] = ['POST', 'idea']
METHODS['idea']['lock'] = ['PUT', 'idea', '', 'lock']
METHODS['idea']['unlock'] = ['PUT', 'idea', '', 'unlock']
METHODS['part']['similar_parts'] = ['GET', 'part', '', 'similar']
METHODS['user']['addresses'] = ['GET', 'user', '', 'addresses']
METHODS['wishlist']['add_item'] = ['POST', 'wishlist', '', 'sku', '']
METHODS['wishlist']['adjust_item'] = ['PUT', 'wishlist', '', 'sku', '']
METHODS['wishlist']['attach_user'] = ['POST', 'wishlist', '', 'user']
METHODS['wishlist']['convert_to_cart'] = ['POST', 'wishlist', '', 'cart']
METHODS['address']['countries'] = ['GET', 'address', 'countries']
METHODS['address']['states'] = ['GET', 'address', 'states']

# novel APIs
METHODS['cp_purchase'] = {
    'claim' : ['POST', 'claim-cp-purchase'],
    'refund' : ['POST', 'refund-cp-purchase'],
}
METHODS['receipt'] = {'fetch' : ['GET', 'receipt', '']}
METHODS['session'] = {
    'login' : ['POST', 'session'],
    'logout' : ['DELETE', 'session', ''],
    'fetch' : ['GET', 'session'],
    'sso' : ['POST', 'session', 'sso', ''],
}
METHODS['sku'] = {
    'fetch' : ['GET', 'sku'],
}
METHODS['status'] = {
    'fetch' : ['GET', 'status'],
    'site' : ['GET', 'status', 'site'],
    'queue' : ['GET', 'status', 'queue'],
}

class TheGameCrafter():
    """ TheGameCrafter API class."""
    def __init__(self, host='www.thegamecrafter.com', secure=True,
                 username=None, password=None, apikey=None,
                 raise_on_errors=False, timeout=None, **kwargs):
        self.host = host
        self.auth = False
        if username and password and apikey:
            params = {'api_key_id': apikey, 'username' : username, 'password': password}
            response = requests.post('https://www.thegamecrafter.com/api/session', params=params)
            self.session_id = response.json()['result']['id']
            self.auth = True

        self.secure = secure
        self.resource  = False
        self.method = False
        self.call_params = False
        self.json = ''
        self.uri = ''
        self.raise_on_errors = raise_on_errors
        self.timeout = timeout

    def __getattr__(self, name):
        if name.startswith('__') or self.method:
            """ can't chain another attribute after the method and
            when __ the copying causes recurssion. """
            raise AttributeError(name)
        elif self.resource:
            if name in list(METHODS[self.resource].keys()):
                self.method = name
            else:
                raise TheGameCrafterError('The \'%s\' attribute is not currently defined.'
                                    % name)
        else: # since self.resource and method_call_dict are empty this must be resource.
            if name in METHODS:
                self.resource = name
            else:
                raise TheGameCrafterError('The \'%s\' resource is not currently defined.'
                                    % name)
        new_instance = copy.copy(self)
        self.resource = self.method = False
        return new_instance

    def __call__(self, *args, **kwargs):
        if self.method is False: # only run calls on methods, not resources.
            raise TheGameCrafterError('Parameters can only be passed to specific methods.')
        self.args = args
        self.kwargs = kwargs
        return self._call_api()

    def _call_api(self):
        self.uri = uri = self._make_uri()
        endpoint = METHODS[self.resource][self.method]
        http_method = endpoint[0]
        params = self.kwargs.copy()
        params['_include_relationships'] = 1
        if self.auth:
            params['session_id'] = self.session_id

        try:
            res = requests.request(http_method, uri, data=params,
                                   json=self.json, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError(exc)

        if res.status_code >= 400 and self.raise_on_errors:
            raise ResponseError(res)

        # wrap response is response classes.
        response = getattr(responses, self._class_name())(res, self)

        if self.raise_on_errors and 'error' in response.content:
            raise ResponseError(res)

        return response

    def _class_name(self):
        return '%sResponse' % self.method.capitalize()

    def _make_uri(self):
        endpoint = METHODS[self.resource][self.method]
        protocol = 'https' if self.secure else 'http'
        base = "%s://%s/api" % (protocol, self.host)
        # insert params into the endpoint
        new_endpoint = []
        param_index = 0
        for word in endpoint[1:]:
            if word == '':
                try:
                    new_endpoint.append(str(self.args[param_index]))
                    param_index += 1
                except:
                    raise TheGameCrafterError('Too few parameters for this call.')
            else:
                new_endpoint.append(word)
        if param_index != len(self.args):
            raise TheGameCrafterError('Too many parameters for this call.')
        uri = '/'.join([base] + new_endpoint)
        return uri
