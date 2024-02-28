import unittest
from tkinter import Tk  # Import Tkinter Tk class
from unittest.mock import patch, MagicMock
from Email_Bombler_GUI import Email_Bomber_GUI

class TestEmailBomberIntegration(unittest.TestCase):
    def setUp(self):
        self.master = Tk()  # Create a dummy Tk instance
        self.app = Email_Bomber_GUI(self.master)  # Pass the dummy Tk instance as master

        self.mock_smtp = patch('smtplib.SMTP').start()
        self.mock_server = MagicMock()
        self.mock_smtp.return_value = self.mock_server

    def tearDown(self):
        self.master.destroy()  # Destroy the dummy Tk instance
        patch.stopall()  # Clean up patches

    # Your test methods go here...


    def test_successful_connection(self):
        # Set up a successful login response
        self.mock_server.login.return_value = (235, '2.7.0 Authentication successful')

        # Set EmailConnector attributes
        self.app.connector.server = 'smtp.example.com'
        self.app.connector.port = 587
        self.app.connector.from_addr = 'user@example.com'
        self.app.connector.from_pwd = 'securepassword'

        # Run the connect method, which should succeed
        self.assertTrue(self.app.connector.connect())

    def test_send_email(self):
        # Set up a successful login response
        self.mock_server.login.return_value = (235, '2.7.0 Authentication successful')

        # Pretend we successfully send an email
        self.mock_server.sendmail.return_value = {}

        # Set EmailConnector attributes
        self.app.connector.server = 'smtp.example.com'
        self.app.connector.port = 587
        self.app.connector.from_addr = 'user@example.com'
        self.app.connector.from_pwd = 'securepassword'

        # Run the connect method, which should succeed
        self.assertTrue(self.app.connector.connect())

        # Send an email, which should be caught by the mock
        self.app.connector.send_email('recipient@example.com', 'Test', 'This is a test email')

        # Verify that the mock SMTP server was used to send an email
        self.mock_server.sendmail.assert_called_with('user@example.com', 'recipient@example.com',
                                                     'From: user@example.com\nTo: recipient@example.com\nSubject: Test\n\nThis is a test email')

        # Clean up by closing the mock SMTP connection
        self.app.connector.close_connection()
        self.mock_server.quit.assert_called_with()


if __name__ == '__main__':
    unittest.main()
