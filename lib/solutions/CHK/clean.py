import copy

# noinspection PyUnusedLocal
# skus = unicode string

item_prices = {
    "A": {1: 50, 3: 130, 5: 200},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
    "E": {1: 40},
    "F": {1: 10},
    "G": {1: 20},
    "H": {1: 10, 5: 45, 10: 80},
    "I": {1: 35},
    "J": {1: 60},
    "K": {1: 70, 2: 120},
    "L": {1: 90},
    "M": {1: 15},
    "N": {1: 40},
    "O": {1: 10},
    "P": {1: 50, 5: 200},
    "Q": {1: 30, 3: 80},
    "R": {1: 50},
    "S": {1: 20},
    "T": {1: 20},
    "U": {1: 40},
    "V": {1: 50, 2: 90, 3: 130},
    "W": {1: 20},
    "X": {1: 17},
    "Y": {1: 20},
    "Z": {1: 21},
}

special_offers = {
    "E": {2: {"B": 1}},
    "F": {3: {"F": 1}},
    "N": {3: {"M": 1}},
    "R": {3: {"Q": 1}},
    "U": {4: {"U": 1}},
}

# I know I could use directly a string instead of the tupple
# a set would have been better in the sense that we do not care the order of the letters
# however a set is not iterable so would require to be converted multiple times
#
# in a prod environment adding methods to eventually validate every entry in group_discount could be another option
# just to say this aspect could/should be improved

group_discounts = {("S", "T", "X", "Y", "Z"): {3: 45, 4: 20}}


