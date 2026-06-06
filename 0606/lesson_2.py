n = 0    # n放在這是全域變數

def main():   # 自定義function
    #n = 10   # n放在這裡是區域變數
    print("這裡是main function的命名空間")   #function的程式區塊是命名空間
    print(n)   # n放在這是文件變數
    
if __name__ == '__main__':
    main()   # main()是整個專案的執行起點
