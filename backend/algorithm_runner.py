def build_heap_steps(arr):
    """针对每种算法单独设计算法步骤拆解逻辑 [cite: 49]"""
    steps = []
    current_arr = arr.copy()
    
    # 此处编写堆的创建过程拆解逻辑，记录比较、交换等标准化信息 [cite: 27]
    # ...
    
    steps.append({
        "step_id": 1,
        "algorithm": "heap_build",
        "description": "初始数组状态",
        "array": current_arr,
        "current_node": None,
        "compare_node": None,
        "swap": False
    })
    return steps