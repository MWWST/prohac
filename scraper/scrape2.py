import scrapy
import pymysql.cursors 


class ProHacSpider(scrapy.Spider):
    global connection
    connection = pymysql.connect(host='localhost', 
                             user='root', 
                             password='root', 
                             port=8889,
                             db='phvscrape1', 
                             charset='utf8', 
                             cursorclass=pymysql.cursors.DictCursor) 
    name = "prohac_spider2"
    global STATES
    global urls
    urls = []

    def start_requests(self):
        try: 
            with connection.cursor() as cursor: 
                sql = "SELECT `url` FROM phvscrape1.federal_districts where state like '%-%' AND court_description is NULL"
                cursor.execute(sql)
                results = cursor.fetchall()
                for i in results:
                    print(i['url'])
                    currentUrl = 'http://prohacvice.com{}'.format(i['url'])
                    print(currentUrl)
                    yield scrapy.Request(url=currentUrl, callback=self.parse,cb_kwargs={'currentUrl': i['url']})
        except Exception as e:
            print('exception')
            print(e)

    def parse(self, response,currentUrl):
            print('CURRENT URL ***')
            print(currentUrl)
            print('END CURRENT URL ***')

            DESCRIPTION_DIV = '#main p'
            for content in response.css(DESCRIPTION_DIV):
                CONTENT_SELECTOR = '::text'
            FEDERAL_COURTS_DIV = '#districts li'
            # p1 = response.xpath('string(//*[@id="main"]/p[1])').extract_first()
            # p2 = response.xpath('string(//*[@id="main"]/p[2])').extract_first()
            for fed_court in response.css(FEDERAL_COURTS_DIV):
                # print(currentState)
                NAME_SELECTOR = 'li a ::attr(title)'
                URL = 'li a ::attr(href)'
                p1 = response.xpath('string(//*[@id="main"]/p[1])').extract_first()
                p2 = response.xpath('string(//*[@id="main"]/p[2])').extract_first()
                related_link = {
                    'current_url': currentUrl,
                    'related_link_text': fed_court.css(NAME_SELECTOR).extract_first(),
                    'related_link_url': fed_court.css(URL).extract_first(),
                    'fed_court_content_1' : p1,
                    'fed_court_content_2' : p2,
                }
                print("######FED COURT CONTENT")
                print(related_link['fed_court_content_1'])
                print("END FED COURT CONTENT #####")
                yield {
                'title': fed_court.css(NAME_SELECTOR).extract_first(),
                'url' : fed_court.css(URL).extract_first()
                }
                try: 
                    with connection.cursor() as cursor: 
                        sql = "INSERT INTO `related_links` (`current_url`, `related_link_text`,`related_link_url`) VALUES (%s, %s, %s)" 
                        cursor.execute(sql, (related_link["current_url"], related_link["related_link_text"],related_link["related_link_url"])) 
                        connection.commit() 
                except:
                    print('exception')
                
                try: 
                    with connection.cursor() as cursor:
                        sql = "UPDATE federal_districts SET court_description =%s, court_description_2 =%s WHERE url =%s"
                        
                        cursor.execute(sql,(related_link['fed_court_content_1'],related_link['fed_court_content_2'],related_link['current_url']))
                        connection.commit()
                except Exception as e:
                    print("!@#$%^^Update exception")
                    print(e)
                    print("END Update exception!@#$%^^")

            BANKRUPTCY_COURT_DIV = '#bankruptcy-courts'
            for bank_court in response.css(BANKRUPTCY_COURT_DIV):
                NAME_SELECTOR = 'li a ::attr(title)'
                URL = 'li a ::attr(href)'
                related_link = {
                        'current_url': currentUrl,
                        'related_link_text': bank_court.css(NAME_SELECTOR).extract_first(),
                        'related_link_url': bank_court.css(URL).extract_first(),
                    }
                # update by url to related links
                # update bankrupcy court table with bank_court_content for description
                try: 
                    with connection.cursor() as cursor: 
                        sql = "INSERT INTO `related_links` (`current_url`, `related_link_text`,`related_link_url`) VALUES (%s, %s, %s)" 
                        cursor.execute(sql, (related_link["current_url"], related_link["related_link_text"],related_link["related_link_url"])) 
                        connection.commit() 
                except:
                    print('exception')
                
                try: 
                    with connection.cursor as cursor:
                        sql = "UPDATE bankruptcy_districts SET `court_description` = %s WHERE url = %"
                        cursor.execute(sql,related_link['bank_court_content'],related_link['current_url'])
                        connection.commit()
                except Exception as e:
                    print(e)