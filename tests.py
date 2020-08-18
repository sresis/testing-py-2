import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """Test to show RSVP form but NOT party details."""
        
        result = self.client.get("/")
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"Party Details", result.data)



    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertNotIn(b"Please RSVP", result.data)
        self.assertIn(b"Party Details", result.data)

   


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """test games page."""

        #tests to see if both games show up
        result = self.client.get("/games")
        self.assertIn(b"Fun Game", result.data)
        self.assertIn(b"Another Game", result.data)
 


if __name__ == "__main__":
    unittest.main()
