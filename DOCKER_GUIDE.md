# Docker 部署指南

本项目支持Docker容器化运行，包括以下服务：
- Django Web 应用
- MySQL 8.0 数据库
- Redis 缓存（可选）
- Nginx 反向代理（可选）

## 前置条件

- Docker >= 20.10
- Docker Compose >= 2.0
- Git

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd water_cube_studio
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，根据需要修改配置：

```env
# Django 配置
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# 数据库配置
DB_NAME=water_cube_db
DB_USER=root
DB_PASSWORD=your-secure-password

# Redis 配置（可选）
USE_REDIS=True
REDIS_URL=redis://redis:6379/1

# 其他配置...
```

### 3. 启动服务

#### 基础运行（不含Redis和Nginx）

```bash
docker-compose up -d
```

#### 包含Redis的运行

```bash
docker-compose --profile with-redis up -d
```

#### 包含Nginx反向代理的完整部署

```bash
docker-compose --profile with-redis --profile with-nginx up -d
```

### 4. 初始化数据库

```bash
# 自动执行迁移（在启动时已完成）
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

# 收集静态文件（在启动时已完成）
docker-compose exec web python manage.py collectstatic --noinput
```

## 服务访问

| 服务 | URL | 用途 |
|------|-----|------|
| Web应用 | http://localhost:8000 | Django 应用 |
| 管理后台 | http://localhost:8000/admin | 后台管理 |
| API文档 | http://localhost:8000/api/docs | Swagger 文档 |
| Nginx | http://localhost:80 | 反向代理（使用 with-nginx profile） |
| MySQL | localhost:3306 | 数据库 |
| Redis | localhost:6379 | 缓存（使用 with-redis profile） |

## 常见命令

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f web
docker-compose logs -f mysql
docker-compose logs -f redis
```

### 进入容器

```bash
# 进入Web容器
docker-compose exec web bash

# 进入MySQL容器
docker-compose exec mysql bash

# 进入Redis容器
docker-compose exec redis redis-cli
```

### 执行Django命令

```bash
# 运行迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

# 收集静态文件
docker-compose exec web python manage.py collectstatic --noinput

# 运行测试
docker-compose exec web python manage.py test

# Django shell
docker-compose exec web python manage.py shell
```

### 备份和恢复

#### 备份数据库

```bash
docker-compose exec mysql mysqldump -u root -p$DB_PASSWORD $DB_NAME > backup.sql
```

#### 恢复数据库

```bash
docker-compose exec -T mysql mysql -u root -p$DB_PASSWORD $DB_NAME < backup.sql
```

#### 备份媒体文件

```bash
docker run --rm -v water_cube_studio_media_volume:/data -v $(pwd):/backup \
  alpine tar czf /backup/media_backup.tar.gz -C /data .
```

### 停止和清理

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎！会删除数据库数据）
docker-compose down -v

# 重启服务
docker-compose restart

# 重建镜像
docker-compose build --no-cache
```

## 环境变量说明

### Django 配置

- `DEBUG`: 是否启用调试模式（生产环境应为 False）
- `SECRET_KEY`: Django 密钥，用于加密
- `ALLOWED_HOSTS`: 允许访问的主机列表

### 数据库配置

- `DB_NAME`: 数据库名称
- `DB_USER`: 数据库用户
- `DB_PASSWORD`: 数据库密码
- `DB_HOST`: 数据库主机（Docker模式下为 mysql）
- `DB_PORT`: 数据库端口

### Redis 配置

- `USE_REDIS`: 是否启用 Redis（True/False）
- `REDIS_URL`: Redis 连接地址
- `CACHE_TIMEOUT`: 缓存超时时间（秒）

### 其他配置

- `CORS_ALLOWED_ORIGINS`: CORS 允许的源
- `EMAIL_*`: 邮件服务配置
- `TZ`: 时区设置

## 性能优化

### 1. 启用Redis缓存

编辑 `.env`：
```env
USE_REDIS=True
REDIS_URL=redis://redis:6379/1
```

### 2. Nginx 静态文件缓存

nginx.conf 已配置了静态文件缓存策略：
- 静态文件：30 天
- 媒体文件：7 天

### 3. Gunicorn 工作进程优化

Dockerfile 中配置了 4 个工作进程，可根据服务器 CPU 核心数调整：

```dockerfile
CMD ["gunicorn", \
     "--workers", "4",  # 调整此值为 CPU核心数 * 2 + 1
     ...
```

## 生产环境部署建议

### 1. 使用强密钥

```bash
# 生成强密钥
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. 启用HTTPS

取消注释 nginx.conf 中的 HTTPS 配置，并配置 SSL 证书。

### 3. 使用外部MySQL数据库

修改 `.env` 中的 `DB_HOST` 指向外部数据库服务器。

### 4. 监控和日志

```bash
# 配置日志服务（ELK Stack）
# 修改 docker-compose.yml 添加 Elasticsearch、Logstash、Kibana

# 配置监控（Prometheus + Grafana）
# 添加相应的监控服务
```

### 5. 自动备份

```bash
# 创建备份脚本
#!/bin/bash
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker-compose exec -T mysql mysqldump -u root -p$DB_PASSWORD $DB_NAME \
  | gzip > $BACKUP_DIR/backup_$TIMESTAMP.sql.gz

# 定期执行（使用 cron）
# 0 2 * * * /path/to/backup.sh
```

## 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs web

# 检查配置文件
docker-compose config

# 重建镜像
docker-compose build --no-cache
```

### 数据库连接错误

```bash
# 检查MySQL是否运行
docker-compose ps mysql

# 检查MySQL日志
docker-compose logs mysql

# 测试连接
docker-compose exec mysql mysql -u root -p$DB_PASSWORD -e "SELECT 1"
```

### Redis 连接错误

```bash
# 检查Redis是否运行
docker-compose ps redis

# 测试连接
docker-compose exec redis redis-cli ping

# 查看Redis内存使用
docker-compose exec redis redis-cli INFO stats
```

### 静态文件404错误

```bash
# 重新收集静态文件
docker-compose exec web python manage.py collectstatic --noinput --clear

# 检查 Nginx 配置
docker-compose logs nginx
```

## 常见问题

**Q: 如何修改端口号？**

A: 在 `.env` 文件中修改相应的 `_PORT` 变量。

**Q: 如何使用外部数据库？**

A: 在 docker-compose.yml 中移除 MySQL 服务，并在 `.env` 中配置 DB_HOST。

**Q: 如何升级 Django 或其他包？**

A: 更新 requirements.txt，然后运行 `docker-compose build --no-cache`。

**Q: 如何在容器中运行管理命令？**

A: 使用 `docker-compose exec web python manage.py <command>`。

## 参考资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- [Django 部署指南](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Gunicorn 文档](https://gunicorn.org/)
- [Nginx 文档](https://nginx.org/en/docs/)

---

更多帮助请查看 USER_MANUAL.md 和 项目文档。
