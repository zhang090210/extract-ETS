from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from structures import ETS

ets = ETS()

root = Tk()
root.title("Extract ETS")
root.geometry("450x200")
# root.resizable(False, False)
# 设置创建位置
root.geometry("+300+300")

# create a label widget
prompt = Label(root, text="Home Work: ")
prompt.grid(row=0, column=0, padx=10, pady=10)

homework_list = Label(root, text=ets.get_homework_list().Name)
homework_list.grid(row=0, column=1)

warn = Label(root, text="如果不是本周作业，请点击‘班级作业’->‘待完成’->‘作业名称’之后点击刷新按钮")
warn.grid(row=2, column=0, columnspan=2)

refresh_button = ttk.Button(root, text="刷新", command=lambda: homework_list.config(text=ets.get_homework_list().Name))
refresh_button.grid(row=3, column=0, padx=10, pady=10)

export_button = ttk.Button(root, text="导出pdf",
                           command=lambda: ets.export_to_pdf(
                               ets.parse_homework(ets.get_homework_list()),
                               filedialog.asksaveasfilename(initialfile=f"{ets.get_homework_list().Name}.pdf", defaultextension=".pdf", initialdir=".", title="保存文件", filetypes=(("pdf文件", "*.pdf"), ("所有文件", "*.*")))
                           ))
export_button.grid(row=3, column=1, padx=10, pady=10)

# start the GUI
root.mainloop()