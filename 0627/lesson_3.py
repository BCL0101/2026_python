import tkinter as tk
from tkinter import ttk
from pathlib import Path
import pandas as pd

def load_and_process_data():
    base_dir = Path(__file__).parent
    csv_path = base_dir / '各鄉鎮市區人口密度.csv'
    df = pd.read_csv(csv_path, header=0)

    df = df.iloc[1:].copy()
    df = df.iloc[:-5].copy()

    df = df[['site_id', 'people_total', 'area']]
    df.columns = ['區域別', '人口數', '土地面積']

    df['人口數'] = pd.to_numeric(df['人口數'], errors='coerce')
    df['土地面積'] = pd.to_numeric(df['土地面積'], errors='coerce')
    df = df.dropna(subset=['人口數', '土地面積'])

    df['人口密度'] = df['人口數'] / df['土地面積']
    return df

def update_table(tree, df, keyword=''):
    for row in tree.get_children():
        tree.delete(row)

    if keyword:
        filtered_df = df[df['區域別'].str.contains(keyword, na=False)]
    else:
        filtered_df = df

    for _, row in filtered_df.iterrows():
        tree.insert('', tk.END, values=(
            row['區域別'],
            int(row['人口數']),
            round(row['土地面積'], 4),
            round(row['人口密度'], 2),
        ))

def main():
    df = load_and_process_data()

    root = tk.Tk()
    root.title('台灣鄉鎮市區人口密度查詢系統')
    root.geometry('900x600')

    control_frame = ttk.Frame(root, padding=10)
    control_frame.pack(fill=tk.X)

    label = ttk.Label(control_frame, text='輸入區域名稱：')
    label.pack(side=tk.LEFT, padx=(0, 5))

    entry = ttk.Entry(control_frame, width=30)
    entry.pack(side=tk.LEFT, padx=(0, 5))

    tree_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('區域別', '人口數', '土地面積', '人口密度')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor='center')

    v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    tree.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    def on_query():
        update_table(tree, df, entry.get())

    btn = ttk.Button(control_frame, text='查詢', command=on_query)
    btn.pack(side=tk.LEFT)

    update_table(tree, df)
    root.mainloop()

if __name__ == '__main__':
    main()
