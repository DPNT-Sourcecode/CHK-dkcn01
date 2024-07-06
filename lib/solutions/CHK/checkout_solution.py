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

# I know I could use directly a string instead of the tupple
group_discounts = {
    ('S','T','X','Y','Z'):{3:45, 4:20}
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
            sp_offer_divs.sort()
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

def apply_group_discount(gd_item_count:dict):
    print(gd_item_count)
    to_remove_from_total = 0
    to_add_to_total = 0
    for group_disc in group_discounts:
        # this loop is optional in this case since we only have on group discount but hypothtically
        # the supermarket could have more in the future
        #gd_indiv_counts = {}
        gd_indiv_prices = {}
        affected_products_counter = 0
        
        for product in group_disc:
            # product will be S, T, X, Y, Z
            #gd_indiv_count[product] = gd_item_count[product]
            #CAREFUL HERE - only works if no other discount applicable when purchasing more than 1 unit
            gd_indiv_prices[product] = item_prices[product][1]
            
        # sorting the dictionnary by (price) value
        # many combinations of 3 products can be made and lead to a discount 
        # but we want the best discount for the customer
        priority_product_prices = dict(sorted(gd_indiv_prices.items(), key=lambda item: item[1], reverse=True))
        print(priority_product_prices)
        
        for product in priority_product_prices:
            if product in gd_item_count:
                affected_products_counter += gd_item_count[product]
        
        print(f"affected_products_counter {affected_products_counter}")
        
        gp_multiples = list(group_discounts[group_disc].keys())
        gp_multiples.sort()
        gp_multiples.reverse()
        
        print("####")
        print(gp_multiples)
        
        div = 0
        div_mult = 0
        for ammount in gp_multiples:
            ###for ammount in group_discounts[group_disc]:
            #if affected_products_counter >= ammount:
            div = int(affected_products_counter / ammount)
            div_mult = ammount
            #else:
            #    pass
            print(f"div {div}")
            print(f"div_mult {div_mult}")
        
            #items_to_remove = div * div_mult
            counter = div * div_mult
            if div > 0:
                for product in priority_product_prices:
                    print(product)
                    if product in gd_item_count:
                        if gd_item_count[product] <= counter:
                            
                            affected_products_counter -= gd_item_count[product]
                            print(f"-- affected_products_counter {affected_products_counter}")
                            
                            to_remove_from_total += priority_product_prices[product]*gd_item_count[product]
                            print(f"to_remove_from_total {to_remove_from_total}")
                            
                            
                            gd_item_count[product] -= gd_item_count[product]
                            print(f"{gd_item_count[product]}{product}")
                            print(f"gd_item_count[product] {gd_item_count[product]}")
                            
                            print("-----")
                        else:
                            print(f"SP2 {product} {gd_item_count[product]}")
                            affected_products_counter -= gd_item_count[product]
                            print(f"-- affected_products_counter {affected_products_counter}")
                            
                            to_remove_from_total += priority_product_prices[product]*gd_item_count[product]
                            print(f"to_remove_from_total {to_remove_from_total}")
                            
                            
                            gd_item_count[product] -= gd_item_count[product]
                            print(f"{gd_item_count[product]}{product}")
                            print(f"gd_item_count[product] {gd_item_count[product]}")
                            
                            print("-----")
                    else:
                        print(f"SP1 {product}")
                        
                print("======")
                print(group_discounts)
                to_add_to_total += group_discounts[group_disc][div_mult]
                print(f"to_add_to_total {to_add_to_total}")
                print("--")
    print(f"ADD {to_add_to_total}")
    print(f"SUB {to_remove_from_total}")
    return to_add_to_total - to_remove_from_total

def calc_total(item_count):
    # calc total based only on item_count and item_prices
    total = 0
    for item in item_count:
        i_prices = list(item_prices[item].keys())
        i_prices.sort()
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
        item_count_for_group_discounts = copy.deepcopy(item_count)
        
        spo_applicable = calc_special_offers_applicable(item_count_for_discounts)
        print(f"spo {spo_applicable}")
        
        #print(item_count)
        apply_spo_applicable(spo_applicable, item_count)
        
        #print(item_count)
        total = calc_total(item_count)
        
        offset = apply_group_discount(item_count_for_group_discounts)
        print(f"offset {offset}")
        total += offset
        
        print(f"total {total}")
        
        return total
    else:
        return -1





