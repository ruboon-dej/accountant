  
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)
from calculate import calculate

ASK_FOR_FUNCTION = "รับ หรือ จ่าย"
ASK_FOR_NUMBER = "จำนวนเงิน"
ASK_FOR_RESPONSE = "ต้องการลบข้อมูลเก่าทิ้งหรือไม่ ปัจจุบันคุณมีเงิน "

class User:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.ask = None
        self.function = None
        self.number = None
        self.total = 0

    def reset_every_time(self):
        self.ask = None
        self.function = None
        self.number = None

    def reset_by_user(self):
        self.total = 0

    def get_response(self, text):
        if self.ask is None:
            if text == "ใช่":
                self.reset_by_user()
                self.ask = "Okay"
                return TextSendMessage(text="เรียบร้อย ปัจจุบันคุณมีเงิน 0 บาท " + ASK_FOR_FUNCTION)
            elif text == "ไม่":
                self.ask = "Okay"
                return TextSendMessage(text="รับทราบ " + ASK_FOR_FUNCTION)
            else:
                Response = ""
                Response += ASK_FOR_RESPONSE + str(self.total) + " บาท"
                FIRST_PROMPT = TextSendMessage(text="ok",
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="ใช่", text="ใช่")),
                        QuickReplyButton(action=MessageAction(label="ไม่", text="ไม่")),
                    ]))
                return FIRST_PROMPT
            
        elif self.function is None:
            if text == "รับ":
                self.function = text
                return TextSendMessage(text=ASK_FOR_NUMBER)
            elif text == "จ่าย":
                self.function = text
                return TextSendMessage(text=ASK_FOR_NUMBER)
            else:
                return TextSendMessage(text=ASK_FOR_FUNCTION)

        elif self.number is None:
            if text.isdigit() == True:
                self.number = float(text)
                answer = self.calculate_answer()
                self.total = answer
                response = "ปัจจุบันคุณมีเงิน " + str(answer) + " บาท"
                self.reset_every_time()
                return TextSendMessage(text=response)                
            else:
                return TextSendMessage(text=ASK_FOR_NUMBER)



    def calculate_answer(self):
        return TextSendMessage(text=calculate(self.total, self.function, self.number))