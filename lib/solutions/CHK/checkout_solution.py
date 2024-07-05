

# noinspection PyUnusedLocal
# skus = unicode string

item_prices = {
"A":{1:50, 3:130},
"B":{1:30, 2:45},
"C":{1:20},
"D":{1:15},
}

def checkout(skus):
    item_count={}
    total = 0
    for item in skus:
        current_item = item.upper()
        if current_item not in item_prices.keys():
            return -1
        else:
            if current_item not in item_count:
                item_count[current_item] = 1
            else:
                item_count[current_item] += 1
    
    for item in item_count:
        i_prices = list(item_prices[item].keys())
        i_prices.reverse()
        for mcount in i_prices:
            if item_count[item] >= mcount:      # worth performing division
                val = int(item_count[item]/mcount)
                total += val * item_prices[item][mcount]
                item_count[item] -= val
                print(f"{val} {item}")
    return total


