from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv
import re
import base64
import os
from collections import Counter
from email.utils import parsedate_to_datetime

# -----------------------------
# Configuration
# -----------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
MAX_EMAILS = 2000
CSV_FILE = 'gmail_data.csv'
STOPWORDS = {'the','and','for','you','with','this','from','that','have','will','not','are','was','but','your','https','http'}

# -----------------------------
# Authentication and Gmail service
# -----------------------------
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('gmail', 'v1', credentials=creds)

# -----------------------------
# Helper functions
# -----------------------------
def get_email_body(payload):
    """Extracts the text from the payload, preferring text/plain."""
    data = payload.get('body', {}).get('data')
    if data:
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    for part in payload.get('parts', []):
        if part.get('mimeType') == 'text/plain':
            return get_email_body(part)
    for part in payload.get('parts', []):
        text = get_email_body(part)
        if text:
            return text
    return ''


def clean_and_analyze(text):
    """Cleans HTML, counts words, URLs, and finds top word."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[^;\s]+;', ' ', text)
    text = text.lower()
    words = re.findall(r"\b[a-z0-9]{3,}\b", text)
    sig = [w for w in words if w not in STOPWORDS]
    word_count = len(words)
    url_count = len(re.findall(r'https?://', text))
    top_word = Counter(sig).most_common(1)[0][0] if sig else ''
    return word_count, url_count, top_word


def extract_headers(headers, name):
    """Extracts header value by name."""
    for h in headers:
        if h.get('name') == name:
            return h.get('value', '')
    return ''


def get_label_info(msg):
    labels = msg.get('labelIds', [])
    category = next((l for l in labels if l.startswith('CATEGORY_')), '')
    return labels, category, 'IMPORTANT' in labels, 'SENT' in labels


def get_thread_count(thread_id):
    if not thread_id:
        return 0
    thread = service.users().threads().get(userId='me', id=thread_id).execute()
    return len(thread.get('messages', []))


def get_attachments_info(parts):
    files = [p['filename'] for p in parts if p.get('filename')]
    count = len(files)
    types = [os.path.splitext(f)[1].lower() or 'unknown' for f in files]
    return count>0, count, ';'.join(types)


def parse_recipients(header):
    addrs = [a.strip() for a in re.split(r'[;,]', header) if a.strip()]
    domains = sorted({re.search(r'@([^>\s]+)', a).group(1) for a in addrs if re.search(r'@([^>\s]+)', a)})
    return len(addrs), ';'.join(domains)

# -----------------------------
# Load all message IDs
# -----------------------------
print("⏬ Loading message IDs...")
msgs = []
token = None
while len(msgs) < MAX_EMAILS:
    res = service.users().messages().list(userId='me', maxResults=100, pageToken=token).execute()
    batch = res.get('messages', [])
    msgs += batch
    print(f"  Loaded IDs: {len(msgs)}")
    token = res.get('nextPageToken')
    if not token:
        break
print(f"✅ Total IDs: {len(msgs)}")

# -----------------------------
# Process and export to CSV
# -----------------------------
print(f"⏬ Processing {len(msgs)} emails...")
with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Date','From','Subject','IsSent','Labels','Category','IsImportant',
        'ThreadID','ThreadCount','HasAttachments','AttachCount',
        'AttachTypes','ToCount','RecipientDomains','IsReply',
        'WordCount','UrlCount','TopWord'
    ])

    for i, m in enumerate(msgs, 1):
        mdata = service.users().messages().get(userId='me', id=m['id']).execute()
        headers = mdata['payload'].get('headers', [])

        # Extract and format the date
        raw_date = extract_headers(headers, 'Date')
        try:
            dt = parsedate_to_datetime(raw_date)
            formatted_date = dt.strftime('%d-%m-%Y %H:%M:%S')
        except Exception:
            formatted_date = raw_date

        # Other headers
        frm = extract_headers(headers, 'From')
        subj = extract_headers(headers, 'Subject')
        to_h = extract_headers(headers, 'To')

        labels, cat, important, sent = get_label_info(mdata)
        tid = mdata.get('threadId', '')
        th_count = get_thread_count(tid)
        parts = mdata['payload'].get('parts', [])
        has_att, att_cnt, att_types = get_attachments_info(parts)
        to_cnt, to_dom = parse_recipients(to_h)
        is_reply = subj.lower().startswith('re:')
        body = get_email_body(mdata['payload'])
        wc, uc, tw = clean_and_analyze(body)

        writer.writerow([
            formatted_date, frm, subj, sent, ';'.join(labels), cat, important,
            tid, th_count, has_att, att_cnt,
            att_types, to_cnt, to_dom, is_reply,
            wc, uc, tw
        ])
        if i % 100 == 0 or i == len(msgs):
            print(f"  Processed {i}/{len(msgs)}")

print(f"✅ CSV saved as '{CSV_FILE}' – done!")
