#!/bin/bash

# 后端服务启动脚本

echo "正在启动社交电商团购后端服务..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "建议在虚拟环境中运行，是否继续？(y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "退出启动"
        exit 1
    fi
fi

# 安装依赖
echo "安装Python依赖包..."
pip install -r requirements.txt

# 设置环境变量
export FLASK_ENV=development
export FLASK_APP=run.py

# 初始化数据库和测试数据
echo "初始化数据库..."
python init_data.py

# 启动服务
echo "启动Flask服务..."
echo "访问地址: http://localhost:5000"
echo "API文档: http://localhost:5000/grouppurchase/"
echo "按 Ctrl+C 停止服务"

python run.py