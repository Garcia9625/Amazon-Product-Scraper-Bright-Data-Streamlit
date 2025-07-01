import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

st.title("Amazon Products Scraper by ASIN")

uploaded_file = st.file_uploader("Upload Excel file with ASINs", type=["xlsx"])
api_key = st.text_input("Enter Bright Data API Key", type="password")

if uploaded_file and api_key:
    try:
        input_df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
        st.stop()

    if "asin" not in input_df.columns.str.lower():
        st.error("❌ Excel file must contain a column named 'asin'")
        st.stop()

    asin_column = input_df.loc[:, input_df.columns.str.lower() == "asin"].squeeze()
    asins_raw = asin_column.dropna().astype(str).unique().tolist()

    valid_asins = []
    for asin in asins_raw:
        asin = asin.strip().upper()
        if re.fullmatch(r"[A-Z0-9]{10}", asin):
            valid_asins.append(asin)

    st.write(f"Loaded {len(valid_asins)} valid ASINs")

    request_count = 0
    start_time = time.time()

    def fetch_html(target_url):
        global request_count
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "zone": "web_unlocker1",
            "url": target_url,
            "format": "raw"
        }
        try:
            res = requests.post("https://api.brightdata.com/request", json=data, headers=headers, timeout=30)
            request_count += 1
            if res.status_code == 200:
                return res.text
        except Exception as e:
            st.warning(f"Request error for {target_url}: {e}")
        return None

    def extract_product(asin):
        url = f"https://www.amazon.com/dp/{asin}"
        html = fetch_html(url)
        if not html:
            return ["", asin, "No rating yet", "", url, 0, "No reviews yet", "", "", "Not found"]

        soup = BeautifulSoup(html, "html.parser")
        name = soup.select_one("span#productTitle")
        name = name.text.strip() if name else ""

        rating = "No rating yet"
        el = soup.select_one("span[data-hook='rating-out-of-text']")
        if el:
            rating = el.text.strip()

        price = ""
        price_el = soup.select_one("div.a-section.a-spacing-none.aok-align-center.aok-relative span.aok-offscreen")
        if price_el:
            price = price_el.text.strip()

        image_urls = set()
        for img in soup.select("#altImages img"):
            url = img.get("src") or img.get("data-src") or img.get("data-image-src")
            if url:
                image_urls.add(url)
        main_img = soup.select_one("#landingImage")
        if main_img:
            url = main_img.get("src") or main_img.get("data-old-hires")
            if url:
                image_urls.add(url)

        review_count = "No reviews yet"
        review_el = soup.select_one("span[data-hook='total-review-count']")
        if review_el:
            review_count = review_el.text.strip().split()[0].replace(",", "")

        breadcrumbs = " > ".join([a.text.strip() for a in soup.select("#wayfinding-breadcrumbs_feature_div ul.a-unordered-list li a")])

        bsr = ""
        for section in ["#productDetails_detailBullets_sections1 tr", "#detailBulletsWrapper_feature_div"]:
            block = soup.select(section)
            for tag in block:
                if "Best Sellers Rank" in tag.text:
                    match = re.search(r"#([\d,]+)", tag.get_text())
                    if match:
                        bsr = match.group(1)
                        break
            if bsr:
                break

        make_sure_fits = "No"
        if soup.select_one("#automotive-pf-primary-view-default-make-sure-this-fits"):
            make_sure_fits = "Yes"

        return [name, asin, rating, price, url, len(image_urls), review_count, breadcrumbs, bsr, make_sure_fits]

    progress = st.progress(0)
    status = st.empty()

    with st.spinner("Scraping products..."):
        data_rows = []
        total = len(valid_asins)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(extract_product, asin) for asin in valid_asins]
            for i, f in enumerate(as_completed(futures), 1):
                data_rows.append(f.result())
                progress.progress(i / total)
                status.write(f"Scraped {i}/{total} products")

        output_df = pd.DataFrame(data_rows, columns=[
            "Name", "ASIN", "Rating", "Price", "ProductURL",
            "ImageCount", "ReviewCount", "Breadcrumbs", "BestSellerRank", "MakeSureFits"])

        total_time = time.time() - start_time
        minutes = total_time / 60
        st.success(f"✅ Done! Scraped {len(output_df)} products using {request_count} requests in {minutes:.2f} minutes ({total_time:.1f} seconds).")
        st.dataframe(output_df)

        csv_data = output_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv_data, file_name="products_scraped.csv", mime="text/csv")

        # Reset uploader
        uploaded_file = None
