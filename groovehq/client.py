__all__ = ('Groove',)

import re

import requests

class Groove(object):

    def __init__(self, api_token):
        self._api_token = api_token
        self._session = requests.Session()
        self._session.headers = self._headers()

    def _headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._api_token),
        }

    def list_tickets(self, **kwargs):
        """
        Return all tickets matching the criteria.

        See https://www.groovehq.com/docs/tickets#listing-tickets for more
        details.

        :param assignee: an agent email
        :param customer: a customer email or ID
        :param page: the page number
        :param per_page: how many results to return per page, defaults to 25
        :param state: One of "unread", "opened", "pending", "closed", or "spam"
        :param folder: the ID of a folder
        """

        params = { k:unicode(v) for k, v in kwargs.items() }
        resp = self._session.get('https://api.groovehq.com/v1/tickets',
                                 params=params)
        return resp.json()['tickets']

    def get_messages(self, ticket_number, **kwargs):
        """
        Get all messages for a particular ticket.

        See https://www.groovehq.com/docs/messages#listing-all-messages for more
        details.

        :param ticket_number: the integer ticket number
        :param page: the page number
        :param per_page: how many results to return per page, defaults to 25
        """
        params = { k:unicode(v) for k, v in kwargs.items() }

        url = ('https://api.groovehq.com/v1/tickets/{}/messages'
               .format(ticket_number))
        resp = self._session.get(url, params=params)
        return resp.json()['messages']

    def create_message(self, ticket_number, author, body, note=True):
        """
        Create a new message.

        See https://www.groovehq.com/docs/messages#creating-a-new-message
        for details.

        :param ticket_number: the ticket this message refers to
        :param author: the email of the owner of this message
        :param body: the body of the message
        :param note: whether this should be a private note, or sent to the
        customer.
        """
        data = {
            'author': author,
            'body': body,
            'note': note
        }
        url = ('https://api.groovehq.com/v1/tickets/{}/messages'
               .format(ticket_number))
        resp = self._session.post(url, json=data)

        result = resp.json()
        new_url = ret['message']['href']
        nums = re.findall(r'\d+', new_url)

        if len(nums) > 0:
            return nums[-1]
