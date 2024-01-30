import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

class GroceryBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Store Billing System")
        self.root.geometry("800x600")

        # Initialize variables
        self.customer_name_var = tk.StringVar()
        self.customer_email_var = tk.StringVar()
        self.customer_contact_var = tk.StringVar()
        self.customer_address_var = tk.StringVar()

        self.item_name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()
        self.total_var = tk.DoubleVar()

        # Create UI elements for customer details
        tk.Label(root, text="Customer Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.customer_name_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.customer_email_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Contact Number:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.customer_contact_var).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.customer_address_var).grid(row=3, column=1, padx=10, pady=10)

        # Create UI elements for item details
        tk.Label(root, text="Item Name:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.item_name_var).grid(row=4, column=1, padx=10, pady=10)

        tk.Label(root, text="Quantity:").grid(row=5, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.quantity_var, width=10).grid(row=5, column=1, padx=10, pady=10)

        tk.Label(root, text="Price per unit:").grid(row=6, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.price_var, width=10).grid(row=6, column=1, padx=10, pady=10)

        tk.Button(root, text="Add Item", command=self.add_item).grid(row=7, column=0, columnspan=2, pady=10)

        self.item_listbox = tk.Listbox(root, height=10, width=60)
        self.item_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(root, text="Total:").grid(row=9, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.total_var, state="readonly", width=10).grid(row=9, column=1, padx=10, pady=10)

        tk.Button(root, text="Generate Bill", command=self.generate_bill).grid(row=10, column=0, pady=10)
        tk.Button(root, text="Share Bill", command=self.share_bill).grid(row=10, column=1, pady=10)

        # Initialize item list
        self.items = []

    def add_item(self):
        item_name = self.item_name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()

        if item_name and quantity > 0 and price > 0:
            total_price = quantity * price
            self.items.append({"item_name": item_name, "quantity": quantity, "price": price, "total_price": total_price})
            self.update_item_listbox()
            self.calculate_total()
            self.clear_item_entry_fields()
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid values for item details.")

    def update_item_listbox(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            self.item_listbox.insert(tk.END, f"{item['item_name']} - {item['quantity']} x {item['price']} = {item['total_price']}")

    def calculate_total(self):
        total = sum(item["total_price"] for item in self.items)
        self.total_var.set(total)

    def generate_bill_pdf(self):
        if not self.items:
            messagebox.showinfo("Empty Bill", "No items added to the bill.")
            return

        pdf_filename = f"grocery_bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf = canvas.Canvas(pdf_filename)

        pdf.drawString(30, 780, "Grocery Store Bill")
        pdf.line(30, 745, 550, 745)

        # Customer details
        pdf.drawString(30, 730, f"Customer Name: {self.customer_name_var.get()}")
        pdf.drawString(30, 715, f"Email: {self.customer_email_var.get()}")
        pdf.drawString(30, 700, f"Contact Number: {self.customer_contact_var.get()}")
        pdf.drawString(30, 685, f"Address: {self.customer_address_var.get()}")

        y_position = 660
        for item in self.items:
            pdf.drawString(30, y_position, f"{item['item_name']} - {item['quantity']} x {item['price']} = {item['total_price']}")
            y_position -= 15

        pdf.drawString(30, y_position, f"Total: {self.total_var.get()}")
        pdf.save()

        return pdf_filename

    def generate_bill(self):
        pdf_filename = self.generate_bill_pdf()
        messagebox.showinfo("Bill Generated", f"Bill saved as {pdf_filename}")

    def share_bill(self):
        pdf_filename = self.generate_bill_pdf()

        # Replace the following with your own email configuration
        smtp_server = "smtp.freesmtpservers.com"
        smtp_port = 25
        smtp_username = "testing1ajeet@gmail.com"
        #smtp_password = "16072018"
        recipient_email = self.customer_email_var.get()

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = recipient_email
        msg['Subject'] = "Grocery Store Bill"

        body = f"Hi {self.customer_name_var.get()},\n\nPlease find attached the grocery store bill.\n\nThanks,\nYour Grocery Store"
        msg.attach(MIMEText(body, 'plain'))

        with open(pdf_filename, "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype="pdf")
            attachment.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
            msg.attach(attachment)

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
           # server.starttls()
           # server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_email, msg.as_string())
            server.quit()

            messagebox.showinfo("Bill Shared", "Bill sent successfully via email.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email. Error: {str(e)}")

        # Remove the generated PDF file after sharing
        import os
        os.remove(pdf_filename)

    def clear_item_entry_fields(self):
        self.item_name_var.set("")
        self.quantity_var.set(0)
        self.price_var.set(0.0)

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryBillingApp(root)
    root.mainloop()
