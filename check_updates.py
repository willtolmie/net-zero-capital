import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_company_names():
    with open("company_names.txt", 'r') as file:
        company_names = [line.strip() for line in file]
    return company_names

def fetch_news(company, keywords='net zero commitment'):
    search_query = 'https://news.google.com/search?q="'
    for word in company.split():
        if word == "&":
            word = "%26"
        search_query = search_query + word + "%20"
    search_query = search_query[:-3] + '"%20'
    for word in keywords.split():
        search_query = search_query + word + "%20"
    days = 7
    url = search_query + "when%3A" + str(days) + "d&hl=en-US&gl=US&ceid=US%3Aen"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
         for keyword in company.split():
            if keyword.lower() in link['href'].lower():
                if link['href'].startswith("./read/"):
                    return True, url
    return False, url

def generate_message():
    print("The following companies have recent news related to their net zero commitment:")
    body = "<p>The following companies have recent news related to their net zero commitment:<p>"
    noNews = True
    get_company_names()
    for company in get_company_names():
        news, link = fetch_news(company)
        if news:
            noNews = False
            print(company)
            body = body + "<p><a href='" + link + "'>" + company + '</a><p>'
    if noNews:
        body = "<p>None of the companies we are tracking have recent news related to their net zero commitment.<p>"
    print("Message generated!")
    return body 

def send_email():
    # email credentials
    sender_email = "will@nzcapitalgroup.com"
    receiver_email = "will@nzcapitalgroup.com"
    password = "htve qlbf emjo ehhl"

    # email content
    subject = "Recent News Regarding Net Zero Commitments"

    # create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    html_content = """
    <html>
    <body>
    """ + generate_message() + """
    </body>
    </html>
    """

    # attach the body with the msg instance
    msg.attach(MIMEText(html_content, "html"))

    # Create a secure SSL context and send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")