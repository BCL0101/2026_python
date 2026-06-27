import tkinter as tk
from tkinter import ttk  # ttk 提供更美觀的元件
import pandas as pd       # 使用 pandas 處理資料


def load_and_process_data():
    """讀取 CSV 並進行資料整理，回傳處理後的 DataFrame"""
    # 讀取 CSV，將第一列（statistic_yyy,site_id,...）作為欄位名稱
    df = pd.read_csv('各鄉鎮市區人口密度.csv', header=0)

    # 移除第二列的中文欄位說明列（該列包含「統計年,區域別,年底人口數,土地面積,人口密度」）
    df = df[df['statistic_yyy'] != '統計年']

    # 移除最後 5 筆尾部說明資訊（如「說明：1.人口密度係指...」等非資料內容）
    df = df.iloc[:-5]

    # 僅保留需要的三個欄位，並重新命名為中文名稱
    # site_id → 區域別, people_total → 人口數, area → 土地面積
    df = df[['site_id', 'people_total', 'area']]
    df.columns = ['區域別', '人口數', '土地面積']

    # 將人口數與土地面積轉換為數值型態（無法轉換者設為 NaN）
    df['人口數'] = pd.to_numeric(df['人口數'], errors='coerce')
    df['土地面積'] = pd.to_numeric(df['土地面積'], errors='coerce')

    # 移除含有空值（NaN）的列（如東沙群島、南沙群島等資料不全的列）
    df = df.dropna()

    # 新增人口密度欄位：人口數 / 土地面積
    df['人口密度'] = df['人口數'] / df['土地面積']

    return df


def update_table(tree, df, keyword=''):
    """
    更新 Treeview 表格內容。
    若有關鍵字，則篩選出區域別包含該關鍵字的資料；否則顯示全部。
    """
    # 清除表格中所有現有資料
    for row in tree.get_children():
        tree.delete(row)

    # 根據關鍵字篩選資料
    if keyword:
        filtered_df = df[df['區域別'].str.contains(keyword, na=False)]
    else:
        filtered_df = df

    # 將篩選結果逐筆插入表格
    for _, row in filtered_df.iterrows():
        tree.insert('', tk.END, values=(
            row['區域別'],
            int(row['人口數']),                    # 人口數顯示為整數
            row['土地面積'],
            round(row['人口密度'], 2),             # 人口密度四捨五入至小數點後兩位
        ))


def main():
    """主程式：建立 GUI 應用程式"""
    # ------ 資料處理 ------
    df = load_and_process_data()

    # ------ 建立視窗 ------
    root = tk.Tk()
    root.title('台灣鄉鎮市區人口密度查詢系統')
    root.geometry('900x600')

    # ------ 上方控制區 ------
    control_frame = ttk.Frame(root, padding=10)
    control_frame.pack(fill=tk.X)

    label = ttk.Label(control_frame, text='輸入區域名稱：')
    label.pack(side=tk.LEFT, padx=(0, 5))

    entry = ttk.Entry(control_frame, width=30)
    entry.pack(side=tk.LEFT, padx=(0, 5))

    def on_query():
        """查詢按鈕的回呼函式：讀取輸入框文字並篩選表格"""
        keyword = entry.get()
        update_table(tree, df, keyword)

    btn = ttk.Button(control_frame, text='查詢', command=on_query)
    btn.pack(side=tk.LEFT)

    # ------ 下方表格區 ------
    # 建立 Treeview 表格框架
    tree_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # 定義欄位
    columns = ('區域別', '人口數', '土地面積', '人口密度')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    # 設定每個欄位的標題、寬度與置中對齊
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor='center')

    # 加入垂直與水平捲動軸
    v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    tree.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # 程式啟動時，預設顯示所有資料
    update_table(tree, df)

    # 進入 tkinter 主迴圈
    root.mainloop()


if __name__ == '__main__':
    main()
