import os
import time

# ---- Beginning of setting ----
b_show_folders = False
b_show_files = True
# ------- End of setting -------

if __name__ == "__main__":
    t = time.strftime("%H_%M_%S", time.localtime())
    f_output = open("output{}.txt".format("_FB_" + t), "w", encoding="UTF-8")
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
