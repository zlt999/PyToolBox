import string
import time

# ---- Beginning of setting ----
#config_ID_list = ["CVK", "RM"]
config_ID_list = ["CVK"]
config_param_list = []

# CVK配置：搜索C_ V_ K_参数
l_begin_str = ["C_", "V_", "K_", "c_", "v_", "k_"]
l_end_str = []
l_body_str = ["_", "[", "]"]
b_contain_uppercase = True
b_contain_lowercase = True
b_contain_numbers = True
min_len = 3
config_param_list.append([l_begin_str, l_end_str, l_body_str, b_contain_uppercase, b_contain_lowercase, b_contain_numbers, min_len])

# RM配置：搜索JIRA RM ticket号
l_begin_str = ["RM-"]
l_end_str = []
l_body_str = []
b_contain_uppercase = True
b_contain_lowercase = False
b_contain_numbers = True
min_len = 4
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
    for i in range(len(config_ID_list)):
        try:
            f_input = open("input.txt", "r",encoding="UTF-8")
        except:
            input("请在当前目录创建文件input.txt，将需要搜索的内容复制到其中，保存后重新运行此脚本")
        else:
            l_begin_str, l_end_str, l_body_str, b_contain_uppercase, b_contain_lowercase, b_contain_numbers, min_len = config_param_list[i]

            num = [str(i) for i in range(10)]
            word = ""
            word_list = set()
            t = time.strftime("%H_%M_%S", time.localtime())
            f_output = open("Output{}.txt".format("_WS_{}_{}".format(config_ID_list[i],t)), "w", encoding="UTF-8")

            for line_raw in f_input.readlines():
                line = line_raw
                found = False
                step = 1
                while line != "":
                    if found:
                        body_match_result = MatchBody(line,l_body_str)
                        end_match_result = MatchEnd(line,l_end_str)
                        if end_match_result is not None:
                            word, word_list, found, line = Process("Add&Push", word, word_list, found, line, end_match_result, min_len)
                        elif body_match_result is not None:
                            word, word_list, found, line = Process("Add", word, word_list, found, line, body_match_result, min_len)
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
                                word, word_list, found, line = Process("Add", word, word_list, found, line, line[0], min_len)
                            else:
                                word, word_list, found, line = Process("Push", word, word_list, found, line, line[0], min_len)
                    else:
                        begin_match_result = MatchBegin(line,l_begin_str)
                        if begin_match_result is not None:
                            word, word_list, found, line = Process("Found", word, word_list, found, line, begin_match_result, min_len)
                        else:
                            word, word_list, found, line = Process("Nothing", word, word_list, found, line, line[0], min_len)

            word_list = sorted(word_list)
            for word in word_list:
                f_output.write(word+"\n")
            f_output.close()
            f_input.close()
