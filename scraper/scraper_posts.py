import scrapy
from htmllaundry import sanitize

class PostsSpider(scrapy.Spider):
    name = "afini_post"
    
    def extract_post_(self, response):
        return ""

    def start_requests(self):
        urls = [f"https://contentmanager.afinidata.com/posts/{pid}/" for pid in range(450)]
        #urls = ["https://contentmanager.afinidata.com/posts/325/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_frame)

    def extract_frame(self, response):
        route = response.xpath('/html/body/article/div/iframe').attrib.get("src")
        print(route)
        if "campaign" in route:
            yield scrapy.Request(url=route, callback=self.parse)

    def parse(self, response):
        b = response.css('.templateContainer')
        page = response.url.split("/")[-1]
        filename = 'scraper/posto-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(sanitize(b.get()).encode())
        self.log('Saved file %s' % filename)    


