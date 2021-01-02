import os
import time

# ---- Beginning of setting ----
b_show_folders = False
b_show_files = True
# ------- End of setting -------

if __name__ == "__main__":
    t = time.strftime("%H_%M_%S", time.localtime())
    f_output = open("Output_MP_{}.txt".format(t), "w", encoding="UTF-8")
    path_root = os.getcwd()

    for root, dirs, files in os.walk(path_root):
        if b_show_files:
            for file in files:
                if file != os.path.basename(__file__):
                    # Output modify date
                    modif_date = time.localtime(os.stat(os.path.join(root, file)).st_mtime)
                    f_output.write(time.strftime("%Y-%m-%d %H:%M:%S", modif_date) + "\t")
                    # Output suffix
                    a, suffix = os.path.splitext(file)
                    f_output.write(suffix[1:]+"\t")
                    # Output path
                    path = os.path.join(root, file)
                    f_output.write(path[len(path_root):] + "\t")
                    # Output file name
                    f_output.write(os.path.basename(file) + "\n")
        if b_show_folders:
            for dir in dirs:
                path = os.path.join(root, dir)
                f_output.write(path[len(path_root):] + "\n")

    f_output.close()

    try:
        import openpyxl
        f_input = open("Output_MP_{}.txt".format(t),"r",encoding="UTF-8")
        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(["修改时间","文件格式","文件相对地址","文件名"])
        for line in ws["A1":"F1"]:
            for cell in line:
                cell.font = openpyxl.styles.Font(size="16",bold="True")
        for line in f_input.readlines():
            ws.append(line.split("\t"))

        wb.save("Output_MP_{}.xlsx".format(t))
        wb.close()
        f_input.close()
        print("搜索完成，已生成文件："+"\n- Output_MP_{}.xlsx".format(t)+"\n- Output_MP_{}.txt".format(t))
    except ModuleNotFoundError:
        print("搜索完成，已生成文件：" "\n- Output_MP_{}.txt".format(t))
        print("\n若要导出为表格，可下载openpyxl库")

    input("\n<< 程序已结束，按任意键退出 >>")
