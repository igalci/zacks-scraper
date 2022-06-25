import requests, json, pickle
from bs4 import BeautifulSoup
from datetime import datetime
from decimal import Decimal

#Mimic Firefox browser
HEADERS = {'Host':'www.zacks.com','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate, br',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Cache-Control':'no-cache', 'Pragma':'no-cache', 'Upgrade-Insecure-Requests':'1'}

#JSON entry names
JSON_VAR = "document.obj_data"
EPS_JSON = "earnings_announcements_earnings_table"
REVENUE_JSON = "earnings_announcements_sales_table"

#Positions of fields in the JSON
DATE_REPORTED_POS = 0
PERIOD_END_POS = 1
ESTIMATE_POS = 2
ACTUAL_POS = 3
REPORT_TIME_POS = 6

#Output names of dictionary entries
DATE_REPORTED = "Date_Reported"
EPS_ACTUAL = "EPS_Actual"
EPS_ESTIMATE = "EPS_Estimate"
REVENUE_ACTUAL = "Revenue_Actual"
REVENUE_ESTIMATE = "Revenue_Estimate"
REPORT_TIME = "Reported_After_Hours"

class Scraper():
    def __init__(self, ticker:str):
        self.ticker=ticker.strip().upper().replace("-",".")

    def get(self):
        url="https://www.zacks.com/stock/research/"+self.ticker+"/earnings-calendar"
        filename = 'zacks-website-test.pk'
        
        data = requests.get(url,headers=HEADERS)
        data = data.text
        with open(filename, 'wb') as fi:
            # dump your data into the file
            pickle.dump(data, fi)
        # with open(filename, 'rb') as fi:
        #     data = pickle.load(fi)

        soup = BeautifulSoup(data, "html.parser")
        scripts = soup.find_all('script', type=None)
        good_script = None
        for script in scripts:
            if JSON_VAR in str(script.string):
                good_script = script.string
                break
        if not good_script:
            raise ValueError ("Bad ticker. Not found on Zacks.com.")
        else:
            json_data = self.__script_to_json(good_script)

        final={}
        for entry in json_data[EPS_JSON]:
            temp_dict={}
            period_end = self.__str_to_date(entry[PERIOD_END_POS])
            temp_dict[DATE_REPORTED] = self.__str_to_date(entry[DATE_REPORTED_POS])
            temp_dict[EPS_ESTIMATE] = self.__str_to_num(entry[ESTIMATE_POS])
            temp_dict[EPS_ACTUAL] = self.__str_to_num(entry[ACTUAL_POS])
            temp_dict[REPORT_TIME] = self.__after_hours(entry[REPORT_TIME_POS])
            final[period_end]=temp_dict

        for entry in json_data[REVENUE_JSON]:
            period_end = self.__str_to_date(entry[PERIOD_END_POS])
            if period_end in final.keys():
                temp_dict=final[period_end]
            else:
                temp_dict={}
            if DATE_REPORTED not in temp_dict.keys() or temp_dict[DATE_REPORTED] is None:
                temp_dict[DATE_REPORTED] = self.__str_to_date(entry[DATE_REPORTED_POS])
            if REPORT_TIME not in temp_dict.keys() or temp_dict[REPORT_TIME] is None:
                temp_dict[REPORT_TIME] = self.__after_hours(entry[REPORT_TIME_POS])
            temp_dict[REVENUE_ESTIMATE] = self.__str_to_num(entry[ESTIMATE_POS],0)
            temp_dict[REVENUE_ACTUAL] = self.__str_to_num(entry[ACTUAL_POS],0)
            final[period_end]=temp_dict
            print(final[period_end])


    def __script_to_json(self,script):
        return json.loads("{"+script.split(JSON_VAR)[1].split("{")[1].split("}")[0]+"}")

    def __str_to_date(self,date_str):
        date_str = date_str.replace(" ","").replace("-","/")
        num_of_slashes = date_str.count("/")
        if num_of_slashes == 1:
            date = datetime.strptime(date_str, '%m/%Y').date()
        elif num_of_slashes == 2:
            date = datetime.strptime(date_str, '%m/%d/%y').date()
        else:
            return None
        return date

    #string to decimal (or int if rounding is 0). Returns None for bad inputs
    def __str_to_num (self,num:str,rounding_digits=2):
        if num == None:
            return None
        num=num.replace(" ","").replace(",","").replace("$","").replace("%","")
        if rounding_digits == 0:
            try:
                num=int(Decimal(num))
            except:
                return None
        else:
            try:
                num=Decimal(num)
            except:
                return None
            num=round(num,rounding_digits)
        return num

    def __after_hours(self,announcement_time):
        announcement_time = announcement_time.lower().replace(" ","")
        if "after" in announcement_time:
            return True
        elif "before" in announcement_time:
            return False
        else:
            return None
            

scrape = Scraper("rivn")
#print(json.dumps(scrape.get(), indent=4))

# f = open('data.json', 'w')
# f.write(str(json.dumps(scrape.get(), indent=4)))

scrape.get()