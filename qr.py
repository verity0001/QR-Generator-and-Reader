import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import time
import os
from time import gmtime, strftime
import requests
import glob
import cv2
import pandas as pd
import pathlib

filename = "qr_code.png"

class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")
        self.master.geometry("400x500")
        self.master.resizable(True, True)

        # load the icon file
        try:
            icon = tk.PhotoImage(file="amogus.ico")
            self.master.iconphoto(True, icon)
        except:
            print("Icon Not Found")

        # create a label for the input entry
        self.input_label = tk.Label(text="Enter text to generate QR code:")
        self.input_label.grid(row=0, column=0, pady=10)

        # create an entry widget for the input
        self.input_entry = tk.Entry(width=20)
        self.input_entry.grid(row=1, column=0)

        # create a label for the input entry
        self.file_label = tk.Label(text="Enter QR code file name:")
        self.file_label.grid(row=0, column=1, pady=10)

        # create an entry widget for the input
        self.file_entry = tk.Entry(width=20)
        self.file_entry.grid(row=1, column=1)

        # create an entry widget for the filename
        self.filename_entry = tk.Entry(width=20)
        self.filename_entry.grid(row=1, column=1)
        self.filename_entry.insert(0, f"{filename}")

        # create a label for the generator speed
        self.speed_label = tk.Label(text="Select QR Code generator speed:")
        self.speed_label.grid(row=2, column=0, pady=10)

        # create a variable to hold the selected generator speed
        self.speed = tk.StringVar()

        # create radio buttons for generator speed
        self.fast_button = tk.Radiobutton(text="Fast", variable=self.speed, value="fast")
        self.fast_button.grid(row=3, column=0)

        self.slow_button = tk.Radiobutton(text="Slow", variable=self.speed, value="slow")
        self.slow_button.grid(row=3, column=1)

        # select the fast generator speed by default
        self.speed.set("fast")

        # create a button to generate the QR code
        self.generate_button = tk.Button(text="Generate", command=self.generate_qr_code, cursor="plus")
        self.generate_button.grid(row=4, column=0, pady=10)

        self.read_button = tk.Button(text="Read QR Code", command=self.readed_qr_code, cursor="plus")
        self.read_button.grid(row=4, column=1, pady=10)

        # create a label for the QR code image
        self.image_label = tk.Label()
        self.image_label.grid(row=5, column=0, columnspan=2)

    def generate_qr_code(self):
        # get the data to encode from the input entry widget
        data = self.input_entry.get()

        # create a QR code instance
        if self.speed.get() == "fast":
            qr = qrcode.QRCode(version=None, box_size=10, border=5)
        else:
            qr = qrcode.QRCode(version=None, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_Q)

        # add data to the QR code
        print(f"Preparing to convert the prompt: '{data}'")
        qr.add_data(data)

        # calculate the minimum required version
        qr.make(fit=True)
        version = qr.version or 1

        # update the QR code with the correct version
        qr = qrcode.QRCode(version=version, box_size=10, border=5)
        qr.add_data(data)
        qr.make()

        # generate an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # save the image
        img.save(f"{filename}")

        # create a PhotoImage object from the image file
        if self.speed.get() == "fast":
            img_file = Image.open(f"{filename}")
            photo = ImageTk.PhotoImage(img_file)
            print(f"'{data}' Has been converted to a QR code (mode - fast)\n")
        else:
            time.sleep(0.5)
            img_file = Image.open(f"{filename}")
            photo = ImageTk.PhotoImage(img_file)
            print(f"'{data}' Has been converted to a QR code (mode - slow)\n")

        # set the image of the image label to the PhotoImage
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # show a message box with the file path of the saved image
        if self.speed.get() == "fast":
            pass
        else:
            messagebox.showinfo("QR Code Successfully Generated", f"The QR code has been saved as '{filename}' in the current directory.")
            time.sleep(1)

    def read_qr_code(self, filename):
        try:
            img = cv2.imread(filename)
            detect = cv2.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(img)
            return value
        except TypeError:
            img = cv2.imread("qr_code.png")
            detect = cv2.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(img)
            return value
        except:
            return

    def readed_qr_code(self):
        image = self.filename_entry.get()
        value = self.read_qr_code(image)

        print(f"The value of the qr code given was: '{value}'")

root = tk.Tk()
app = QRCodeGeneratorApp(root)
root.mainloop()