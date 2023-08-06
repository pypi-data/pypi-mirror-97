from ppps.res import glob as g


def find(array, target):
    for i in range(len(array)):
        if array[i:i + len(target)] == target:
            yield i


def find_str_range(array, start_token="/*", end_token="*/"):
    for s, e in zip(find(array, start_token), find(array, end_token)):
        yield (s, e + len(end_token)), array[s + len(start_token):e]


def find_n_replace(string, *args, **kwargs):
    last_index = 0
    for (s, e), _str in find_str_range(string, *args, **kwargs):
        yield string[last_index:s], _str
        last_index = e
    yield string[last_index:], None


def process_file(input_path, output_path: str = None, *args, **kwargs):
    output_path = input_path + ".c" if output_path is None else output_path

    try:
        with open(input_path, "r") as file:
            read = file.read()

        processed_string = process_string(read, *args, **kwargs)

        with open(output_path, "w+") as file:
            file.write(processed_string)

    except:
        return False
    return True


def process_string(
    string,
    exec_tokens: dict = g.exec_tokens,
    eval_tokens: dict = g.eval_tokens,
    replace_exec: bool = True,
    replace_eval: bool = True,
):
    try:
        if not (exec_tokens["start_token"] and exec_tokens["end_token"]):
            raise Exception
        if not (eval_tokens["start_token"] and eval_tokens["end_token"]):
            raise Exception
    except:
        raise Exception("Exec or eval tokens not valid")

    process_f1 = ""
    for _str, _exec in find_n_replace(string, **exec_tokens):
        process_f1 += _str if replace_exec or _exec is None else (
            _str + exec_tokens["start_token"] + _exec +
            exec_tokens["end_token"])
        if _exec is not None: exec(_exec)

    process_f2 = ""
    for _str, _eval in find_n_replace(process_f1, **eval_tokens):
        process_f2 += _str if replace_eval or _eval is None else (
            _str + eval_tokens["start_token"] + _eval +
            eval_tokens["end_token"])
        if _eval is not None: process_f2 += eval(_eval)

    return process_f2


def delete_extension(path: str):
    return path[:[i for i, j in enumerate(path) if j == "."][-1]]


def change_extension(path: str, extension: str):
    if extension[0] == ".": extension = "." + extension
    return path + extension
