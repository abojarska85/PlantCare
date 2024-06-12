def humidity_label(humidity_number):
    if humidity_number == 1:
        return 'długo utrzymulące wilgość'
    elif humidity_number == 2:
        return 'przepuszczalne'
    elif humidity_number == 3:
        return 'wysoko przepuszczalne'


def light_label(light_number):
    if light_number == 1:
        return 'bardzo jasne'
    elif light_number == 2:
        return 'jasne, światło rozproszone'
    elif light_number == 3:
        return 'półcieniste'
    elif light_number == 4:
        return 'cieniste'
