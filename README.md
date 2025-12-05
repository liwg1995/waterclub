# 水立方舞蹈工作室管理系统

基于 Python + Django + xadmin + MySQL 8.0 构建的舞蹈工作室综合管理系统，集成宣传展示、学员管理、班级管理、财务管理等功能。

## 技术栈

### 后端技术
- **Python 3.11** - 开发语言
- **Django 4.2** - Web框架
- **Django REST Framework 3.14** - API开发
- **xadmin** - 后台管理界面
- **MySQL 8.0** - 数据库（使用pymysql连接）
- **Redis** - 缓存与会话存储
- **Celery** - 异步任务队列

### 前端技术
- **TailwindCSS** - CSS框架（自适应设计）
- **Alpine.js** - 轻量级JavaScript框架（交互动画）
- **Django Templates** - 模板引擎

### 核心依赖
- djangorestframework-simplejwt - JWT认证
- django-cors-headers - 跨域支持
- django-redis - Redis缓存集成
- Pillow - 图片处理
- django-ckeditor - 富文本编辑器
- django-import-export - 数据导入导出
- python-decouple - 环境配置管理

## 项目结构

```
water_cube_studio/
├── apps/                          # 业务应用
│   ├── users/                     # 用户管理
│   ├── students/                  # 学员管理
│   ├── teachers/                  # 教师管理
│   ├── classes/                   # 班级课程管理
│   ├── finance/                   # 财务管理
│   ├── attendance/                # 考勤管理
│   └── cms/                       # 内容管理（宣传页面）
├── templates/                     # 模板文件
│   ├── base.html                  # 基础模板
│   └── cms/                       # CMS模板
├── static/                        # 静态文件
├── media/                         # 媒体文件
├── water_cube_studio/             # 项目配置
│   ├── settings.py                # 配置文件
│   ├── urls.py                    # 路由配置
│   └── __init__.py                # PyMySQL配置
├── manage.py                      # Django管理脚本
├── requirements.txt               # 依赖列表
├── .env.example                   # 环境配置示例
└── README.md                      # 项目说明
```

## 核心功能模块

### 1. 用户管理（users）
- 自定义用户模型
- 支持多角色（管理员、教务人员、教师、学员）
- JWT认证与会话管理
- 用户扩展信息（积分、会员等级、推荐人）

### 2. 学员管理（students）
- 学员档案管理
- 学籍状态追踪
- 监护人信息
- 课时余额管理
- 健康信息记录

### 3. 教师管理（teachers）
- 教师信息管理
- 擅长舞种与教龄
- 课时费设置
- 教学成果展示

### 4. 班级课程管理（classes）
- 舞种分类管理
- 班型配置（级别、适龄、课时长）
- 课程开班管理
- 教室资源管理
- 排课系统
- 报名管理

### 5. 财务管理（finance）
- 价格策略（次卡、月卡、学期制、按课时）
- 支付记录（微信、支付宝、现金、银行转账）
- 订单管理
- 退款处理

### 6. 考勤管理（attendance）
- 学员签到
- 出勤统计
- 请假管理

### 7. 内容管理（cms）
- 轮播图管理
- 文章资讯（新闻、活动、演出、教学）
- 作品相册
- 联系留言

## 前端特性

### 响应式设计
- 基于TailwindCSS的移动优先设计
- 自适应不同屏幕尺寸（手机、平板、桌面）
- 流畅的导航体验

### 交互动画
- Alpine.js驱动的交互效果
- 渐入动画（fadeIn、scaleIn）
- 悬停效果（hover-lift）
- 页面过渡动画
- 移动端菜单动画

### 视觉设计
- 渐变色彩方案
- 卡片式布局
- 阴影与圆角设计
- 统一的视觉语言

## 安装部署

### 1. 环境要求
- Python 3.11+
- MySQL 8.0
- Redis（可选）

### 2. 创建数据库
```sql
CREATE DATABASE water_cube_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 安装依赖
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 配置环境变量
复制`.env.example`为`.env`，并修改配置：
```bash
cp .env.example .env
# 编辑.env文件，配置数据库密码等信息
```

### 5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员
```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器
```bash
python manage.py runserver
```

访问：
- 前台首页：http://localhost:8000/
- xadmin后台：http://localhost:8000/xadmin/
- API文档：http://localhost:8000/api/docs/

## 三种运行方式

本项目支持三种不同的运行和部署方式，满足开发、测试和生产环境的不同需求。

### 方式一：原生运行模式 (Native)

**适用场景**：本地开发、学习测试

**优点**：
- 直接运行，无需额外工具
- 快速部署，适合开发调试
- 易于理解整个项目流程

**运行步骤**：

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库、Redis 等信息

