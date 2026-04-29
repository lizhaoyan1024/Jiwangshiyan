def validate_input(data_str):
    """针对不同算法的输入要求，实现输入数据的合法性检查 [cite: 46]"""
    try:
        if not data_str:
            return False, "输入不能为空", None
        arr = [int(x.strip()) for x in data_str.split(',')]
        if len(arr) != 9:
            return False, "请输入9个整数", None
        return True, "校验成功", arr
    except ValueError:
        return False, "输入包含非整数，请检查", None