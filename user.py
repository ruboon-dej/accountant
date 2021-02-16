from linebot.models import (MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction)
from calculate import calculate
from calculate_history import calculate_history
import re
from models import AccountMovement
from server import db

ASK_FOR_FUNCTION = "รับ หรือ จ่าย"
ASK_FOR_NUMBER = "จำนวนเงิน"
ASK_FOR_RESPONSE = "ต้องการลบข้อมูลเก่าทิ้งหรือไม่ ปัจจุบันคุณมีเงิน "

FIRST_PROMPT = TextSendMessage(text="ok",
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="ใช่", text="ใช่")),
        QuickReplyButton(action=MessageAction(label="ไม่", text="ไม่")),
    ]))

def isdigit(text):
    return re.match("^\d+(\.\d+)?$", text) is not None

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.reset()
    
    def reset(self):
        self.first = None
        self.ask = None
        self.function = None
        self.number = None
        self.history = "B"
        self.total = 0
        self.last = None
        self.action = None

    def reset_every_time(self):
        self.first = None
        self.ask = None
        self.function = None
        self.number = None
        self.last = None
        self.action = None

    def reset_by_user(self):
        self.total = 0
        self.history = "B"

    def get_response_2(self, text):
        if self.history == "B":
            self.reset()
            return TextSendMessage(text="ปัจจุบันคุณยังไม่มีประวัติการบันทึกรายรับ รายจ่าย")
        else:
            result_1 = self.history
            self.reset_every_time()
            return TextSendMessage(text=result_1[1:-1])
           
    def history_test(self,text):
        accounts = AccountMovement.query.all()
        for account in accounts:
            action = account.action
            action += action
        return TextSendMessage(text=action)

    def get_response_1(self, text):            
        if self.function is None:
            if text == "รับ":
                self.function = text
                return TextSendMessage(text=ASK_FOR_NUMBER)
            elif text == "จ่าย":
                self.function = text
                return TextSendMessage(text=ASK_FOR_NUMBER)
            elif text == "ยกเลิก":
                self.reset_every_time()
                return TextSendMessage(text="okay")                
            else:
                SECOND_PROMPT = TextSendMessage(text=ASK_FOR_FUNCTION,
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="รับ", text="รับ")),
                        QuickReplyButton(action=MessageAction(label="จ่าย", text="จ่าย")),
                        QuickReplyButton(action=MessageAction(label="ยกเลิก", text="ยกเลิก"))
                    ]))
                return SECOND_PROMPT

        elif self.number is None:
            if isdigit(text) == True:
                self.number = float(text)
                return TextSendMessage(text="กรุณาบอกการกระทำที่เกี่ยวกับรายรับ หรือรายจ่ายนี้")                
            else:
                return TextSendMessage(text=ASK_FOR_NUMBER)

        elif self.last is None:
            if self.action is None:
                response = ""
                try:
                    answer = self.calculate_answer()
                    self.total = answer
                    response = "ปัจจุบันคุณมีเงิน " + str(answer) + " บาท"
                    self.last = "Done"
                    self.action = text
                    self.history = self.calculate_history()
                    self.reset_every_time()
                except Exception as e:
                    response = e.args[0]
                    self.last = "Done"
                    self.action = text
                    self.reset_every_time()
                return TextSendMessage(text=response)
            else:
                response = ""
                try:
                    answer = self.calculate_answer()
                    self.total = answer
                    response = "ปัจจุบันคุณมีเงิน " + str(answer) + " บาท"
                    self.last = "Done"
                    self.action = text
                    self.history = self.calculate_history()
                    self.reset_every_time()                    
                except Exception as e:
                    response = e.args[0]
                    self.last = "Done"
                    self.action = text
                    self.reset_every_time()
                return TextSendMessage(text=response)
    
    def calculate_answer(self):
        return calculate(self.total, self.function, self.number)

    def calculate_history(self):
        amount = -self.number if self.function == "จ่าย" else self.number
        db.session.add(AccountMovement(user_id=self.user_id, action=self.action, amount=amount))
        db.session.commit()
        return calculate_history(self.history, self.action, self.function, self.number)

    def get_result(self, text):
        if self.first is None:
            if text == "ประวัติ":
                self.first = "ประวัติ"
                return self.get_response_2(text)
            elif text == "รายรับรายจ่าย":
                self.first = "รายรับรายจ่าย"
                return self.get_response_1(text)
            elif text == "คงเหลือ":
                yes = "ปัจจุบันคุณมีเงินคงเหลือ " + str(self.total) + " บาท"
                return TextSendMessage(text=yes)
            elif text == "ลบ":
                self.reset_by_user()
                eyes = "ปัจจุบันคุณมีเงินคงเหลือ " + str(self.total) + " บาท"
                return TextSendMessage(text=eyes)
            elif text == "Test":
                return self.history_test(text)

            else:
                THIRD_PROMPT = TextSendMessage(text="คุณต้องการทำรายการอะไร",
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="ประวัติรายรับรายจ่าย", text="ประวัติ")),
                        QuickReplyButton(action=MessageAction(label="รายรับรายจ่าย", text="รายรับรายจ่าย")),
                        QuickReplyButton(action=MessageAction(label="เงินคงเหลือ", text="คงเหลือ")),
                        QuickReplyButton(action=MessageAction(label="ลบข้อมูลรายรับรายจ่าย", text="ลบ")),
                        QuickReplyButton(action=MessageAction(label="Test", text="Test"))
                    ]))
                return THIRD_PROMPT
        else:
            if self.first == "ประวัติ":
                return self.get_response_2(text)
            elif self.first == "รายรับรายจ่าย":
                return self.get_response_1(text)
            elif text == "คงเหลือ":
                yes = "ปัจจุบันคุณมีเงินคงเหลือ " + str(self.total) + " บาท"
                return TextSendMessage(text=yes)
            elif text == "Test":
                return self.history_test(text)