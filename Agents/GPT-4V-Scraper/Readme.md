# GPT4V-Web-Scraper

## Usage
The `vision_scraper.py` is the execution file

- `visionCrawl` function contains two arguments - Webpage link and prompt

```python
def visionCrawl(url, prompt):
    b64_image = url2screenshot(url)

    print("Image captured")
    
    if b64_image == "Failed to scrape the website":
        return "I was unable to crawl that site. Please pick a different one."
    else:
        return visionExtract(b64_image, prompt)

response = visionCrawl("https://www.myntra.com/reviews/3009070", "Summarize the reviews")
```