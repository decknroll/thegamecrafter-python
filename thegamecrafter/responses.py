"""
The following class names are paired with the methods listed
at the top of the api module. If you add a method to the api
module you must also add a corresponding Response class below.
"""

import requests
from urllib.parse import urlparse
from .exceptions import ResponseError

class TheGameCrafterResponse(object):
    def __init__(self, response, thegamecrafter_instance):
        self.response = response
        self.content = response.json()
        self.thegamecrafter = thegamecrafter_instance
    def __getattr__(self, name):
        if name == 'result': # no recursion!
            return None
        result = self.content.get('result')
        if name in result:
            return result[name]
        elif '_' + name in result:
            return result['_' + name]
        else:
            return None
    def __repr__(self):
        return repr(self.__dict__)


class ListResponse(TheGameCrafterResponse):
    def __init__(self, response, thegamecrafter_instance):
        super(ListResponse, self).__init__(response, thegamecrafter_instance)

        # check to make sure that you have a valid response
        if 'error' in self.content:
            return

        self.all = self.all_serial = self._get_all_serial

    def _get_all_serial(self):
        req = self.response.request
        items = self.items

        current_page = self.paging['page_number'] + 1

        while current_page <= self.paging['total_pages']:
            params = urlparse.parse_qs(req.body)
            params['_page_number'] = current_page
            resp = requests.request(req.method, req.url, params=params)
            list_resp = ListResponse(resp, self.thegamecrafter)
            items.extend(list_resp.items)
            current_page += 1

        return items


class CreateResponse(TheGameCrafterResponse):
    pass

class FetchResponse(TheGameCrafterResponse):
    pass

class UpdateResponse(TheGameCrafterResponse):
    pass

class DeleteResponse(TheGameCrafterResponse):
    pass

class AddResponse(TheGameCrafterResponse):
    pass

class Add_itemResponse(TheGameCrafterResponse):
    pass

class AddressesResponse(ListResponse):
    pass

class AdjustResponse(TheGameCrafterResponse):
    pass

class Adjust_itemResponse(TheGameCrafterResponse):
    pass

class Attach_userResponse(TheGameCrafterResponse):
    pass

class Bulk_pricingResponse(TheGameCrafterResponse):
    pass

class CardsResponse(ListResponse):
    pass

class ClaimResponse(TheGameCrafterResponse):
    pass

class Convert_to_cartResponse(TheGameCrafterResponse):
    pass

class Convert_to_wishlistResponse(TheGameCrafterResponse):
    pass

class CopyResponse(TheGameCrafterResponse):
    pass

class Cost_breakdownResponse(TheGameCrafterResponse):
    pass

class CountriesResponse(TheGameCrafterResponse):
    pass

class GamesResponse(ListResponse):
    pass

class ItemsResponse(ListResponse):
    pass

class LockResponse(TheGameCrafterResponse):
    pass

class LoginResponse(TheGameCrafterResponse):
    pass

class LogoutResponse(TheGameCrafterResponse):
    pass

class MergeResponse(TheGameCrafterResponse):
    pass

class OpinionResponse(TheGameCrafterResponse):
    pass

class Pay_creditcardResponse(TheGameCrafterResponse):
    pass

class Pay_invoiceResponse(TheGameCrafterResponse):
    pass

class Pay_shopcreditResponse(TheGameCrafterResponse):
    pass

class PublishResponse(TheGameCrafterResponse):
    pass

class QueueResponse(TheGameCrafterResponse):
    pass

class ReferencesResponse(ListResponse):
    pass

class RefundResponse(TheGameCrafterResponse):
    pass

class ReviewResponse(TheGameCrafterResponse):
    pass

class Shipping_method_optionsResponse(TheGameCrafterResponse):
    pass

class Similar_gamesResponse(ListResponse):
    pass

class Similar_partsResponse(ListResponse):
    pass

class SiteResponse(TheGameCrafterResponse):
    pass

class SsoResponse(TheGameCrafterResponse):
    pass

class StatesResponse(TheGameCrafterResponse):
    pass

class UnlockResponse(TheGameCrafterResponse):
    pass

class UnpublishResponse(TheGameCrafterResponse):
    pass
