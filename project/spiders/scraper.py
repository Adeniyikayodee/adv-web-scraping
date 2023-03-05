import scrapy
import logging
logger = logging.getLogger('my_logger')

class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    start_urls = ['https://www.elcorteingles.es/']

    def parse(self, response):
        '''This function is scraping categories which are available on main page and passing the URLs to parse_product_links function'''
        
        
        logger.info('Parse Function called on %s to scrap category', response.url)
        links =[response.urljoin(link) for link in response.css("div.megadropList-wrp>li:nth-child(7) a::attr(href)").getall()]
        print("Category link",links[1])
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_product_links)
    def parse_product_links(self,response):
        '''Inside this funciton product links are being scrapped'''
        links = [response.urljoin(link) for link in response.css("a.product_link::attr(href)").getall()]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
            
        next_page = response.css("a._pagination_link::attr(href)").get()
        
        if next_page:
            yield response.follow(response.urljoin(next_page),callback=self.parse_product_links)
    def parse_product(self,response):
        '''Finally product details are being scrapped from their main page'''
        data_dict ={}
        images = [response.urljoin(img) for img in response.css("div.image-layout-slides-secondary img::attr(data-src)").getall()]
        if len(images)<1:
            images =response.css(".layout-img-unique::attr(data-src)").get()
        
        data_dict['Brand']=response.css(".product_detail-brand::text").get()
        data_dict['Product Title']= response.css(".product_detail-title::text").get()
        data_dict['SKU/Model']= response.css(".sku-model::text").get()
        data_dict['Product link']= response.url
        data_dict['Description']= response.css(".product_detail-description-in-image ::text").get()
        data_dict['Image']= images
        yield data_dict