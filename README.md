# First Part: 📬 Gmail Email Export via Gmail API (Python)

This project connects to your Gmail account using the official Gmail API, extracts metadata from your emails (such as `Date`, `From`, `Subject`), and exports it into a CSV file for further analysis in Power BI, Streamlit, or other tools.

---

## ✅ Features

- Connects securely to your Gmail account via OAuth 2.0
- Fetches up to thousands of emails with pagination
- Extracts metadata (Date, From, Subject)
- Optionally includes deleted/spam/archived emails
- Outputs clean CSV for BI/reporting usage

---

## 🚀 Setup Instructions

### 1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable the **Gmail API**

### 2. Configure OAuth Consent Screen
- Set **User Type**: `External`
- Fill in required info (App name, email, etc.)
- Add your Gmail address to **Test Users**

### 3. Create OAuth Credentials
- Navigate to **APIs & Services > Credentials**
- Click **Create Credentials > OAuth client ID**
- Choose **Desktop App**
- Download the `credentials.json` file

### 4. Install Required Libraries
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```
## 🧠 How This Script Works

- Launches a local server via `flow.run_local_server(port=0)` to complete OAuth login  
- Fetches messages via Gmail API using `service.users().messages().list()` and `service.users().messages().get()`  
- Supports pagination using `nextPageToken`  
- Saves emails to `gmail_data.csv`  

## 📁 Output

## 📤 Gmail Export – CSV Output Overview

The script connects to the Gmail API, fetches up to **2000 emails**, and saves them into a CSV file named `gmail_data.csv`. Each row in the file represents one email message with the following columns:

| Column Name         | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `Date`              | Timestamp of the email in `DD-MM-YYYY HH:MM:SS` format                      |
| `From`              | Sender’s email address                                                      |
| `Subject`           | Subject of the email                                                        |
| `IsSent`            | Whether the email was sent by you (`True`/`False`)                          |
| `Labels`            | All Gmail labels assigned to the email                                      |
| `Category`          | Gmail category (e.g. `CATEGORY_UPDATES`, `CATEGORY_PROMOTIONS`)             |
| `IsImportant`       | Whether Gmail marked it as important                                        |
| `ThreadID`          | Unique ID of the email thread (conversation)                                |
| `ThreadCount`       | Number of messages in the conversation thread                               |
| `HasAttachments`    | Whether the email contains attachments (`True`/`False`)                     |
| `AttachCount`       | Number of attached files                                                    |
| `AttachTypes`       | File types (extensions) of attachments, separated by `;`                    |
| `ToCount`           | Number of recipients in the `To` field                                      |
| `RecipientDomains`  | Email domains of all recipients in `To`, separated by `;`                   |
| `IsReply`           | Whether the subject starts with `Re:`                                       |
| `WordCount`         | Number of words in the email body                                           |
| `UrlCount`          | Number of links (URLs) in the email body                                    |
| `TopWord`           | Most frequent word (excluding common stopwords) in the email body           |

The script shows progress in the terminal during fetching and processing, and ends with a message confirming the export.


## 📊 Use Cases

- Personal inbox analytics  
- Email behavior dashboards (Power BI / Streamlit)  
- Identifying top senders or activity patterns
---
#  📬 Gmail Activity Dashboard

## 📌 What is this about?

This dashboard gives me a clear overview of my Gmail activity over time. I connected directly to my Gmail account using the **official Gmail API via Google Cloud**, and extracted metadata like sender, subject, labels, and timestamps.

I built it mostly out of curiosity – to better understand my email habits, how much time I spend in communication, and whether certain days or weeks are heavier than others.

---

## 📊 What it shows

- Number of emails sent and received by day/week/month  
- Breakdown by labels (e.g., important, work, personal, unread)  
- Top senders and recipients  
- Trends in email activity over time  
- Hour-of-day and day-of-week heatmaps

---

## 🎯 Why I made it

Email takes up a big part of my day, and I wanted to see that visually. Some reasons this dashboard might be useful:

- **Productivity tracking**: spot peaks and patterns in communication  
- **Personal insight**: understand who I interact with the most  
- **Portfolio project**: shows how I work with APIs, Google Cloud, and Power BI  
- Could be expanded for **team inbox monitoring** or **support ticket tracking**

---

> 🔐 The data shown here is real but anonymized for privacy.  
> 🛠️ The connection to Gmail was built using a custom Python script and Google Cloud credentials.

---

Let me know if you'd like to see the script or how the connection works – happy to share more.

  
