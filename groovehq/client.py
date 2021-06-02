__all__ = ("Groove",)

import datetime
import re

import requests


class Groove(object):
    def __init__(self, api_token):
        self._api_token = api_token
        self._session = requests.Session()
        self._session.headers = self._headers()

    def _headers(self):
        return {"Authorization": "Bearer {}".format(self._api_token)}

    def list_agents(self):
        """
        Return all agents.
        """
        resp = self._session.get("https://api.groovehq.com/v1/agents")
        return resp.json()["agents"]

    def get_agent(self, email):
        """
        Find the agent whose email is *email*.

        :param email: the agent's email.
        """
        resp = self._session.get(f"https://api.groovehq.com/v1/agents/{email}")
        return resp.json()["agent"]

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

        params = kwargs.items()
        resp = self._session.get(
            "https://api.groovehq.com/v1/tickets", params=params
        )
        return resp.json()["tickets"]

    def get_messages(self, ticket_number, **kwargs):
        """
        Get all messages for a particular ticket.

        See https://www.groovehq.com/docs/messages#listing-all-messages for
        more details.

        :param ticket_number: the integer ticket number
        :param page: the page number
        :param per_page: how many results to return per page, defaults to 25
        """
        params = kwargs.items()

        url = "https://api.groovehq.com/v1/tickets/{}/messages".format(
            ticket_number
        )
        resp = self._session.get(url, params=params)
        return resp.json()["messages"]

    def create_ticket(
        self,
        body,
        from_,
        to,
        mailbox="",
        assigned_group="",
        assignee="",
        sent_at=None,
        note=False,
        send_copy_to_customer=False,
        state="unread",
        subject="",
        tag="",
    ):

        if sent_at is None:
            sent_at = datetime.datetime.now()

        data = {
            "body": body,
            "from": from_,
            "to": to,
            "mailbox": mailbox,
            "assigned_group": assigned_group,
            "assignee": assignee,
            "sent_at": sent_at.strftime("%a, %d %b %Y %H:%M:%S"),
            "note": note,
            "send_copy_to_customer": send_copy_to_customer,
            "state": state,
            "subject": subject,
            "tag": tag,
        }
        resp = self._session.post(
            "https://api.groovehq.com/v1/tickets/", json=data
        )
        return resp.json()["ticket"]

    def update_ticket(self, ticket_number, state):
        """Update a ticket's state.

        Args:
            ticket_number (int): The ID of the ticket to update.
            state (str): The state of the ticket. Can be "unread", "opened",
                "pending", "closed", or "spam".

        Returns:
            None

        """
        self._session.put(
            f"https://api.groovehq.com/v1/tickets/{ticket_number}/state",
            json={"state": state},
        )

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
        data = {"author": author, "body": body, "note": note}
        url = "https://api.groovehq.com/v1/tickets/{}/messages".format(
            ticket_number
        )
        resp = self._session.post(url, json=data)

        result = resp.json()
        new_url = result["message"]["href"]
        nums = re.findall(r"\d+", new_url)

        if len(nums) > 0:
            return nums[-1]

    def get_customer(self, customer_id):
        """
        Fetch a customer whose id is *customer_id*.

        *customer_id* can be an actual ID or an email address.

        See https://www.groovehq.com/docs/customers#finding-one-customer
        for details.

        :param customer_id: the ID / email address of the customer.
        """
        url = "https://api.groovehq.com/v1/customers/{}".format(customer_id)
        resp = self._session.get(url)
        result = resp.json()
        return result["customer"]

    def update_customer(
        self,
        email,
        name=None,
        about=None,
        twitter_username=None,
        title=None,
        company_name=None,
        phone_number=None,
        location=None,
        linkedin_username=None,
        custom=None,
    ):
        data = {"email": email}
        if name is not None:
            data["name"] = name
        if about is not None:
            data["about"] = about
        if twitter_username is not None:
            data["twitter_username"] = twitter_username
        if title is not None:
            data["title"] = title
        if company_name is not None:
            data["company_name"] = company_name
        if phone_number is not None:
            data["phone_number"] = phone_number
        if location is not None:
            data["location"] = location
        if linkedin_username is not None:
            data["linkedin_username"] = linkedin_username
        if custom is not None:
            data["custom"] = {}
        resp = self._session.put(
            f"https://api.groovehq.com/v1/customers/{email}", json=data
        )
        result = resp.json()
        return result["customer"]

    def create_customer(
        self,
        email,
        name=None,
        about=None,
        twitter_username=None,
        title=None,
        company_name=None,
        phone_number=None,
        location=None,
        linkedin_username=None,
        custom=None,
    ):
        data = {"email": email}
        if name is not None:
            data["name"] = name
        if about is not None:
            data["about"] = about
        if twitter_username is not None:
            data["twitter_username"] = twitter_username
        if title is not None:
            data["title"] = title
        if company_name is not None:
            data["company_name"] = company_name
        if phone_number is not None:
            data["phone_number"] = phone_number
        if location is not None:
            data["location"] = location
        if linkedin_username is not None:
            data["linkedin_username"] = linkedin_username
        if custom is not None:
            data["custom"] = {}
        resp = self._session.post(
            "https://api.groovehq.com/v1/customers/", json=data
        )
        result = resp.json()
        return result["customer"]
