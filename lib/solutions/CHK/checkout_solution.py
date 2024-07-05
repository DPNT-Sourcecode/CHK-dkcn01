

# noinspection PyUnusedLocal
# skus = unicode string

item_prices = {
"A":{1:50, 3:130}
"B":{1:30, 2:45}
"C":{1:20}
"D":{1:15}
}

def checkout(skus):
    for item in skus:
        if item.upper() not in item_prices.keys():
            return -1
        else:
            
    raise NotImplementedError()

