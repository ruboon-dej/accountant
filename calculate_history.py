def calculate_history(history,action,function,number):
    if below == "Number cannot be lower than 0":
        pass
    else:
        if function == "รับ":
            history += str(function) + " " + str(action) + " +" + str(number) + " บาท" + "\n"
            return history
        elif function == "จ่าย":
            history += str(function) + " " + str(action) + " -" + str(number) + " บาท" + "\n"
            return history