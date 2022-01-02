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
    STATES = [
                  "American-Samoa",
                  "District-of-Columbia",
                  "North-Carolina",
                  "North-Dakota",
                  "New-Jersey",
                  "New-Mexico",
                  "New-York",
                  "Puerto-Rico",
                  "Rhode-Island",
                  "South-Carolina",
                  "South-Dakota",
                  "Virgin-Islands",
                  "West-Virginia"
    ]
    for index, state in enumerate(STATES):
        global currentState 
        currentState = STATES[index].lower()
        urls.append({'url':'http://prohacvice.com/state/{}/'.format(currentState),'state':currentState})
    
    def start_requests(self):
        print("PRINT PRINT PRINT URLS")
        print(urls)
        start_urls = urls
        for url_to_use in start_urls:
            yield scrapy.Request(url=url_to_use['url'], callback=self.parse,cb_kwargs={'currentState':url_to_use['state']})
       
    def parse(self, response,currentState):
        print('CURRENT STATE ***')
        print(currentState)
        print('END CURRENT SATE ***')

        CURRENT_STATE_DIV = 'div.header-content'
        for cur_state in response.css(CURRENT_STATE_DIV):
            STATE_SELECTOR = 'h1 ::text'
            
        FEDERAL_COURTS_DIV = '#federal-courts li'


        for fed_court in response.css(FEDERAL_COURTS_DIV):
            # print(currentState)
            NAME_SELECTOR = 'li a ::attr(title)'
            URL = 'li a ::attr(href)'
            federal_court = {
                'state': currentState,
                'court_title': fed_court.css(NAME_SELECTOR).extract_first(),
                'url': fed_court.css(URL).extract_first(),
                'federal_district': fed_court.css(NAME_SELECTOR).extract_first()
            }
            # yield {
            # 'title': fed_court.css(NAME_SELECTOR).extract_first(),
            # 'url' : fed_court.css(URL).extract_first()
            # }
            try: 
                with connection.cursor() as cursor: 
                    sql = "INSERT INTO `federal_districts` (`state`, `court_title`,`url`,`district`) VALUES (%s, %s, %s, %s)" 
                    cursor.execute(sql, (federal_court["state"], federal_court["court_title"],federal_court["url"],federal_court["federal_district"])) 
                    connection.commit() 
            except:
                print('exception')
        BANKRUPTCY_COURTS_DIV = '#bankruptcy-courts li'
        for state_court in response.css(BANKRUPTCY_COURTS_DIV):
            # print(currentState)
            NAME_SELECTOR = 'li a ::attr(title)'
            URL = 'li a ::attr(href)'
            bankruptcy_court = {
                'state' : currentState,
                'court_title' : state_court.css(NAME_SELECTOR).extract_first(),
                'url': state_court.css(URL).extract_first(),
                'federal_district': state_court.css(NAME_SELECTOR).extract_first(),
            }
            # yield {
            # 'title': state_court.css(NAME_SELECTOR).extract_first(),
            # 'url' : state_court.css(URL).extract_first()
            # }
            try: 
                with connection.cursor() as cursor: 
                    sql = "INSERT INTO `bankruptcy_districts` (`state`, `court_title`,`url`) VALUES (%s, %s, %s)" 
                    cursor.execute(sql, (bankruptcy_court["state"], bankruptcy_court["court_title"],bankruptcy_court["url"])) 
                    connection.commit() 
            except:
                print('exception')
            
            #save name
            #save url
        FORMS_DIV = '#forms li'
        for forms in response.css(FORMS_DIV):
            # print(currentState)
            NAME_SELECTOR = 'li a ::attr(title)'
            URL = 'li a ::attr(href)'
            form_info = {
                'form_name' : forms.css(NAME_SELECTOR).extract_first(),
                'form_pdf_url' : forms.css(URL).extract_first(),
                'state' : currentState
            }
            # yield {
            # 'title': forms.css(NAME_SELECTOR).extract_first(),
            # 'url' : forms.css(URL).extract_first()
            # }
            try: 
                with connection.cursor() as cursor: 
                    sql = "INSERT INTO `forms` (`state`, `form_name`,`form_pdf_url`) VALUES (%s, %s, %s)" 
                    cursor.execute(sql, (form_info["state"], form_info["form_name"],form_info["form_pdf_url"])) 
                    connection.commit() 
            except:
                print('exception')
            #save name
            #save url
        
        COMMON_QUESTIONS_DIV = '#faq dl'
        ANSWER_SELECTOR ='#faq dl dd *::text'
        answersTextArray = response.css(ANSWER_SELECTOR).getall()
        
        print("AnswerTextArray ***")
        print(answersTextArray)
        print("End Answer Text Array ***")
        for index, answer in enumerate(answersTextArray):
            try: 
                with connection.cursor() as cursor: 
                        sql = "INSERT INTO `common_questions` (`state`, `is_there_a_fee`,`what_documents_do_i_need`,`how_do_i_apply`,`is_local_counsel_required`) VALUES (%s, %s, %s, %s, %s)" 
                        cursor.execute(sql, (currentState, answersTextArray[0],answersTextArray[1],answersTextArray[2],answersTextArray[3])) 
                        connection.commit()
            except:
                print('exception')

