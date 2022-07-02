
def is_list(element) -> bool:
    if(isinstance(element,list)):
        return True
    return False

def sum_in_list(element):
    if(isinstance(element,list)):
        sum = 0
        for num in element:
            sum += int(num)
        return sum
    else:
        return element