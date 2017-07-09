from base64 import b64encode, b64decode
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from hashlib import sha256
from smtplib import SMTP
from urllib.parse import urljoin
from urllib.request import urlopen

def summarize_site(index_url):
    '''
    Return a dict that maps the URL to the SHA-256 sum of its page contents
    for each link in the index_url.
    '''
    summary = {}
    with urlopen(index_url) as index_req:
        soup = BeautifulSoup(index_req.read())
        links = [urljoin(index_url, a.attrs.get('href'))
                 for a in soup.select('li.topLevel a[href^=/site/csc110winter2015/]')]
        for page in links:
            # Ignore the sitemap page
            if page == '/site/csc110winter2015/system/app/pages/sitemap/hierarchy':
                continue
            with urlopen(page) as page_req:
                fingerprint = sha256()
                soup = BeautifulSoup(page_req.read())
                for div in soup.find_all('div', class_='sites-attachments-row'):
                    fingerprint.update(div.encode())
                summary[page] = fingerprint.digest()
    return summary

def save_site_summary(filename, summary):
    with open(filename, 'wt', encoding='utf-8') as f:
        for path, fingerprint in summary.items():
            f.write("{} {}\n".format(b64encode(fingerprint).decode(), path))

def load_site_summary(filename):
    summary = {}
    with open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            fingerprint, path = line.rstrip().split(' ', 1)
            summary[path] = b64decode(fingerprint)
    return summary

def diff(old, new):
    return {
        'added': new.keys() - old.keys(),
        'removed': old.keys() - new.keys(),
        'modified': [page for page in set(new.keys()).intersection(old.keys())
                     if old[page] != new[page]],
    }

def describe_diff(diff):
    desc = []
    for change in ('added', 'removed', 'modified'):
        if not diff[change]:
            continue
        desc.append('The following page(s) have been {}:\n{}'.format(
            change,
            '\n'.join(' ' + path for path in sorted(diff[change]))
        ))
    return '\n\n'.join(desc)

def send_mail(body):
    ## Compose the email
    fromaddr = 'jasontwright@gmail.com'
    toaddr = 'jasontwright@gmail.com'
    msg = MIMEText(body, 'plain')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Incoming CSC110 website changes!"

    ## Send it
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('jasontwright@gmail.com', 'tvkqpawddzdpvpej')
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

def main(index_url, filename):
    summary = summarize_site(index_url)
    try:
        prev_summary = load_site_summary(filename)
        if prev_summary:
            diff_description = describe_diff(diff(prev_summary, summary))
            if diff_description:
                print(diff_description)
                send_mail(diff_description)
    except FileNotFoundError:
        pass
    save_site_summary(filename, summary)

main(index_url='https://sites.google.com/site/csc110winter2015/home',
     filename='site.txt')
