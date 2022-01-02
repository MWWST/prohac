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
    name = "prohac_spider"
    global STATES
    global urls
    urls = []
    try: 
        with connection.cursor() as cursor: 
            sql = "SELECT * FROM phvscrape1.bankruptcy_districts WHERE (state = 'district-of-columbia' OR state = 'north-dakota' OR state ='new-mexico' OR state = 'new-jersey' OR state ='south-dakota' OR state= 'rhode-island' OR state = 'south-carolina')" 
            cursor.execute(sql) 
            result = cursor.fetchall()
            # print("HERE IS A RESULT")
            # print(result)
            for index, item in enumerate(result):
                urls.append(result[index])
                # print("***TESTING TESTING 123")
                # print(result[index])
            print('***URLS')
            print(urls)
            print('***URLS')
    except Exception as e:
        print('THIS IS NOT WORKING')
        print(e)
    # STATES = ["Alaska",
    #               "Alabama",
    #               "Arkansas",
    #               "American_Samoa",
    #               "Arizona",
    #               "California",
    #               "Colorado",
    #               "Connecticut",
    #               "District_of_Columbia",
    #               "Delaware",
    #               "Florida",
    #               "Georgia",
    #               "Guam",
    #               "Hawaii",
    #               "Iowa",
    #               "Idaho",
    #               "Illinois",
    #               "Indiana",
    #               "Kansas",
    #               "Kentucky",
    #               "Louisiana",
    #               "Massachusetts",
    #               "Maryland",
    #               "Maine",
    #               "Michigan",
    #               "Minnesota",
    #               "Missouri",
    #               "Mississippi",
    #               "Montana",
    #               "North_Carolina",
    #               "North_Dakota",
    #               "Nebraska",
    #               "New_Hampshire",
    #               "New_Jersey",
    #               "New_Mexico",
    #               "Nevada",
    #               "New_York",
    #               "Ohio",
    #               "Oklahoma",
    #               "Oregon",
    #               "Pennsylvania",
    #               "Puerto_Rico",
    #               "Rhode_Island",
    #               "South_Carolina",
    #               "South_Dakota",
    #               "Tennessee",
    #               "Texas",
    #               "Utah",
    #               "Virginia",
    #               "Virgin_Islands",
    #               "Vermont",
    #               "Washington",
    #               "Wisconsin",
    #               "West_Virginia",
    #               "Wyoming"]
   
    def start_requests(self):
        start_urls = urls
        for url_to_use in start_urls:
            yield scrapy.Request(url='http://prohacvice.com/'+url_to_use['url'], callback=self.parse,cb_kwargs={'currentUrl':url_to_use['url'],'currentState':url_to_use['state']})
       
    def parse(self, response,currentUrl,currentState):

        # BANKRUPTCY_COURTS_DIV = '#main'
        # for court in response.css(BANKRUPTCY_COURTS_DIV):
        #     print("CURRENT STATE *****")
        #     print(currentState)
        #     # NAME_SELECTOR = 'li a ::attr(title)'
        #     # URL = 'li a ::attr(href)'
        #     p1 = response.xpath('string(//*[@id="main"]/p[1])').extract_first()
        #     print("THIS IS FIRST PARAGRAPH")
        #     print(p1)
        #     print("THIS IS SECOND PARAGRAPH")
        #     p2 = response.xpath('string(//*[@id="main"]/p[2])').extract_first()
        #     data = {
        #         'current_url': currentUrl,
        #         # 'related_link_text': fed_court.css(NAME_SELECTOR).extract_first(),
        #         # 'related_link_url': fed_court.css(URL).extract_first(),
        #         'court_description_1' : p1,
        #         'court_description_2' : p2,
        #     }

        #     try: 
        #         with connection.cursor() as cursor:
        #             sql = "UPDATE bankruptcy_districts SET court_description =%s, court_description_2 =%s WHERE url =%s"
        #             cursor.execute(sql,(data['court_description_1'],data['court_description_2'],data['current_url']))
        #             connection.commit()
        #     except Exception as e:
        #         print("!@#$%^^Update exception")
        #         print(e)
        #         print("END Update exception!@#$%^^")

        COMMON_QUESTIONS_DIV = '#faq dl'
        ANSWER_SELECTOR ='#faq dl dd *::text'
        answersTextArray = response.css(ANSWER_SELECTOR).getall()
        print("CURRENT URL ***:::")
        print(currentUrl)
        print("CURRENT URL ***:::")
        print("AnswerTextArray ***")
        print(answersTextArray)
        print("End Answer Text Array ***")
        for index, answer in enumerate(answersTextArray):
            try: 
                with connection.cursor() as cursor: 
                        sql = "INSERT INTO `common_questions_bk` (`url`,`state`, `is_there_a_fee`,`what_documents_do_i_need`,`how_do_i_apply`,`is_local_counsel_required`) VALUES (%s, %s, %s, %s, %s, %s)" 
                        cursor.execute(sql, (currentUrl,currentState, answersTextArray[0],answersTextArray[1],answersTextArray[2],answersTextArray[3])) 
                        connection.commit()
            except Exception as e:
                print('exception')
                print(e)

    #     CURRENT_STATE_DIV = 'div.header-content'
    #     for cur_state in response.css(CURRENT_STATE_DIV):
    #         STATE_SELECTOR = 'h1 ::text'
    #     FEDERAL_COURTS_DIV = '#federal-courts li'
    #     for fed_court in response.css(FEDERAL_COURTS_DIV):
    #         # print(currentState)
    #         NAME_SELECTOR = 'li a ::attr(title)'
    #         URL = 'li a ::attr(href)'
    #         federal_court = {
    #             'state': currentState,
    #             'court_title': fed_court.css(NAME_SELECTOR).extract_first(),
    #             'url': fed_court.css(URL).extract_first(),
    #             'federal_district': fed_court.css(NAME_SELECTOR).extract_first()
    #         }
    #         # yield {
    #         # 'title': fed_court.css(NAME_SELECTOR).extract_first(),
    #         # 'url' : fed_court.css(URL).extract_first()
    #         # }
    #         try: 
    #             with connection.cursor() as cursor: 
    #                 sql = "INSERT INTO `federal_districts` (`state`, `court_title`,`url`,`district`) VALUES (%s, %s, %s, %s)" 
    #                 cursor.execute(sql, (federal_court["state"], federal_court["court_title"],federal_court["url"],federal_court["federal_district"])) 
    #                 connection.commit() 
    #         except:
    #             print('exception')
    #     BANKRUPTCY_COURTS_DIV = '#bankruptcy-courts li'
    #     for state_court in response.css(BANKRUPTCY_COURTS_DIV):
    #         # print(currentState)
    #         NAME_SELECTOR = 'li a ::attr(title)'
    #         URL = 'li a ::attr(href)'
    #         bankruptcy_court = {
    #             'state' : currentState,
    #             'court_title' : state_court.css(NAME_SELECTOR).extract_first(),
    #             'url': state_court.css(URL).extract_first(),
    #             'federal_district': state_court.css(NAME_SELECTOR).extract_first(),
    #         }
    #         # yield {
    #         # 'title': state_court.css(NAME_SELECTOR).extract_first(),
    #         # 'url' : state_court.css(URL).extract_first()
    #         # }
    #         try: 
    #             with connection.cursor() as cursor: 
    #                 sql = "INSERT INTO `bankruptcy_districts` (`state`, `court_title`,`url`) VALUES (%s, %s, %s)" 
    #                 cursor.execute(sql, (bankruptcy_court["state"], bankruptcy_court["court_title"],bankruptcy_court["url"])) 
    #                 connection.commit() 
    #         except:
    #             print('exception')
            
    #         #save name
    #         #save url
    #     FORMS_DIV = '#forms li'
    #     for forms in response.css(FORMS_DIV):
    #         # print(currentState)
    #         NAME_SELECTOR = 'li a ::attr(title)'
    #         URL = 'li a ::attr(href)'
    #         form_info = {
    #             'form_name' : forms.css(NAME_SELECTOR).extract_first(),
    #             'form_pdf_url' : forms.css(URL).extract_first(),
    #             'state' : currentState
    #         }
    #         # yield {
    #         # 'title': forms.css(NAME_SELECTOR).extract_first(),
    #         # 'url' : forms.css(URL).extract_first()
    #         # }
    #         try: 
    #             with connection.cursor() as cursor: 
    #                 sql = "INSERT INTO `forms` (`state`, `form_name`,`form_pdf_url`) VALUES (%s, %s, %s)" 
    #                 cursor.execute(sql, (form_info["state"], form_info["form_name"],form_info["form_pdf_url"])) 
    #                 connection.commit() 
    #         except:
    #             print('exception')
    #         #save name
    #         #save url
        
        



        # FEDERAL_COURTS_LINK        
        # NEXT_PAGE_SELECTOR = '#navigation a ::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # if currentState:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback=self.parse
        # )