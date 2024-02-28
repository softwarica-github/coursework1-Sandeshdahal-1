import unittest
from tkinter import Tk
from unittest.mock import patch
from Email_Bombler_GUI import Email_Bomber_GUI

class TestEmailBomberGUI(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = Email_Bomber_GUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("tkinter.messagebox.showinfo")
    def test_connect_button_click(self, mock_showinfo):
        # Set values for email configuration
        self.app.server_var.set("Gmail")
        self.app.port_entry.insert(0, "587")
        self.app.from_addr_entry.insert(0, "sender@example.com")
        self.app.from_pwd_entry.insert(0, "password")

        # Ensure that the connect method returns True
        with patch("Email_Bombler_GUI.EmailConnector.connect", return_value=True):
            # Simulate click on Connect button
            self.app.connect_and_enable_send()

        # Verify that messagebox.showinfo is called
        self.assertTrue(mock_showinfo.called)

    @patch("tkinter.messagebox.showerror")
    def test_invalid_connect(self, mock_showerror):
        # Set invalid values for email configuration
        self.app.server_var.set("Invalid Server")
        self.app.port_entry.insert(0, "123")
        self.app.from_addr_entry.insert(0, "sender@example.com")
        self.app.from_pwd_entry.insert(0, "password")

        # Simulate click on Connect button
        self.app.connect_and_enable_send()

        # Verify that messagebox.showerror is called
        self.assertTrue(mock_showerror.called)

    def test_get_server_address(self):
        # Test valid server names
        self.assertEqual(self.app.get_server_address("Gmail"), "smtp.gmail.com")
        self.assertEqual(self.app.get_server_address("Yahoo"), "smtp.mail.yahoo.com")
        self.assertEqual(self.app.get_server_address("Outlook"), "smtp-mail.outlook.com")

        # Test invalid server name
        self.assertEqual(self.app.get_server_address("Invalid Server"), "")

if __name__ == "__main__":
    unittest.main()
