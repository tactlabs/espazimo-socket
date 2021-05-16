def startpy(dict1):
    # dict1 = {
    #     "value"     : 1,
    #     "Value_2"   : 9,
    #     "Value_3"   : 4
    #     }
    sorted_values = sorted(dict1.values()) # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in dict1.keys():
            if dict1[k] == i:
                sorted_dict[k] = dict1[k]
                break

    #print(sorted_dict)

    return(print(sorted_dict))

    # for i in sort_orders:
    #     print(i[0], i[1])

if __name__ == '__main__':
    dict1 = {
        "value"     : 1,
        "Value_2"   : 9,
        "Value_3"   : 4
    }
    startpy(dict1)