# 4. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 5. 创建超级管理员
python manage.py createsuperuser

# 6. 收集静态文件（可选）
python manage.py collectstatic --noinput

# 7. 运行开发服务器
python manage.py runserver
```

**访问地址**：
- 前台首页：http://localhost:8000/
- xadmin后台：http://localhost:8000/xadmin/
- API文档：http://localhost:8000/api/docs/

**注意事项**：
- 确保 MySQL 8.0 已安装并运行
- 确保 Redis 已安装（如配置了 USE_REDIS=True）
- 开发环境默认 DEBUG=True，生产环境需改为 False

---

### 方式二：Docker 运行模式

**适用场景**：容器化部署、测试环境、简化部署流程

**优点**：
- 环境一致性好，避免「在我的机器上可以运行」问题
- 自动化部署，快速启动
- 支持 Docker Compose 多容器编排
- 易于在不同服务器上部署

**前置要求**：
- 安装 Docker（推荐 20.10+）
- 安装 Docker Compose（推荐 2.0+）

**快速开始**：

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 使用 Docker Compose 启动服务
docker-compose up -d

# 或仅启用 Redis（如果需要）
docker-compose --profile with-redis up -d

# 或启用 Redis 和 Nginx（完整配置）
docker-compose --profile with-redis --profile with-nginx up -d
```

**查看运行状态**：

```bash
# 查看容器状态
docker-compose ps

# 查看应用日志
docker-compose logs -f web

# 进入容器交互式 Shell
docker-compose exec web bash
```

**访问地址**：
- 前台首页：http://localhost:8000/
- xadmin后台：http://localhost:8000/xadmin/
- API文档：http://localhost:8000/api/docs/

**停止服务**：

```bash
# 停止容器
docker-compose down

# 停止容器并删除数据卷
docker-compose down -v
```

**详细配置**：

参考项目根目录的 `docker-compose.yml` 和 `Dockerfile`，了解：
- 多阶段构建优化镜像大小
- MySQL、Redis 配置
- Nginx 反向代理
- 健康检查配置

**常用命令**：

```bash
# 查看 Docker 镜像
docker images | grep water-cube

# 手动构建镜像
docker build -t water-cube-web:latest .

# 推送镜像到仓库
docker push your-registry/water-cube-web:latest

# 清理未使用的镜像
docker image prune -a
```

---

### 方式三：Kubernetes 运行模式 (K8s)

**适用场景**：生产环境、高可用部署、微服务架构

**优点**：
- 高可用性（自动故障转移、自动重启）
- 自动扩缩容（HPA）
- 声明式管理
- 支持多集群部署
- 完整的监控告警系统

**前置要求**：
- Kubernetes 集群（1.24+）
- kubectl 命令行工具
- Kustomize 或 Helm（用于部署管理）

**三种部署方案**：

#### 1. 使用 Kustomize（推荐用于学习）

```bash
# 一行命令快速部署
./deploy.sh prod deploy

# 或详细步骤
./deploy.sh dev validate        # 验证配置
./deploy.sh dev generate        # 生成清单
./deploy.sh dev deploy          # 部署应用
./deploy.sh dev status          # 查看状态
./deploy.sh dev logs            # 查看日志
./deploy.sh dev cleanup         # 清理资源
```

#### 2. 使用 Helm Chart（推荐用于生产）

```bash
# 验证 Chart
helm lint ./helm

# 安装应用
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace

# 升级应用
helm upgrade water-cube ./helm

# 卸载应用
helm uninstall water-cube -n water-cube
```

#### 3. 使用 ArgoCD（推荐用于企业 GitOps）

```bash
# 安装 ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 部署应用
kubectl apply -f argocd/application-dev.yaml
kubectl apply -f argocd/application-staging.yaml
kubectl apply -f argocd/application-prod.yaml

# 查看应用状态
argocd app list
argocd app get water-cube-dev
```

**验证部署**：

```bash
# 查看所有资源
kubectl get all -n water-cube

# 查看 Pod 状态
kubectl get pods -n water-cube -w

# 查看服务
kubectl get svc -n water-cube

# 查看 Ingress
kubectl get ingress -n water-cube

# 查看部署进度
kubectl rollout status deployment/web -n water-cube
```

**访问应用**：

```bash
# 本地端口转发
kubectl port-forward svc/web 8000:8000 -n water-cube
# 访问: http://localhost:8000

# 或通过 Ingress 访问（生产环境）
# 访问: https://water-cube.yourdomain.com
```

