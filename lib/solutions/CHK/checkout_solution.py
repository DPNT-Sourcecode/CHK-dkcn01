

# noinspection PyUnusedLocal
# skus = unicode string

item_prices = {
"A":{1:50, 3:130, 5:200},
"B":{1:30, 2:45},
"C":{1:20},
"D":{1:15},
"E":{1:40}
}

special_offers = {
    "E":{ 2:{1:"B"} }
}

def calc_item_count(skus:str)-> dict:
    item_count={}
    special_offer_eligibility_count = {}
    total = 0
    for item in skus:
        if item not in item_prices.keys():
            return -1
        else:
            if item not in item_count:
                item_count[item] = 1
            else:
                item_count[item] += 1
    return item_count
    
def calc_special_offers(item_count):
    for sp_offer_k in special_offers:
        sp_offer_divs = list(special_offers[sp_offer_k].keys())
        sp_offer_divs.reverse()
        for div in sp_offer_divs:
            if int(item_count / div) > 0:
                sp_count = int(item_count / div)
                sp_offer_avail = special_offer_eligibility_count[ special_offers[sp_offer_k][div] ]     # {1:"B"}
                
    return sp_offer_avail
    
def calc_total(item_count)
    for item in item_count:
        i_prices = list(item_prices[item].keys())
        i_prices.reverse()
        for mcount in i_prices:
            if item_count[item] >= mcount:      # worth performing division
                val = int(item_count[item]/mcount)
                total += val * item_prices[item][mcount]
                item_count[item] -= val * mcount
                #print(f"{val} {item}")
                #print(item_count)
                #print(total)
    return total
    
def checkout(skus:str):
    assert type(skus) is str, "skus must be a string"
    item_count = calc_item_count(skus)
    
    spo = calc_special_offers(item_count)
    
    total = calc_total(item_count)
    return total

