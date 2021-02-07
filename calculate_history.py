def calculate_history(history,action,function,number):
    if function == "รับ":
        history += str(function) + " " + str(action) + " +" + str(number) + " บาท" + "\n"
        return history
    elif function == "จ่าย":
        history += str(function) + " " + str(action) + " -" + str(number) + " บาท" + "\n"
        return history