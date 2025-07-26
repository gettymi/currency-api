# 💱 Currency Exchange API

A simple Django-based REST API for fetching currency rates, converting currencies, and listing available currencies using the [Open Exchange Rates API](https://openexchangerates.org/).

---

## 🔧 Features

- Convert between two currencies
- Fetch latest exchange rates
- List all available currency codes
- Caching for performance
- Logging for traceability
- Error handling for API failures and bad input

---

## 🧪 Tech Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- Open Exchange Rates API
- Memcached/LocMem cache
- Logging with Python's standard library

## 🚀 Setup

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/currency-api.git
cd currency-api
pip install -r requirements.txt

Add your .env file
OXR_APP_ID=your_openexchangerates_app_id
OXR_BASE_URL=https://openexchangerates.org/api

Run server
python manage.py runserver


🔍 API Endpoints
Method	Endpoint	Description
GET	/api/convert/	Convert amount from one currency to another
GET	/api/latest/	Get latest exchange rates
GET	/api/currencies/	List all currency codes


Example:
GET /api/convert/?from=USD&to=EUR&amount=100


✅ Run Tests
python manage.py test




📚 License
MIT – feel free to fork and build on it!

Made with 💻 and ☕️ by Bohdan Tereshchenko