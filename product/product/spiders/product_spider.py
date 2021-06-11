from product.items import ProductItem
from scrapy import Spider, Request
import re

class ProductSpider(Spider):
	name = 'product_spider'
	allowed_urls = ['https://wwww.https://www.macys.com']
	start_urls = ['https://www.macys.com/shop/shoes/all-womens-shoes?id=56233']

	def parse(self, response):
#		num_pages = 157
#		result_urls = [f'https://www.macys.com/shop/shoes/all-womens-shoes/Pageindex/{i+1}?id=56233' for i in range(num_pages) ]
		
#		for url in result_urls:
#			yield Request(url=url, callback=self.parse_results_page)

		for shoe_type, num_pages in [('Pumps', 11), ('Booties', 16), (r'Boat%20Shoes', 1), ('Boots', 22), 
		('Clogs', 2), ('Flats', 21), ('Mules', 5), ('Sandals', 59), ('Slippers', 8), ('Sneakers', 26), 
		('Waterproof', 3), ('Wedges', 13)]:

			result_urls = [f'https://www.macys.com/shop/shoes/all-womens-shoes/Shoe_type,Pageindex/{shoe_type},{i+1}?id=56233' for i in range(num_pages)]

			for url in result_urls:

				yield Request(url=url, callback=self.parse_results_page, meta={'shoe_type':shoe_type})


	def parse_results_page(self, response):

		shoe_type = response.meta['shoe_type']
		rows = response.xpath('//li[@class="cell productThumbnailItem"]')

		for row in rows:

			brand = row.xpath('.//div[@class="productBrand"]/text()').extract_first().strip()
			description = row.xpath('.//a[@class="productDescLink"]/@title').extract_first()
			price = float('.'.join(re.findall(r'\d+', row.xpath('.//div[@class="prices"]/div[1]').extract_first())[0:2]))
			
			try:
				num_review = int(re.findall(r'\d+', row.xpath('.//span[@class="aggregateCount"]/text()').extract_first())[0])
			except:
				num_review = 0

			try:
				rating = float('.'.join(re.findall(r'\d+', row.xpath('.//span[@class="black-star"]').get())))
			except:
				rating = 0.0

			try:
				sale_price = float('.'.join(re.findall(r'\d+', row.xpath('.//span[@class="discount"]').get())))
			except:
				sale_price = price	

			item = ProductItem()
			item['brand'] = brand
			item['description'] = description
			item['price'] = price
			item['num_review'] = num_review
			item['rating'] = rating
			item['sale_price'] = sale_price
			item['shoe_type'] = shoe_type.replace(r'%20', ' ')


			yield item