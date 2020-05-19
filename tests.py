"""Tests for Balloonicorn's Flask app."""

import unittest
import server


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()  #creates a test client for the application 
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get('/')
        self.assertIn(b'having a party', result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get('/')
        self.assertIn(b'Please RSVP', result.data)

        self.assertNotIn(b'Party Details', result.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': 'Jane', 'email': 'jane@jane.com'}

        result = self.client.post('/rsvp', data=rsvp_info,
                                  follow_redirects=True)

        # Users who have RSVPd should NOT see 'Please RSVP'
        # Users who have RSVPd SHOULD see 'Party Details'
        self.assertNotIn(b'Please RSVP', result.data)
        self.assertIn(b'Party Details', result.data)


    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': 'Mel Melitpolski', 'email': 'mel@ubermelon.com'}

        result = self.client.post('/rsvp', data=rsvp_info,
                                  follow_redirects=True)

        # Mel shoudl never see the Party Details page
        self.assertNotIn(b'Party Details', result.data)


if __name__ == '__main__':
    unittest.main()
