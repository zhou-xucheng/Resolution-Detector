import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import analyzer
import pandas as pd

class ResolutionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("产线解析力自动检测工具 v1.0")
        self.root.geometry("1024x768")
        
        self.image_files = []
        self.results = []
        self.threshold_var = tk.DoubleVar(value=50.0)
        
        self.create_widgets()
    
    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="合格阈值 (LW/PH):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(top_frame, textvariable=self.threshold_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="选择图片", command=self.select_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="导出报表", command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        ttk.Label(left_frame, text="图片列表", font=('Arial', 12, 'bold')).pack(pady=5)
        self.image_listbox = tk.Listbox(left_frame, width=40, height=30)
        self.image_listbox.pack(fill=tk.BOTH, expand=True)
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="检测结果", font=('Arial', 12, 'bold')).pack(pady=5)
        
        columns = ("文件名", "解析力 (LW/PH)", "对比度", "是否合格")
        self.result_tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150)
        self.result_tree.pack(fill=tk.BOTH, expand=True)
        
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[("图片文件", "*.jpg;*.jpeg;*.png")]
        )
        
        if files:
            self.image_files = list(files)
            self.image_listbox.delete(0, tk.END)
            for f in self.image_files:
                self.image_listbox.insert(tk.END, os.path.basename(f))
            
            self.analyze_all_images()
    
    def analyze_all_images(self):
        self.results = []
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.status_bar.config(text="正在分析图片...")
        self.root.update_idletasks()
        
        for filepath in self.image_files:
            try:
                res, contrast = analyzer.calculate_resolution(filepath)
                filename = os.path.basename(filepath)
                threshold = self.threshold_var.get()
                is_pass = "合格" if res >= threshold else "不合格"
                
                self.results.append({
                    "文件名": filename,
                    "解析力 (LW/PH)": res,
                    "对比度": contrast,
                    "是否合格": is_pass
                })
                
                self.result_tree.insert("", tk.END, values=(filename, f"{res:.2f}", f"{contrast:.2f}", is_pass))
            except Exception as e:
                messagebox.showerror("错误", f"处理 {filepath} 时出错: {str(e)}")
        
        self.status_bar.config(text=f"分析完成，共 {len(self.results)} 张图片")
    
    def on_image_select(self, event):
        pass
    
    def export_results(self):
        if not self.results:
            messagebox.showwarning("警告", "没有检测结果可导出")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        
        if filepath:
            df = pd.DataFrame(self.results)
            df.to_excel(filepath, index=False)
            messagebox.showinfo("成功", f"报表已导出到 {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResolutionAnalyzerApp(root)
    root.mainloop()