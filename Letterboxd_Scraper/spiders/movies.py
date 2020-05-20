# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Letterboxd_Scraper.items import LetterboxdScraperItem
import logging


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['letterboxd.com']
    start_urls = ['https://letterboxd.com/films/']

    def __init__(self, genre=None):
        self.genre = genre

    def parse(self, response):
        if self.genre:
            genre_url = response.xpath('//ul[@class="smenu-menu browse-nav-smenu"]/li/a[contains(text(), "'+ self.genre +'")]/@href').extract_first()
            abs_genre_url = response.urljoin(genre_url)

            self.log('---------------------------- \n Scraping '+ str(self.genre) +' Movies \n ---------------------------- ',
                     level=logging.DEBUG)

            yield Request(abs_genre_url,
                          callback=self.parse_page)
        else:
            self.log('---------------------------- \n Please select a Genre to Scrape When Using Crawl Command \n ---------------------------- ',
                     level=logging.WARNING)
        #next page:
        next_page_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page_url:
            abs_page_url = 'https://' + self.allowed_domains[0] + next_page_url
            self.log('---------------------------- \n Going to Next Page \n ---------------------------- ',
                     level=logging.DEBUG)
            yield Request(abs_page_url,
                          callback=self.parse)

    def parse_page(self, response):
        #This method extracts link to actual database for the genre_url
        data_url = response.xpath('//div[@id="content"]/div[@class="content-wrap"]/section/div[@id="films-browser-list-container"]/@data-url').extract_first()
        abs_data_url = 'https://' + self.allowed_domains[0] + data_url
        if abs_data_url:
            self.log('---------------------------- \n Successfully Redirected to Genre Data Page \n ---------------------------- ',
                     level=logging.DEBUG)
            yield Request(abs_data_url,
                          callback=self.parse_genre_data)
        else:
            self.log('----------------------------\n \ Not Redirected to Genre Data Page \n ---------------------------- ',
                     level=logging.WARNING)



    def parse_genre_data(self, response):
        #Collects list of movies on the page to request specific movies, then goes to next page
        movies = response.xpath('//li/div/a/@href').extract()
        for movie in movies:
            movie_url = 'https://' + self.allowed_domains[0] + movie
            movie_path = movie.split('/')[2]
            yield Request(movie_url,
                          callback=self.parse_movie,
                          meta={'Movie': movie_path})

        #next page:
        next_page_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page_url:
            abs_page_url = 'https://' + self.allowed_domains[0] + next_page_url
            self.log('---------------------------- \n Going to Next Page \n ---------------------------- ',
                     level=logging.DEBUG)
            yield Request(abs_page_url,
                          callback=self.parse_page)

    def parse_movie(self, response):
        #Scrapes movie general info from movie page
        movie_path = response.meta['Movie']
        data = LetterboxdScraperItem()

        title = response.xpath('//h1[@class="headline-1 js-widont prettify"]/text()').extract_first()
        year = response.xpath('//p/small/a/text()').extract_first()
        director = response.xpath('//*[@class="text-sluglist"]/p/a[contains(@href,"director")]/text()').extract()
        length = int(response.xpath('//p[@class="text-link text-footer"]/text()').extract_first().strip().split('\xa0')[0])

        data['title'] = title
        data['year'] = year
        data['director'] = director
        data['running_time'] = length

        stats_url = 'https://letterboxd.com/esi/film/' + movie_path +'/stats/'

        #Going to the stats page to scrape data
        yield Request(stats_url,
                      callback=self.parse_stats,
                      meta={'Movie': movie_path, 'Data': data})

    def parse_stats(self, response):
        movie_path = response.meta['Movie']
        data = response.meta['Data']

        views = int(response.xpath('//li[@class="stat filmstat-watches"]/a/@title').extract_first().split()[2].replace(',',''))
        likes = int(response.xpath('//li[@class="stat filmstat-likes"]/a/@title').extract_first().split()[2].replace(',',''))

        data['views'] = views
        data['likes'] = likes

        ratings_url = 'https://letterboxd.com/csi/film/' + movie_path + '/rating-histogram/'

        yield Request(ratings_url,
                      callback=self.parse_ratings,
                      meta={'Data': data})

    def parse_ratings(self, response):
        data = response.meta['Data']

        avg_rating = float(response.xpath('//span[@class="average-rating"]/a/text()').extract_first())
        data['avg_rating'] = avg_rating

        ratings = response.xpath('//div[@class="rating-histogram clear rating-histogram-exploded"]/ul/li')
        ratings = ratings.xpath('.//@title').extract()
        n_star_ratings = [0]*10
        i = 0
        for each in ratings:
            elements = each.split()
            rating_null = 'No' in elements
            if rating_null:
                n_star_ratings[i] = 0
            else:
                n_star_ratings[i] = int(elements[0].replace(',',''))
            i += 1


        data['half_star'] = n_star_ratings[0]
        data['one_star'] = n_star_ratings[1]
        data['one_half_star'] = n_star_ratings[2]
        data['two_star'] = n_star_ratings[3]
        data['two_half_star'] = n_star_ratings[4]
        data['three_star'] = n_star_ratings[5]
        data['three_half_star'] = n_star_ratings[6]
        data['four_star'] = n_star_ratings[7]
        data['four_half_star'] = n_star_ratings[8]
        data['five_star'] = n_star_ratings[9]

        yield data
