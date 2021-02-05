from calculate import calculate

ASK_FOR_FUNCTION = "รับ หรือ จ่าย"
ASK_FOR_NUMBER = "จำนวนเงิน"
ASK_FOR_RESPONSE = "ต้องการลบข้อมูลเก่าทิ้งหรือไม่ ปัจจุบันคุุณมีเงิน"

class User:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.ask = None
        self.function = None
        self.number = None
        self.total = None

    def reset_every_time(self):
        self.ask = None
        self.function = None
        self.number = None

    def reset_by_user(self):
        self.total = None
        self.total = 0

    def get_response(self, text):
        if self.ask is None:
            print ("first")
            if text == "ใช่":
                self.reset_by_user()
                return "Done"
            elif text == "ไม่":
                self.ask = "Okay"
                return "Okay"
            else:
                Response = ""
                Response += ASK_FOR_RESPONSE + self.total
                return Response
            
        elif self.function is None:
            if text == "รับ":
                self.function = text
                return ASK_FOR_NUMBER
            elif text == "จ่าย":
                self.function = text
                return ASK_FOR_NUMBER
            else:
                return ASK_FOR_FUNCTION

        elif self.number is None:
            if text.isdigit() == True:
                self.number = float(text)
                answer = self.calculate_answer()
                self.total = answer
                self.reset_every_time
            else:
                return ASK_FOR_NUMBER

    def calculate_answer(self):
        return calculate(self.total, self.function, self.number)