class SupermarketCheckout:
    def __init__(self, item_prices, special_offers={}, group_discounts={}):
        """
        __init__(self, item_prices, special_offers={}, group_discounts={})

        Constructor
        """

        self.item_prices = item_prices
        self.special_offers = special_offers
        self.group_discounts = group_discounts

    def calc_item_count(self, skus: str) -> dict:
        """
        calc_item_count(self, skus:str)->dict

        returns a dictionnary with SKU letter (string) as key and count (int) as value
        """

        assert type(skus) is str, f"skus must be a string, you provided a {type(skus)}"

        item_count = {}
        special_offer_eligibility_count = {}
        total = 0
        for item in skus:
            if item not in self.item_prices.keys():
                return -1
            else:
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
        return item_count

    def calc_special_offers_applicable(self, item_count: dict) -> dict:
        """
        calc_special_offers_applicable(self, item_count:dict)->dict

        calculate how many "free" articles the consumer is elligible
        hence return a dictionnary with the Sku letter and count
        which will then be substracted from the total by apply_spo_applicable
        """

        assert (
            type(item_count) is dict
        ), f"item_count must be a string, you provided a {type(item_count)}"

        special_offer_eligibility_count = {}
        for sp_offer_k in self.special_offers:
            if sp_offer_k in item_count:
                sp_offer_divs = list(self.special_offers[sp_offer_k].keys())
                sp_offer_divs.sort()
                sp_offer_divs.reverse()
                for div in sp_offer_divs:
                    discount_multiple = int(item_count[sp_offer_k] / div)
                    if discount_multiple > 0:

                        for item_letter in item_count:
                            if item_letter in list(
                                self.special_offers[sp_offer_k][div].keys()
                            ):
                                while discount_multiple > 0:
                                    if item_letter in special_offer_eligibility_count:
                                        special_offer_eligibility_count[
                                            item_letter
                                        ] += self.special_offers[sp_offer_k][div][
                                            item_letter
                                        ]
                                        item_count[sp_offer_k] -= div
                                        discount_multiple -= 1
                                    else:
                                        special_offer_eligibility_count[item_letter] = (
                                            self.special_offers[sp_offer_k][div][
                                                item_letter
                                            ]
                                        )
                                        item_count[sp_offer_k] -= div
                                        discount_multiple -= 1
                            else:
                                pass
        return special_offer_eligibility_count

    def apply_spo_applicable(self, spo: dict, item_count: dict) -> int:
        """
        apply_spo_applicable(self, spo:dict, item_count:dict)->int

        applies SPecial Offer (SPO) discounts
        This method operates on the item_count (free articles)
        requires the spo (dictionnary) as parameter :
            applicable special offers generated by calc_special_offers_applicable
        requires the item_count (dictionnary) as parameters :
            character (string) as key and count (int) as value
        """

        assert type(spo) is dict, f"spo must be a string, you provided a {type(spo)}"
        assert (
            type(item_count) is dict
        ), f"item_count must be a string, you provided a {type(item_count)}"

        # removes applicables offers from item_count
        substract_item_count = {}
        for letter in spo:
            item_count[letter] -= spo[letter]

    def apply_group_discount(self, gd_item_count: dict) -> int:
        """
        apply_group_discount(self, gd_item_count:dict)->int

        Applies group discounts, return an offset (int) to be added to the total from checkout
        gd_item_count is a (deep) copy of the item_count dictionnary
        """

        assert (
            type(gd_item_count) is dict
        ), f"gd_item_count must be a string, you provided a {type(gd_item_count)}"

        to_remove_from_total = 0
        to_add_to_total = 0
        for group_disc in self.group_discounts:
            # this loop is optional in this case since we only have on group discount but hypothtically
            # the supermarket could have more in the future
            # gd_indiv_counts = {}
            gd_indiv_prices = {}
            affected_products_counter = 0

            for product in group_disc:
                # product will be S, T, X, Y, Z
                # gd_indiv_count[product] = gd_item_count[product]
                # CAREFUL HERE - only works if no other discount applicable when purchasing more than 1 unit
                gd_indiv_prices[product] = self.item_prices[product][1]

            # sorting the dictionnary by (price) value
            # many combinations of 3 products can be made and lead to a discount
            # but we want the best discount for the customer
            priority_product_prices = dict(
                sorted(gd_indiv_prices.items(), key=lambda item: item[1], reverse=True)
            )

            for product in priority_product_prices:
                if product in gd_item_count:
                    affected_products_counter += gd_item_count[product]

            gp_multiples = list(self.group_discounts[group_disc].keys())
            gp_multiples.sort()
            gp_multiples.reverse()

            div = 0
            div_mult = 0
            for ammount in gp_multiples:

                div = int(affected_products_counter / ammount)
                div_mult = ammount

                counter = div * div_mult

                for product in priority_product_prices:
                    if counter > 0:

                        if product in gd_item_count:

                            if gd_item_count[product] <= counter:
                                # I can remove all of gd_item_count
                                affected_products_counter -= gd_item_count[product]
                                to_remove_from_total += (
                                    priority_product_prices[product]
                                    * gd_item_count[product]
                                )
                                # CAREFUL - the order of these two following lines is important
                                couter -= gd_item_count[product]
                                gd_item_count[product] -= gd_item_count[product]

                            else:
                                # I can't remove all of gd_item_count, will remove counter instead
                                affected_products_counter -= counter
                                to_remove_from_total += (
                                    priority_product_prices[product] * counter
                                )
                                # CAREFUL - the order of these two following lines is important
                                gd_item_count[product] -= counter
                                counter -= counter

                        if counter == 0:
                            to_add_to_total += (
                                self.group_discounts[group_disc][div_mult] * div
                            )

        return to_add_to_total - to_remove_from_total

    def calc_total(self, item_count) -> int:
        """
        calc_total(self, item_count)->int

        calculate the total (int) based on teh item_count dictionnary
        Note:
        item_count dictionnary contains as key a (string) indicating the product
        and as value the count (int) of these products being purchased
        """

        assert (
            type(item_count) is dict
        ), f"item_count must be a string, you provided a {type(item_count)}"

        # calc total based only on item_count and item_prices
        total = 0
        for item in item_count:
            i_prices = list(self.item_prices[item].keys())
            i_prices.sort()
            i_prices.reverse()
            for mcount in i_prices:
                if item_count[item] >= mcount:  # worth performing division
                    val = int(item_count[item] / mcount)
                    total += val * self.item_prices[item][mcount]
                    item_count[item] -= val * mcount
        return total

    def checkout(self, skus: str) -> int:
        """
        checkout(self, skus:str)->int

        This was the original checkout function
        Takes a string argument skus (a succession of characters, case sensitive, each letter representing a product purchased)
        returns the total ammount of money (int) due at the checkout
        (with all special_prices, discounts, special_offers applied)
        in case of a wrong/unexisting article in the string, it returns -1 instead of the total
        """

        assert type(skus) is str, f"skus must be a string, you provided a {type(skus)}"

        item_count = self.calc_item_count(skus)
        if item_count != -1:
            item_count_for_discounts = copy.deepcopy(item_count)
            item_count_for_group_discounts = copy.deepcopy(item_count)

            spo_applicable = self.calc_special_offers_applicable(
                item_count_for_discounts
            )
            self.apply_spo_applicable(spo_applicable, item_count)

            total = self.calc_total(item_count)

            offset = self.apply_group_discount(item_count_for_group_discounts)
            total += offset

            return total
        else:
            return -1


def checkout(skus: str) -> int:
    assert type(skus) is str, f"skus must be a string, you provided a {type(skus)}"
    supermarket_instance = SupermarketCheckout(
        item_prices, special_offers, group_discounts
    )
    total = supermarket_instance.checkout(skus)
    return total
