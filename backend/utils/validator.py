# backend/utils/validator.py

def validate_input(data_str, algo_type="heap"):
    if not data_str or not data_str.strip():
        return False, "输入不能为空", None
    
    data_str = data_str.replace('，', ',')
    parts = data_str.split(',')
    
    # 根据不同算法放宽或收紧校验规则
    if algo_type == "heap":
        if len(parts) != 9: return False, f"堆创建严格要求 9 个整数，当前 {len(parts)} 个", None
    elif algo_type in ["quick_sort", "bubble_sort", "binary_tree"]:
        if len(parts) < 3 or len(parts) > 15:
            return False, f"该算法建议输入 3~15 个整数，当前 {len(parts)} 个", None
    
    result_arr = []
    for item in parts:
        item = item.strip()
        if not item: return False, "存在多余的逗号", None
        try:
            result_arr.append(int(item))
        except ValueError:
            return False, f"'{item}' 不是有效整数", None
            
    return True, "校验成功", result_arr