**部署包含的组件**：
- Web 应用（Deployment，3 副本）
- MySQL 8.0（StatefulSet，10Gi 存储）
- Redis 7（StatefulSet，5Gi 存储）
- Ingress（HTTPS/TLS 支持）
- 自动扩缩容（HPA，3-10 副本）
- Prometheus 监控（4 个告警规则）
- RBAC 权限管理

**环境配置**：
- **dev**：1 副本，DEBUG=True，本地镜像
- **staging**：2 副本，DEBUG=False，日志详细
- **prod**：3-20 副本，自动扩缩容，HPA 启用

**详细文档**：

参考以下 K8s 部署文档：
- `K8S_README.md` - K8s 快速开始
- `K8S_FILES_OVERVIEW.md` - 文件清单
- `K8S_DEPLOY_GUIDE.md` - 详细部署指南
- `K8S_QUICK_REFERENCE.md` - 命令速查表
- `K8S_SUMMARY.md` - 架构和最佳实践
- `helm/README.md` - Helm 使用指南
- `argocd/README.md` - GitOps 部署指南

**常用 kubectl 命令**：

```bash
# 查看日志
kubectl logs -n water-cube -l app=web

# 进入 Pod 交互
kubectl exec -it <pod-name> -n water-cube -- bash

# 查看资源使用
kubectl top pods -n water-cube

# 扩缩容
kubectl scale deployment web --replicas=5 -n water-cube

# 查看事件
kubectl get events -n water-cube
```

---

## 运行方式对比

| 特性 | 原生运行 | Docker | Kubernetes |
|------|--------|--------|------------|
| 学习难度 | ⭐ 简单 | ⭐⭐ 中等 | ⭐⭐⭐ 复杂 |
| 部署速度 | ⚡⚡⚡ 快 | ⚡⚡ 中 | ⚡ 慢 |
| 环境一致性 | ❌ 差 | ✅ 好 | ✅ 很好 |
| 可靠性 | ❌ 低 | ✅ 中 | ✅✅ 高 |
| 自动扩缩容 | ❌ | ❌ | ✅ |
| 高可用性 | ❌ | ❌ | ✅ |
| 多集群支持 | ❌ | ❌ | ✅ |
| 推荐场景 | 开发测试 | 容器部署 | 生产环境 |
| 推荐指数 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## API接口

### 认证接口
- POST `/api/auth/token/` - 获取JWT Token
- POST `/api/auth/token/refresh/` - 刷新Token
- POST `/api/auth/users/` - 用户注册
- GET `/api/auth/users/me/` - 获取当前用户信息

### 业务接口
- `/api/students/` - 学员管理
- `/api/teachers/` - 教师管理
- `/api/classes/dance-types/` - 舞种管理
- `/api/classes/class-types/` - 班型管理
- `/api/classes/courses/` - 课程管理
- `/api/classes/enrollments/` - 报名管理
- `/api/finance/price-policies/` - 价格策略
- `/api/finance/payments/` - 支付记录
- `/api/attendance/` - 考勤记录

详细API文档请访问：http://localhost:8000/api/docs/

## 后台管理

访问 http://localhost:8000/xadmin/ 使用超级管理员账号登录。

### 主要功能
- 用户与权限管理
- 学员档案管理
- 教师信息管理
- 班型与课程配置
- 报名与收费管理
- 考勤统计
- 内容发布（Banner、文章、相册）
- 数据导入导出

## 数据库设计

### 核心数据表
- `users` - 用户表
- `user_profiles` - 用户扩展信息
- `students` - 学员表
- `teachers` - 教师表
- `dance_types` - 舞种分类
- `class_types` - 班型表
- `courses` - 课程表
- `classrooms` - 教室表
- `class_schedules` - 排课表
- `enrollments` - 报名记录
- `price_policies` - 价格策略
- `payments` - 支付记录
- `attendances` - 考勤记录
- `banners` - 轮播图
- `articles` - 文章
- `gallery` - 作品相册
- `contacts` - 联系留言

## 生产部署建议

### Web服务器
```bash
# 使用Gunicorn
gunicorn water_cube_studio.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 静态文件
```bash
python manage.py collectstatic
# 使用Nginx提供静态文件服务
```

### 反向代理（Nginx配置示例）
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /path/to/project/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/project/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 安全配置
- 修改`SECRET_KEY`为随机值
- 设置`DEBUG=False`
- 配置`ALLOWED_HOSTS`
- 启用HTTPS
- 配置CSRF与CORS
- 数据库定期备份

## 扩展功能（后续可添加）

- [ ] 微信/支付宝支付集成
- [ ] 短信通知（课前提醒、续费提醒）
- [ ] 小程序端
- [ ] 在线视频课程
- [ ] 学员成长档案
- [ ] 数据统计报表
- [ ] 优惠券系统
- [ ] 会员积分体系

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系开发团队。
