import json
#your_json={"mart":"WALMART_US","sku":"LM-ON09230","wpid":"5C7Y06LO4YS6","gtin":"03603314112727","productName":"Ocean Nutrition Formula ONE Marine Pellet - Medium Medium Pellets - 100 Grams[ PACK OF 2 ]","shelf":"[\"Home Page\",\"Pets\",\"Fish\",\"Fish Food\",\"Fish Food: Pellets and Fish Flakes\"]","productType":"Fish Food","price":{"currency":"USD","amount":28.55},"publishedStatus":"PUBLISHED","lifecycleStatus":"ACTIVE"}

your_json='{"ItemResponse":[{"mart":"WALMART_US","sku":"LM-ON09230","wpid":"5C7Y06LO4YS6","gtin":"03603314112727","productName":"Ocean Nutrition Formula ONE Marine Pellet - Medium Medium Pellets - 100 Grams[ PACK OF 2 ]","shelf":"[\"Home Page\",\"Pets\",\"Fish\",\"Fish Food\",\"Fish Food: Pellets and Fish Flakes\"]","productType":"Fish Food","price":{"currency":"USD","amount":28.55},"publishedStatus":"PUBLISHED","lifecycleStatus":"ACTIVE"}],"totalItems":1}'
#
#myArr=JSON.parse(your_json)

def parse_json(your_json):
    to_dict = json.loads(your_json)
    print (to_dict)
    for item in to_dict['price']:
        print ('amount')

