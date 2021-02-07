from calculate import calculate

try:
    calculate(0, "จ่าย", -1)
    print("success")
except Exception as e:
    print(e.args[0])
print("hi")