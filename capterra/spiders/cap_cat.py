# -*- coding: utf-8 -*-
from scrapy import Spider
import scrapy
from ..items import CapterraItem
import re
import json
from datetime import date

# zL4cXzeFxV
class CapCatSpider(scrapy.Spider):
    name = 'cap_cat'
    allowed_domains = ['www.capterra.com']
    start_urls = ['https://www.capterra.com/categories']

    def parse(self, response):
        div = response.xpath("//a")
        for x in range(8, 781):
            items = CapterraItem()
            category = response.xpath(".//a/text()")[x].get()
            slug = response.xpath(".//a/@href")[x].get()
            slug = slug.strip('/')
            slug = re.sub(r'[/ ]+', ' ', slug).strip()
            api_url = "https://www.capterra.com/directoryPage/rest/v1/category?htmlName=" + slug + "&countryCode=IN"
            items['category'] = category
            # items['slug'] = slug
            # items['api_url'] = api_url
            yield scrapy.Request(api_url, meta={'item': items}, callback=self.api)

    def api(self, response):
        items = response.meta['item']
        data = json.loads(response.body)
        products = data.get('pageData').get('categoryData').get('products')
        for product in products:
            # product_name = product.get('product_name')
            # rating = product.get('rating')
            # description = product.get('long_desc')
            product_id = product.get('product_id')
            product_slug = product.get('product_slug')
            product_url = 'https://www.capterra.com/p/' + str(product_id) + "/" + product_slug + "/"
            # yield {'product': product_name, 'product_url': product_url}
            yield scrapy.Request(product_url, meta={'item': items}, callback=self.details)

    def details(self, response):
        items = response.meta['item']
        site_id = "1"
        title = response.xpath("//h1/text()").get()
        rating = response.xpath("//*[@class='StarRating__Rating-sc-9jwzgg-1 cAGyvf']/text()").get().split('/')[0]
        review = response.xpath("//*[@class='ReviewSection__Root-sc-189472c-0 icjcMH']/text()").get()
        image = response.xpath("//*[@class='Thumbnail__Image-sc-1xvq2zk-0 idhssu']/@src").get()
        features = response.xpath("//*[@class='CheckIndicator__Children-sc-445q3w-1 bePeQr']/text()").get()
        try:
            price = response.xpath("//*[@class='SpecRow__RowItem-sc-2l3qlv-4 gPGpNd']/span/text()").get().split('/')[0].split('$')[1]
        except:

            price = response.xpath("//*[@class='SpecRow__RowItem-sc-2l3qlv-4 gPGpNd']/span/text()").get()
            print("alteredaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        description = response.xpath("//*[@class='Section__Body-w4hkcm-1 jhCJZs']/text()").get()
        created_date = str(date.today())
        items['site_id'] = site_id
        items['title'] = title
        items['rating'] = rating
        items['image'] = image
        items['review'] = review
        items['feature'] = features
        items['price'] = price
        items['description'] = description
        items['created_date'] = created_date
        yield items
