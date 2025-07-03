# 🧠 Who Said That? – Quote Guessing Game

An interactive Streamlit web app where users guess the author of a famous quote. Quotes are scraped from [quotes.toscrape.com](http://quotes.toscrape.com), and the game includes three difficulty levels, real-time hints, author bios, and quote tracking.

---

## 🔧 Features

- Scrapes quotes, author bios, birth info, and tags.
- Loads 50 quotes at a time to minimise scraping load.
- Automatically refreshes to the next 50 after 50 rounds.
- Three difficulty levels:
  - **Easy**: Author bio shown (name redacted); accepts first or last name
  - **Medium**: Two guesses; second try reveals the full last name
  - **Hard**: Four guesses with progressive hints (birthplace, initials)
- Tracks score and quote count
- Modular structure with separate logic files for each difficulty
- Author bio is hidden behind a clickable “More Details >>” link

---

## 📁 Project Structure


```

Quote-Guessing/
├── app.py                 # Main Streamlit app
├── scraper.py             # Web scraping and caching logic
├── easy.py                # Easy mode logic
├── medium.py              # Medium mode logic
├── hard.py                # Hard mode logic
├── quotes_cache.json      # Cached quote data (auto-generated)
├── requirements.txt       # Dependencies
└── README.md              # Project documentation

````

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Launch the app

```bash
streamlit run app.py
```

---

## Game Logic Overview

* Quotes are loaded in batches of 50
* When all 50 are played, the app loads the next unseen 50
* User guesses based on difficulty:

  * Easy: author bio without name; accepts partial name
  * Medium: 2 tries, final hint shows last name
  * Hard: 4 tries, multiple hints

---

## 📝 Acknowledgement

This project is adapted from a public tutorial on [GeeksforGeeks](https://www.geeksforgeeks.org/python/quote-guessing-game-using-web-scraping-in-python/) and expanded with additional logic, user interface, and features using Streamlit.

Quotes sourced from [quotes.toscrape.com](http://quotes.toscrape.com)
