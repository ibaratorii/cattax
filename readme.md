# CatTax - 猫咪行为分析系统

基于计算机视觉的猫咪行为分析系统，可以实时检测和分析视频中猫咪的行为状态。

## 功能特点

- 实时猫咪检测和追踪
- 行为状态分析（行走、休息、站立等）
- 多猫同时分析
- 实时可视化结果

## 系统要求

- Python 3.8+
- Node.js 14+
- Redis 服务器
- CUDA (可选，用于GPU加速)

## 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/ibaratorii/cattax.git
   cd cattax

2. 创建并激活 Python 虚拟环境
   
   Windows
   ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    Linux/Mac
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 安装前端依赖
   ```bash
   cd frontend
   npm install
   ```

5. 配置环境变量
   ```bash
   复制环境变量示例文件
   cp .env.example .env

   根据需要编辑 .env 文件
   ```

6. 初始化数据库
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   

## 启动服务

需要启动三个终端：

### 终端 1: Redis 服务器    
```bash
redis-server
```

### 终端 2: celery worker

```bash
激活虚拟环境后
celery -A cattax worker -l info
```

### 终端 3: django服务器    

```bash
python manage.py runserver
```

### 终端 4: 前端开发服务器

```bash
cd frontend
npm run serve
```
## 使用说明

1. 访问 http://localhost:8080
2. 上传猫咪视频文件
3. 等待系统分析（分析时间取决于视频长度）
4. 查看分析结果
### 模型文件

YOLO 模型文件 `yolo11x-seg.pt` 需要单独下载：
1. 下载地址：[链接]
2. 将文件放在项目根目录

## 项目结构

- cattax/
  - api/ # Django API 应用
  - cattax/ # 主项目目录
    - cat_capture.py # 猫咪检测模块
    - cat_behavior.py # 行为分析模块
  - frontend/ # Vue.js 前端应用
  - manage.py # Django 管理脚本
  - requirements.txt # 依赖包列表
  - .env.example # 环境变量示例文件
  
## 许可证

MIT License