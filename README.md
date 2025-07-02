# 📦 Amazon ASIN Scraper — Streamlit App

Extract detailed product data from Amazon using a list of ASINs — **without writing any code**.  
This tool uses the [Bright Data API](https://brightdata.com) and a friendly Streamlit interface for fast, reliable scraping.

---

## 🚀 Features

- ✅ Upload your Excel file with ASINs
- 🔍 Scrape titles, prices, ratings, images, reviews & categories
- ⚡ Multithreaded scraping (fast performance)
- 🧠 Automatic ASIN validation
- 📄 Download data as a CSV file
- 🔐 Secure Bright Data API integration

---

## 🖥 How to Run Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py
📁 Input Format
Upload a .xlsx Excel file with a column named asin (case-insensitive):

asin
B07FZ8S74R
B08N5WRWNW
B07PGL2ZSL

🔑 Bright Data API Key
You must have a valid Bright Data account and API Key.

Format: 64-character string

Enter it in the app when prompted

👉 Don’t have one? Sign up at Bright Data

📄 Output
The app generates a downloadable CSV file with the following fields:

Name	ASIN	Rating	Price	ProductURL	ImageCount	ReviewCount	Breadcrumbs	BestSellerRank	MakeSureFits

📸 Screenshot

📝 License
MIT License. Use freely and responsibly.

yaml
Copy
Edit

---

Let me know if you'd like help:
- Adding a real screenshot or preview image
- Deploying to Streamlit Cloud
- Or converting this into a Spanish version too








