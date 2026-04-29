# backend/algorithm_runner.py

def build_heap_steps(arr):
    """
    堆创建（最大堆）的步骤拆解逻辑
    接收前端传入的原始数组，返回标准化的分步数据列表
    """
    steps = []
    current_arr = arr.copy()
    step_id = 1

    def record_step(desc, current=None, compare=None, swap=False):
        """内部辅助函数：记录每一步的状态"""
        nonlocal step_id
        steps.append({
            "step_id": step_id,
            "algorithm": "heap_build",
            "description": desc,
            "array": current_arr.copy(), # 必须用 copy，否则所有步骤都会指向最终数组
            "current_node": current,
            "compare_node": compare,
            "swap": swap
        })
        step_id += 1

    n = len(current_arr)
    record_step("初始数组状态，准备开始从底向上构建堆")

    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        record_step(f"当前关注节点：索引 {i} (值: {current_arr[i]})", current=i)

        if l < n:
            record_step(f"与左子节点比较：索引 {l} (值: {current_arr[l]})", current=largest, compare=l)
            if current_arr[l] > current_arr[largest]:
                largest = l

        if r < n:
            record_step(f"与右子节点比较：索引 {r} (值: {current_arr[r]})", current=largest, compare=r)
            if current_arr[r] > current_arr[largest]:
                largest = r

        if largest != i:
            record_step(f"发现更大子节点，准备交换索引 {i} 和 {largest}", current=i, compare=largest, swap=True)
            # 执行交换
            current_arr[i], current_arr[largest] = current_arr[largest], current_arr[i]
            record_step(f"交换完成", current=largest, compare=i)
            
            # 递归向下调整
            record_step(f"继续向下检查受影响的子树 (以索引 {largest} 为根)", current=largest)
            heapify(n, largest)
        else:
            record_step(f"节点 {i} 已经符合最大堆性质，无需交换", current=i)

    # 从最后一个非叶子节点开始构建堆
    for i in range(n // 2 - 1, -1, -1):
        record_step(f"--- 开始调整以索引 {i} 为根的子树 ---")
        heapify(n, i)
        
    record_step("堆创建全部完成！")
    return steps
# backend/algorithm_runner.py
# (保留原有的 build_heap_steps 函数，并在文件最下方添加以下代码)

def build_quick_sort_steps(arr):
    """
    扩展功能：快速排序步骤拆解
    """
    steps = []
    current_arr = arr.copy()
    step_id = 1

    def record_step(desc, current=None, compare=None, swap=False, pivot=None):
        nonlocal step_id
        steps.append({
            "step_id": step_id,
            "algorithm": "quick_sort",
            "description": desc,
            "array": current_arr.copy(),
            "current_node": current,
            "compare_node": compare,
            "swap": swap,
            "pivot_node": pivot # 快排专属：基准值标记
        })
        step_id += 1

    def quick_sort(low, high):
        if low < high:
            record_step(f"开始对索引 [{low} ~ {high}] 进行分区", pivot=high)
            pivot_idx = partition(low, high)
            quick_sort(low, pivot_idx - 1)
            quick_sort(pivot_idx + 1, high)

    def partition(low, high):
        pivot_val = current_arr[high]
        record_step(f"选择索引 {high} (值:{pivot_val}) 作为基准", pivot=high)
        i = low - 1
        for j in range(low, high):
            record_step(f"比较索引 {j} 与基准值", current=j, compare=high, pivot=high)
            if current_arr[j] < pivot_val:
                i += 1
                if i != j:
                    record_step(f"发现较小值，交换索引 {i} 和 {j}", current=i, compare=j, swap=True, pivot=high)
                    current_arr[i], current_arr[j] = current_arr[j], current_arr[i]
                    record_step("交换完成", current=j, compare=i, pivot=high)
        
        record_step(f"分区结束，将基准值放入正确位置 {i+1}", current=i+1, compare=high, swap=True, pivot=high)
        current_arr[i + 1], current_arr[high] = current_arr[high], current_arr[i + 1]
        return i + 1

    record_step("初始数组状态，准备快速排序")
    quick_sort(0, len(current_arr) - 1)
    record_step("快速排序全部完成！")
    return steps
# backend/algorithm_runner.py (保留上面的堆和快排，在下面追加)

def build_bubble_sort_steps(arr):
    """新增扩展算法 1：冒泡排序"""
    steps = []
    current_arr = arr.copy()
    step_id = 1
    n = len(current_arr)

    def record_step(desc, curr=None, comp=None, swap=False):
        nonlocal step_id
        steps.append({
            "step_id": step_id, "algorithm": "bubble_sort", "description": desc,
            "array": current_arr.copy(), "current_node": curr, "compare_node": comp,
            "swap": swap, "pivot_node": None
        })
        step_id += 1

    record_step("初始数组，准备冒泡排序")
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            record_step(f"比较索引 {j} 和 {j+1}", curr=j, comp=j+1)
            if current_arr[j] > current_arr[j + 1]:
                record_step(f"前一个比后一个大，准备交换", curr=j, comp=j+1, swap=True)
                current_arr[j], current_arr[j + 1] = current_arr[j + 1], current_arr[j]
                record_step("交换完成", curr=j+1, comp=j)
                swapped = True
        record_step(f"第 {i+1} 轮结束，末尾元素已归位")
        if not swapped:
            record_step("本轮无交换，数组已有序，提前结束")
            break
            
    record_step("冒泡排序全部完成！")
    return steps

def build_tree_steps(arr):
    """新增扩展算法 2：二叉树前序遍历 (以数组模拟二叉树)"""
    steps = []
    step_id = 1
    visited = [] # 记录已访问的节点

    def record_step(desc, curr=None):
        nonlocal step_id
        steps.append({
            "step_id": step_id, "algorithm": "binary_tree", "description": desc,
            "array": arr.copy(), "current_node": curr, "compare_node": None,
            "swap": False, "pivot_node": None, "visited": visited.copy() # 新增 visited 字段
        })
        step_id += 1

    def preorder(idx):
        if idx >= len(arr): return
        
        record_step(f"抵达节点索引 {idx} (值: {arr[idx]})", curr=idx)
        visited.append(idx)
        record_step(f"【访问】记录节点 {arr[idx]} 到结果中", curr=idx)

        left_idx = 2 * idx + 1
        if left_idx < len(arr):
            record_step(f"准备前往节点 {arr[idx]} 的左子树", curr=left_idx)
            preorder(left_idx)

        right_idx = 2 * idx + 2
        if right_idx < len(arr):
            record_step(f"准备前往节点 {arr[idx]} 的右子树", curr=right_idx)
            preorder(right_idx)

    record_step("初始二叉树(数组存储格式)，开始前序遍历 (根->左->右)")
    preorder(0)
    record_step("二叉树前序遍历完成！")
    return steps