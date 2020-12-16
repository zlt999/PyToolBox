import string
import time

# ---- Beginning of setting ----
config_ID_list = []
config_param_list = []

# CVK配置：搜索C_ V_ K_参数
config_ID = "CVK"
l_begin_str = ["C_", "V_", "K_", "c_", "v_", "k_"]
l_end_str = []
l_body_str = ["_", "[", "]"]
b_contain_uppercase = True
b_contain_lowercase = True
b_contain_numbers = True
min_len = 3
config_ID_list.append(config_ID)
config_param_list.append([l_begin_str, l_end_str, l_body_str, b_contain_uppercase, b_contain_lowercase, b_contain_numbers, min_len])

# RM配置：搜索JIRA RM ticket号
config_ID = "RM"
l_begin_str = ["RM-"]
l_end_str = []
l_body_str = []
b_contain_uppercase = True
b_contain_lowercase = False
b_contain_numbers = True
min_len = 4
config_ID_list.append(config_ID)
config_param_list.append([l_begin_str, l_end_str, l_body_str, b_contain_uppercase, b_contain_lowercase, b_contain_numbers, min_len])
# ------- End of setting -------


def MatchBegin(str,l_key):
    for key in l_key:
        if str.startswith(key):
            return key
    return


def MatchEnd(str,l_key):
    for key in l_key:
        if str.startswith(key):
            return key
    return


def MatchBody(str,l_key):
    for key in l_key:
        if str.startswith(key):
            return key
    return


def Process(method_t, word_t, word_list_t, found_t, line_t, key_t, min_len_t):
    if method_t == "Nothing":
        None

    elif method_t == "Add&Push":
        word_t += key_t
        if len(word_t) > min_len_t:
            word_list.add(word_t)
        word_t = ""
        found_t = False

    elif method_t == "Push":
        if len(word_t) > min_len_t:
            word_list.add(word_t)
        word_t = ""
        found_t = False

    elif method_t == "Add":
        word_t += key_t

    elif method_t == "Found":
        found_t = True
        word_t = key_t

    else:
        input("Method error")

    line_t = line_t[len(key_t):]
    return word_t, word_list_t, found_t, line_t

if __name__ == "__main__":
    try:
        # 打开输入文件
        f_input = open("input.txt", "r",encoding="UTF-8")

        # 选择配置
        print("现有配置：", end="")
        for s in config_ID_list:
            print(s, end=" ")
        print("\n")
        config_ID = input("请输入选择的配置：")
        print()

        # 读取配置信息
        ID = config_ID_list.index(config_ID)
        l_begin_str, l_end_str, l_body_str, b_contain_uppercase, b_contain_lowercase, b_contain_numbers, min_len = config_param_list[ID]

        # 打开输出文件
        t = time.strftime("%H_%M_%S", time.localtime())
        f_output = open("Output_WS_{}_{}.txt".format(config_ID, t), "w", encoding="UTF-8")

        # 初始化
        num = [str(i) for i in range(10)]
        word = ""
        word_list = set()

        for line_raw in f_input.readlines():
            line = line_raw
            found = False
            step = 1
            while line != "":
                if found:
                    body_match_result = MatchBody(line, l_body_str)
                    end_match_result = MatchEnd(line, l_end_str)
                    if end_match_result is not None:
                        word, word_list, found, line = Process("Add&Push", word, word_list, found, line,
                                                               end_match_result, min_len)
                    elif body_match_result is not None:
                        word, word_list, found, line = Process("Add", word, word_list, found, line, body_match_result,
                                                               min_len)
                    else:
                        legal = False
                        if line[0] in string.ascii_uppercase:
                            if b_contain_uppercase:
                                legal = True
                        elif line[0] in string.ascii_lowercase:
                            if b_contain_lowercase:
                                legal = True
                        elif line[0] in num:
                            if b_contain_numbers:
                                legal = True
                        if legal:
                            word, word_list, found, line = Process("Add", word, word_list, found, line, line[0],
                                                                   min_len)
                        else:
                            word, word_list, found, line = Process("Push", word, word_list, found, line, line[0],
                                                                   min_len)
                else:
                    begin_match_result = MatchBegin(line, l_begin_str)
                    if begin_match_result is not None:
                        word, word_list, found, line = Process("Found", word, word_list, found, line,
                                                               begin_match_result, min_len)
                    else:
                        word, word_list, found, line = Process("Nothing", word, word_list, found, line, line[0],
                                                               min_len)

        # 输出结果
        word_list = sorted(word_list)
        for word in word_list:
            f_output.write(word + "\n")
        f_output.close()
        f_input.close()

        print("搜索完成，已生成文件："+"Output_WS_{}_{}.txt".format(config_ID, t))
    except FileNotFoundError:
        f = open("input.txt","w")
        f.close()
        print("已创建文件input.txt，请存入需要搜索的内容，然后重新运行此脚本")
    except ValueError:
        print("该配置字不存在")

    print()
    input("<< 程序已结束 >>")
