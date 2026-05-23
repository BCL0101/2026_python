import random

secret_number = random.randint(1, 10)
# print(secret_number) # 作弊通道

min_val = 1
max_val = 10
count = 0

print("歡迎參加動態區間猜數字遊戲!")

while True:
    guess = int(input(f"請猜一個 {min_val} 到 {max_val} 的數字: "))
    count += 1

    if guess == secret_number:
        # 🎯 在這裡加上 secret_number，明確告訴玩家答案是多少！
        print(f"\n🎉 猜對了！正確答案就是 【{secret_number}】！")
        print(f"👉 你總共猜了 {count} 次")
        break
        
    elif guess < secret_number:
        min_val = guess
        print(f"提示：不對喔，請在 {min_val}~{max_val} 之間再猜一次！")
        
    else:
        max_val = guess
        print(f"提示：不對喔，請在 {min_val}~{max_val} 之間再猜一次！")

print("\n遊戲結束，感謝遊玩！")