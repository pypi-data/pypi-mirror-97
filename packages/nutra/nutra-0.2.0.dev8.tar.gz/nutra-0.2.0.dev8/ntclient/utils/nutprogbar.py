def print_nutprogbar(food_amts, food_analyses, nutrients):
    def tally(nut_percs):
        for nut in nut_percs:
            # TODO: get RDA values from nt DB, tree node nested organization
            print(nut)

    food_analyses = {
        x[0]: {y[1]: y[2] for y in food_analyses if y[0] == x[0]} for x in food_analyses
    }

    # print(food_ids)
    # print(food_analyses)

    nut_amts = {}

    for id, grams in food_amts.items():
        r = grams / 100.0
        analysis = food_analyses[id]
        for n, amt in analysis.items():
            if n not in nut_amts:
                nut_amts[n] = amt
            else:
                nut_amts[n] += amt

    nut_percs = {}

    for id, amt in nut_amts.items():
        # TODO: if not rda, show raw amounts?
        if type(nutrients[id][1]) == float:
            nut_percs[id] = round(amt / nutrients[id][1], 3)

    tally(nut_percs)
    return nut_percs
