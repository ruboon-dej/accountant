def calculate(total,function,number)
    if function ==  "รับ":
        total += number
    elif function == "จ่าย":
        total -= number
    else:
        total = "an error has occured please try again."
    return total