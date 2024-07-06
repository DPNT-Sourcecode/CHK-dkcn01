import copy

# noinspection PyUnusedLocal
# skus = unicode string

item_prices = {
"A":{1:50, 3:130, 5:200},
"B":{1:30, 2:45},
"C":{1:20},
"D":{1:15},
"E":{1:40},
"F":{1:10},
"G":{1:20},
"H":{1:10, 5:45, 10:80},
"I":{1:35},
"J":{1:60},
"K":{1:70, 2:120},
"L":{1:90},
"M":{1:15},
"N":{1:40},
"O":{1:10},
"P":{1:50, 5:200},
"Q":{1:30, 3:80},
"R":{1:50},
"S":{1:20},
"T":{1:20},
"U":{1:40},
"V":{1:50, 2:90, 3:130},
"W":{1:20},
"X":{1:17},
"Y":{1:20},
"Z":{1:21}
}

special_offers = {
    "E":{ 2:{"B":1} },
    "F":{ 3:{"F":1} },
    "N":{ 3:{"M":1} },
    "R":{ 3:{"Q":1} },
    "U":{ 4:{"U":1} }
}

def calc_item_count(skus:str)-> dict:
    # returns a dictionary with SKU letter as key and count as value
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
    
def calc_special_offers_applicable(item_count:dict)->dict:
    # calc how many "free" articles the consumer is elligible
    # hence return a dictionnary with the Sku letter and count
    # which will then be substracted from the total by apply_spo_applicable
    special_offer_eligibility_count = {}
    for sp_offer_k in special_offers:
        if sp_offer_k in item_count:
            sp_offer_divs = list(special_offers[sp_offer_k].keys())
            sp_offer_divs.reverse()
            for div in sp_offer_divs:
                #print(div)
                discount_multiple = int(item_count[sp_offer_k] / div)
                if discount_multiple > 0:
                    #print(f"discount multiple : {discount_multiple}") # until here we are on track !
                    
                    for item_letter in item_count:
                        if item_letter in list(special_offers[sp_offer_k][div].keys()):
                            while(discount_multiple>0):
                                if item_letter in special_offer_eligibility_count:
                                    special_offer_eligibility_count[item_letter] += special_offers[sp_offer_k][div][item_letter]
                                    item_count[sp_offer_k] -=  div
                                    discount_multiple -= 1
                                else:
                                    special_offer_eligibility_count[item_letter] = special_offers[sp_offer_k][div][item_letter]
                                    item_count[sp_offer_k] -=  div
                                    discount_multiple -= 1
                        else:
                            pass
    return special_offer_eligibility_count
    
def apply_spo_applicable(spo:dict, item_count:dict)->int:
    # removes applicables offers from item_count
    substract_item_count = {}
    for letter in spo:
        item_count[letter] -= spo[letter]

def calc_total(item_count):
    # calc total based only on item_count and item_prices
    total = 0
    for item in item_count:
        i_prices = list(item_prices[item].keys())
        i_prices.reverse()
        for mcount in i_prices:
            if item_count[item] >= mcount:      # worth performing division
                val = int(item_count[item]/mcount)
                total += val * item_prices[item][mcount]
                item_count[item] -= val * mcount
    return total
    
def checkout(skus:str):
    assert type(skus) is str, "skus must be a string"
    item_count = calc_item_count(skus)
    if item_count != -1:
        item_count_for_discounts = copy.deepcopy(item_count)
        
        spo_applicable = calc_special_offers_applicable(item_count_for_discounts)
        print(f"spo {spo_applicable}")
        
        #print(item_count)
        apply_spo_applicable(spo_applicable, item_count)
        
        #print(item_count)
        total = calc_total(item_count)
        print(f"total {total}")
        
        return total
    else:
        return -1