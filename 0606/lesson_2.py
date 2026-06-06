# n = 0    # n在這是全域變數
def main():   # 自定義function
    n = 10   # n在這裡是區域變數
    print("這裡是main function的命名空間")   #function的程式區塊是命名空間
    print(n)   # n在這是文件變數
    
if __name__ == '__main__':
    main()   # 整個專案的執行起點
    print(n)