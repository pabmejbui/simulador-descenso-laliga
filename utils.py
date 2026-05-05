def sort_table_with_h2h(table, h2h):

    def compare(a, b):

        # puntos
        if table[a]["points"] != table[b]["points"]:
            return table[b]["points"] - table[a]["points"]

        key = tuple(sorted([a, b]))

        if key in h2h:

            a_h2h = h2h[key][a]
            b_h2h = h2h[key][b]

            if a_h2h["points"] != b_h2h["points"]:
                return b_h2h["points"] - a_h2h["points"]

            if a_h2h["gd"] != b_h2h["gd"]:
                return b_h2h["gd"] - a_h2h["gd"]

        # fallback
        gd_a = table[a]["gf"] - table[a]["ga"]
        gd_b = table[b]["gf"] - table[b]["ga"]

        if gd_a != gd_b:
            return gd_b - gd_a

        return table[b]["gf"] - table[a]["gf"]

    teams = list(table.keys())

    # ordenar con comparator
    from functools import cmp_to_key
    teams.sort(key=cmp_to_key(compare))

    return [(t, table[t]) for t in teams]