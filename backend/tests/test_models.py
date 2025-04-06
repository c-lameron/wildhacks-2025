import unittest
from backend.models.user import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(1, "test@example.com", "testuser")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")

if __name__ == '__main__':
    unittest.main()