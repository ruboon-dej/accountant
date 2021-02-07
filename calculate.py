def calculate(total,function,number):
    if function ==  "รับ":
        total += number
    elif function == "จ่าย":
        total -= number
        if total <= 0:
            raise Exception("เงินคุณน้อยกว่า 0 บาทไม่ได้")
    else:
        raise Exception("Invalid Input")
    return total