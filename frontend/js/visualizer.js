/**
 * 根据完全二叉树的索引计算坐标
 * @param {number} i - 节点的索引 (0, 1, 2...)
 * @returns {object} {x, y} 坐标
 */
function getTreeCoords(i) {
    const containerWidth = 900; // 对应容器宽度
    const rowHeight = 80;       // 每层的高度间距
    
    // 计算当前在第几层 (0, 1, 2, 3...)
    const level = Math.floor(Math.log2(i + 1));
    // 计算当前层总共有多少个节点位置 (1, 2, 4, 8...)
    const nodesInLevel = Math.pow(2, level);
    // 计算当前节点是该层中的第几个 (0, 1, 2...)
    const posInLevel = i - (Math.pow(2, level) - 1);
    
    // 计算 X：将容器宽度平分，节点居中
    const x = (posInLevel + 0.5) * (containerWidth / nodesInLevel);
    // 计算 Y：层级乘以层高
    const y = level * rowHeight + 40;
    
    return { x, y };
}

/**
 * 辅助函数：专门绘制 SVG 线段
 */
function drawLine(svg, p1, p2) {
    const ns = "http://www.w3.org/2000/svg";
    const line = document.createElementNS(ns, "line");
    line.setAttribute("x1", p1.x);
    line.setAttribute("y1", p1.y + 22); // 从父节点中心开始
    line.setAttribute("x2", p2.x);
    line.setAttribute("y2", p2.y + 22); // 连向子节点中心
    line.setAttribute("stroke", "#ccc");
    line.setAttribute("stroke-width", "2");
    svg.appendChild(line);
}

/**
 * 核心渲染函数
 */
function render(step, algoType) {
    const vis = document.getElementById('visualizer');
    if (!vis) return;
    vis.innerHTML = ''; // 清空上一帧的内容

    // 根据算法类型创建布局
    if (algoType === 'heap' || algoType === 'binary_tree') {
        // 创建一个新的 SVG 容器用于画线
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.style.position = "absolute";
        svg.style.width = "100%";
        svg.style.height = "100%";
        svg.id = "treeLines";
        vis.appendChild(svg); // 先放线
        
        renderTreeLayout(step, vis, svg);
    } else {
        renderLinearLayout(step, vis);
    }
}

// --- 逻辑 A：树形布局 ---
function renderTreeLayout(step, vis, svg) {
    // 画线
    step.array.forEach((val, i) => {
        const leftIdx = 2 * i + 1;
        const rightIdx = 2 * i + 2;
        const pCoords = getTreeCoords(i);
        
        if (leftIdx < step.array.length) {
            drawLine(svg, pCoords, getTreeCoords(leftIdx));
        }
        if (rightIdx < step.array.length) {
            drawLine(svg, pCoords, getTreeCoords(rightIdx));
        }
    });

    // 画球
    step.array.forEach((val, i) => {
        const coords = getTreeCoords(i);
        createNode(vis, val, i, coords.x - 22, coords.y, step);
    });
}

/// --- 逻辑 B：线性布局 ---
function renderLinearLayout(step, vis) {
    const startX = 50;
    const spacing = 60;
    step.array.forEach((val, i) => {
        const x = startX + i * spacing;
        const y = 150; 
        createNode(vis, val, i, x, y, step);
    });
}

// 通用节点创建
function createNode(vis, val, i, x, y, step) {
    const node = document.createElement('div');
    node.className = 'node';
    node.style.left = `${x}px`;
    node.style.top = `${y}px`;
    node.innerHTML = `<span class="idx">${i}</span>${val}`;

    if (i === step.current_node) node.classList.add('current');
    if (i === step.compare_node) node.classList.add('compare');
    if (i === step.pivot_node) node.classList.add('pivot');
    
    vis.appendChild(node);
}