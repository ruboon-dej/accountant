def calculate(total,function,number):
    if function ==  "รับ":
        total += number
    elif function == "จ่าย":
        if number <= 0:
            raise Exception("Number cannot be lower than 0")
        else:
            total -= number
    else:
        raise Exception("Invalid Input")
    return total