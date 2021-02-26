from csv import DictWriter
import scrapy
import json
from scrapy.spiders.init import InitSpider



class SchafkopfSpider(InitSpider):
    name = 'SchafkopfSpider'
    login_url = '*'
    start_urls = [
        '*' % i for i in range(50400001, 50500000)
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": "0.25"
    }

    def init_request(self):
        return scrapy.Request(
            url=self.login_url,
            callback=self.login,
        )

    def login(self, response):
        yield scrapy.FormRequest.from_response(
            response=response,
            formid='login_form',
            formdata={
                'login': 'Domi2002',
                'password': '8472borgSP.!',
            },
            callback=self.initialized,
        )

    def parse(self, response):
        game_protocol = {}
        game_protocol["number"] = response.selector.xpath('/html/body/div[1]/div/div[1]/div/h2//text()').get()
        game_protocol["type"] = response.selector.xpath('/html/body/div[1]/div/div[1]/div/h1//text()').get()
        game_protocol["special_rules"] = response.selector.xpath('/html/body/div[1]/div/div[5]/div[2]/table/tbody/tr[2]/td//text()').get()
        game_protocol["short_version"] = False
        game_protocol["tariff"] = response.selector.xpath('/html/body/div[1]/div/div[5]/div[2]/table/tbody/tr[1]/td//text()').get()
        game_protocol["result"] = response.selector.xpath('/html/body/div[1]/div/div[5]/div[2]/table/tbody/tr[4]/td//text()').get()
        game_protocol["legen"] = response.selector.xpath('/html/body/div[1]/div/div[5]/div[2]/table/tbody/tr[6]/td/a//text()').get()
        game_protocol["contra"] = response.selector.xpath('/html/body/div[1]/div/div[5]/div[2]/table/tbody/tr[7]/td//text()').get()

        game_protocol["players"] = {}
        for i in range(4):
            game_protocol["players"][i] = {}
            game_protocol["players"][i]["name"] = response.selector.xpath(f'/html/body/div[1]/div/div[5]/div[1]/div/div[{i+1}]/div/a/div[2]//text()').get().strip()
            game_protocol["players"][i]["cards"] = [card for card in response.selector.xpath(f'/html/body/div[1]/div/section/div[2]/div[2]/div[{i+1}]/div[2]//text()').extract() if '\n' not in card]

        if len(game_protocol["players"][0]["cards"]) == 6:
            game_protocol["short_version"] = True

        game_protocol["bidding"] = [step.replace('\n          ', '').strip() for step in
         response.selector.xpath('/html/body/div[1]/div/section/div[3]/div[2]//text()').extract() if
         step != '\n          ']

        # save the tricks

        tricks = 8 if game_protocol["short_version"] is False else 6
        game_protocol["tricks"] = {}
        for i in range(tricks):
            game_protocol["tricks"][i] = [info for info in response.selector.xpath(f'/html/body/div[1]/div/section/div[{i+4}]//text()').extract() if
             '\n' not in info]

        # Saving into the csv
        game_protocol = clean_dict(game_protocol)
        fieldnames = list(game_protocol.keys())
        with open("/models/data/Get process_data/Get process_data/spiders/games500-504.csv", 'a', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, fieldnames=fieldnames, delimiter=';')
            #writer.writeheader()
            writer.writerow(game_protocol)


def clean_dict(dictionary):
    for key, value in dictionary.items():
        if type(value) == str:
            dictionary[key] = value.replace('\n', '').strip()
        elif type(value) == bool:
            pass
        elif type(value) == dict:
            clean_dict(value)
        elif type(value) == list:
            for counter, item in enumerate(value):
                dictionary[key][counter] = item.replace('\n', '').strip()
    return dictionary
