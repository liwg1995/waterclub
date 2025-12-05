#!/bin/bash

echo "======================================"
echo "水立方舞蹈工作室管理系统 - 快速启动"
echo "======================================"
echo ""

# 检查Python版本
echo "检查Python环境..."
python3 --version

# 检查是否已创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 检查是否需要安装依赖
if [ ! -f "venv/installed.flag" ]; then
    echo "安装项目依赖（这可能需要几分钟）..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed.flag
    echo "依赖安装完成！"
else
    echo "依赖已安装，跳过安装步骤"
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库密码等信息"
fi

echo ""
echo "======================================"
echo "接下来的步骤："
echo "======================================"
echo "1. 确保MySQL 8.0已安装并运行"
echo "2. 创建数据库: CREATE DATABASE water_cube_db CHARACTER SET utf8mb4;"
echo "3. 编辑 .env 文件配置数据库密码"
echo "4. 运行数据库迁移: python manage.py migrate"
echo "5. 创建管理员: python manage.py createsuperuser"
echo "6. 启动服务器: python manage.py runserver"
echo ""
echo "访问地址："
echo "  - 前台: http://localhost:8000/"
echo "  - 后台: http://localhost:8000/xadmin/"
echo "  - API文档: http://localhost:8000/api/docs/"
echo "======================================"
