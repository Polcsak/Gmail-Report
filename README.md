# 📬 Gmail Email Export via Gmail API (Python)

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
## 🧠 How It Works

- Launches a local server via `flow.run_local_server(port=0)` to complete OAuth login  
- Fetches messages via Gmail API using `service.users().messages().list()` and `service.users().messages().get()`  
- Supports pagination using `nextPageToken`  
- Saves emails to `gmail_data.csv`  

## 📁 Output

The script generates a file named `gmail_data.csv` with the following columns:

- `Date`  
- `From`  
- `Subject`  

## 📊 Use Cases

- Personal inbox analytics  
- Email behavior dashboards (Power BI / Streamlit)  
- Identifying top senders or activity patterns  
