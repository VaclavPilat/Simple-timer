import json, time, random, datetime

data = []

stack = []

time = round(time.time())

count = 5000

for i in range(count, 0, -1):
    time -= random.randrange(100_000)
    if i % 2 == 1:
        ttype = "start"
    else:
        ttype = "stop"
    stack.append({
        "id": i,
        "type": ttype,
        "datetime": datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M:%S')
    })


for i in range(count, 0, -1):
    data.append(stack.pop())

print(json.dumps(data))