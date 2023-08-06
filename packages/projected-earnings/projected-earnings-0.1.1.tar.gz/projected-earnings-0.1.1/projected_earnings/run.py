import imghdr
import os
import smtplib
from datetime import date
from email.message import EmailMessage
from pathlib import Path
from pprint import pprint

import gspread
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from oauth2client.service_account import ServiceAccountCredentials

# -This is for gmail set up ----------------#

# EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
# EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")


cwd = Path(os.getcwd())
image_file_location = f"{cwd}\\Pictures\\ChrisProjectoin{date.today()}.jpg".replace("\\","/")
#image_file_location = "C:/Users/dicha/OneDrive/Documents/Code/Chris Email/Projected-Earnings/test.jpg"

EMAIL_ADDRESS = "ChambersAutomation@gmail.com"
EMAIL_PASSWORD = "Automation1!"
msg = EmailMessage()

# ------------------------------------------#


def send_email(final_amount):
    msg["Subject"] = "Portfolio Projection Daily Update"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "dichambers95@gmail.com"
    # msg["To"] = "dichambers95@gmail.com", "ChambersAutomation@gmail.com"
    msg.set_content(
        f"Good Morning Chris, \n\nI hope you are well.\n\nPlease find attached a graph with your current projection of portfolio value by the end of the year. You are currently on track to finish the year with £{final_amount} in your account. In order to keep this projection accurate be sure to update your daily performance on our shared document, you can update the document here: https://docs.google.com/spreadsheets/d/1GuMo4rbOYgJQE4huJbJgAFf-PM7lIr3tlgemPXQUKAY/edit#gid=0. Any questions please get in touch.\n\nKind regards,\n\nNotorious DIC"
    )

    with open(image_file_location, "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f"Daily Graph {date.today()} "

    msg.add_attachment(
        file_data, maintype="image", subtype=file_type, filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)


today = date.today()

# This is for google sheets set up -------------------#
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
GraphDays = 365
font = {"family": "normal", "weight": "bold", "size": 30}
# ----------------------------------------------------#


def makegraph(df):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.scatter(df["Days"], df["Potential Earnings"], color="cyan")
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    ax.spines["bottom"].set_color("cyan")
    ax.spines["left"].set_color("cyan")
    ax.yaxis.label.set_color("cyan")
    ax.xaxis.label.set_color("cyan")
    ax.title.set_color("cyan")
    ax.tick_params(axis="x", colors="cyan", labelsize=16)
    ax.tick_params(axis="y", colors="cyan", labelsize=16)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("£{x:,.0f}"))
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.title.set_size(30)

    plt.xlabel("Number of Days", labelpad=15)
    plt.ylabel("Value of Portfolio Projection (£)", labelpad=15)

    ax.set_title("Chris Projected Portfolio Value", fontsize=26)
    print(image_file_location)
    plt.savefig(image_file_location)


def collect_data_from_sheets():
    sheet = client.open("Trading Data").sheet1
    # data = sheet.get_all_records()
    df = pd.DataFrame(sheet.get_all_records(empty2zero=True))
    df = df.head(GraphDays)
    df["Potential Earnings"] = df["Potential Earnings"].str.replace(",", "")
    df["Potential Earnings"] = df["Potential Earnings"].str.replace("£", "")
    df["Potential Earnings"] = df["Potential Earnings"].astype("float")
    # print(df["Potential Earnings"])

    Final_amount = df["Potential Earnings"].iloc[-1]
    Final_amount = "{:,.2f}".format(Final_amount)
    return df, Final_amount


def main():
    df, final_amount = collect_data_from_sheets()
    makegraph(df)
    send_email(final_amount)
    print("Email Sent")


if __name__ == "__main__":
    main()
