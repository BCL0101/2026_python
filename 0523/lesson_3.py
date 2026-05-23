#猜數字遊戲 1~10
import random   # random是內建的module, package

secret_number = random.randint(1, 10)
#print(secret_number) <<< 這是作弊用, 先傳出答案

count = 0

while True: # 無限迴圈
    guess = int(input("請猜一個1到10的數字: "))
    count += 1

    if guess == secret_number:
        print("猜對了!")
        print(f"你總共猜了{count}次")
        break # 跳出迴圈
    elif guess < secret_number:
        print("太小了!")
    else:
        print("太大了!")
        
print("遊戲結束")