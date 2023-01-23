# AGidas-API
Api for AGidasScraper

1. Edit file "url" to any AutoGidas url that has cars list
2. Launch uvicorn main:app --reload in console
3. Visit http://127.0.0.1:8000/cars/[cars amount that you want to scrape] for example - http://127.0.0.1:8000/cars/5
4. Get titles for each car with /{title}
5. Get 10 most recent requests with /recent_requests
