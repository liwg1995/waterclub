# Kubernetes 部署指南

本指南详细说明如何在 Kubernetes 集群中部署水立方舞蹈工作室管理系统。

## 目录

- [前置要求](#前置要求)
- [架构概述](#架构概述)
- [部署步骤](#部署步骤)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [监控告警](#监控告警)
- [故障排查](#故障排查)

## 前置要求

### 必需软件

1. **Kubernetes 集群** (v1.24+)
   - 可选：本地测试使用 minikube 或 Docker Desktop K8s

2. **kubectl** (v1.24+)
   ```bash
   # 验证安装
   kubectl version --client
   ```

3. **Kustomize** (v5.0+)
   ```bash
   # 验证安装
   kustomize version
   ```

4. **Docker** (用于构建镜像)
   ```bash
   docker version
   ```

### 集群要求

- 最少 3 个 Worker 节点
- 每个节点最少 2GB RAM
- 每个节点最少 1 核 CPU
- 集群需要支持 PersistentVolume

### 可选组件

- **Ingress Controller** (nginx-ingress)
- **Cert-Manager** (HTTPS/TLS 证书)
- **Prometheus + Grafana** (监控)
- **ELK Stack** (日志收集)

## 架构概述

```
┌─────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                    │
├──────────────────┬──────────────────┬──────────────────┤
│   Ingress Nginx  │    Namespace:    │  StatefulSets    │
│                  │   water-cube     │                  │
├──────────────────┼──────────────────┼──────────────────┤
│                  │  Deployments     │                  │
│  water-cube-     │  ├─ web (3)      │  ├─ mysql (1)   │
│  ingress         │  └─ worker       │  └─ redis (1)   │
│                  │                  │                  │
│  Services        │  ConfigMaps      │  PersistentVol  │
│  ├─ web:8000    │  ├─ config       │  ├─ mysql-pvc  │
│  ├─ mysql:3306  │  └─ secret       │  ├─ redis-pvc  │
│  └─ redis:6379  │                  │  └─ media-pvc  │
└──────────────────┴──────────────────┴──────────────────┘
```

### 部署组件

| 组件 | 类型 | 副本数 | 存储 | 描述 |
|------|------|--------|------|------|
| web | Deployment | 3 | 静态+媒体卷 | Django 应用，支持自动扩缩 |
| mysql | StatefulSet | 1 | 10Gi | MySQL 8.0 数据库 |
| redis | StatefulSet | 1 | 5Gi | Redis 缓存 |

## 部署步骤

### 1. 环境准备

```bash
# 创建工作目录
mkdir -p /path/to/k8s-deployment
cd /path/to/k8s-deployment

# 复制 K8s 配置文件
cp -r k8s/* .

# 列出所有文件
ls -la
# 输出：
# namespace.yaml
# configmap.yaml
# secret.yaml
# mysql-deployment.yaml
# redis-deployment.yaml
# web-rbac.yaml
# web-deployment.yaml
# ingress.yaml
# hpa.yaml
# monitoring.yaml
# kustomization.yaml
```

### 2. 验证集群连接

```bash
# 检查集群可用性
kubectl cluster-info

# 列出节点
kubectl get nodes

# 检查默认 StorageClass
kubectl get storageclass
```

### 3. 构建 Docker 镜像

```bash
# 进入项目根目录
cd /path/to/water-cube-studio

# 构建镜像
docker build -t your-registry/water-cube-web:latest .

# 推送到镜像仓库
docker push your-registry/water-cube-web:latest

# 验证镜像
docker images | grep water-cube-web
```

### 4. 修改配置文件

#### 4.1 修改镜像地址 (kustomization.yaml)

```yaml
# kustomization.yaml
images:
- name: water-cube-web
  newName: your-registry/water-cube-web  # 修改为实际地址
  newTag: latest
```

#### 4.2 修改 Secret 敏感信息 (secret.yaml)

```yaml
# secret.yaml
stringData:
  SECRET_KEY: "your-production-secret-key"
  DB_PASSWORD: "your-secure-password"
  REDIS_PASSWORD: "your-redis-password"
  # 填写实际的支付配置
  ALIPAY_APP_ID: "real-alipay-id"
  WECHAT_APP_ID: "real-wechat-id"
```

> ⚠️ **安全提示**：生产环境不要将密钥提交到 Git。使用 Sealed Secrets 或 External Secrets 管理。

#### 4.3 修改 ConfigMap (configmap.yaml)

```yaml
# configmap.yaml
data:
  DEBUG: "False"  # 生产环境必须 False
  ALLOWED_HOSTS: "water-cube.yourdomain.com,api.water-cube.yourdomain.com"
  LANGUAGE_CODE: "zh-hans"
  TIME_ZONE: "Asia/Shanghai"
```

#### 4.4 修改 Ingress (ingress.yaml)

```yaml
# ingress.yaml
spec:
  rules:
  - host: water-cube.yourdomain.com  # 修改为实际域名
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 8000
  - host: api.water-cube.yourdomain.com  # API 域名
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 8000
```

### 5. 使用 Kustomize 部署

#### 5.1 验证部署文件

```bash
# 使用 Kustomize 生成最终配置
kustomize build . > generated.yaml

# 验证生成的 YAML
kubectl apply -f generated.yaml --dry-run=client -o yaml | head -50
```

#### 5.2 创建命名空间

```bash
# 创建 water-cube 命名空间
kubectl apply -f namespace.yaml

# 验证命名空间创建成功
kubectl get namespace water-cube
```

#### 5.3 部署应用

```bash
# 使用 Kustomize 部署所有资源
kustomize build . | kubectl apply -f -

# 或者直接使用 kubectl 部署
kubectl apply -k .

# 验证部署状态
kubectl get all -n water-cube
```

### 6. 验证部署

```bash
# 查看 Pod 状态
kubectl get pods -n water-cube -w

# 查看服务
kubectl get svc -n water-cube

# 查看 PVC 状态
kubectl get pvc -n water-cube

# 查看 Ingress
kubectl get ingress -n water-cube

# 查看 HPA 状态
kubectl get hpa -n water-cube
```

### 7. 访问应用

#### 7.1 本地开发环境 (使用 port-forward)

```bash
# 转发 web 服务
kubectl port-forward -n water-cube svc/web 8000:8000

# 浏览器访问
# http://localhost:8000

# 转发 mysql 服务
kubectl port-forward -n water-cube svc/mysql 3306:3306

# 转发 redis 服务
kubectl port-forward -n water-cube svc/redis 6379:6379
```

#### 7.2 生产环境 (使用 Ingress)

```bash
# 获取 Ingress IP/域名
kubectl get ingress -n water-cube

# 更新本地 /etc/hosts (如果未配置 DNS)
# 127.0.0.1  water-cube.local api.water-cube.local

# 浏览器访问
# http://water-cube.local
# https://water-cube.local (配置证书后)
```

## 配置说明

### ConfigMap (configmap.yaml)

| 变量 | 值 | 说明 |
|------|-----|------|
| DEBUG | False | Django 调试模式 |
| ALLOWED_HOSTS | localhost,127.0.0.1,*.water-cube.local | 允许的主机 |
| LANGUAGE_CODE | zh-hans | 语言 |
| TIME_ZONE | Asia/Shanghai | 时区 |
| USE_REDIS | True | 启用 Redis |
| CACHE_TIMEOUT | 3600 | 缓存超时时间（秒） |

### Secret (secret.yaml)

敏感信息存储，包括：
- Django SECRET_KEY
- 数据库密码
- Redis 密码
- 支付 API 密钥

### 资源限制

#### Web 应用 (Deployment)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### MySQL (StatefulSet)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### Redis (StatefulSet)

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "250m"
```

### 健康检查

#### Liveness Probe (存活探针)

```yaml
livenessProbe:
  httpGet:
    path: /admin/
    port: 8000
  initialDelaySeconds: 60
  periodSeconds: 10
  failureThreshold: 3
```

#### Readiness Probe (就绪探针)

```yaml
readinessProbe:
  httpGet:
    path: /admin/
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 5
  failureThreshold: 3
```

### 自动扩缩容 (HPA)

```yaml
minReplicas: 3
maxReplicas: 10

metrics:
- CPU 使用率: 70%
- 内存使用率: 80%
```

## 常见问题

### 1. Pod 无法启动

```bash
# 查看 Pod 日志
kubectl logs -n water-cube -l app=web

# 查看 Pod 详细信息
kubectl describe pod -n water-cube <pod-name>

# 常见原因：
# - 镜像不存在或无权访问
# - 数据库连接失败
# - 配置文件错误
```

### 2. 数据库迁移失败

```bash
# 手动执行迁移
kubectl exec -n water-cube -it <web-pod-name> -- python manage.py migrate

# 创建超级管理员
kubectl exec -n water-cube -it <web-pod-name> -- \
  python manage.py createsuperuser
```

### 3. 静态文件不加载

```bash
# 收集静态文件
kubectl exec -n water-cube -it <web-pod-name> -- \
  python manage.py collectstatic --noinput

# 检查静态文件卷挂载
kubectl describe pod -n water-cube <web-pod-name> | grep -A 5 Mounts
```

### 4. Redis 连接失败

```bash
# 测试 Redis 连接
kubectl exec -n water-cube -it redis-0 -- redis-cli ping

# 查看 Redis 日志
kubectl logs -n water-cube redis-0
```

### 5. Ingress 不工作

```bash
# 检查 Ingress 状态
kubectl get ingress -n water-cube -o yaml

# 检查 Ingress Controller 日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 确保 Ingress Controller 已安装
kubectl get pods -n ingress-nginx
```

## 监控告警

### Prometheus 监控指标

系统已配置以下告警规则：

#### 高错误率告警
- 条件：5分钟内错误率 > 5%
- 动作：立即告警

#### 高内存使用率告警
- 条件：内存使用率 > 80%
- 动作：5分钟后告警

#### 数据库连接错误告警
- 条件：出现连接错误
- 动作：2分钟后告警

#### Redis 不可用告警
- 条件：Redis 服务离线
- 动作：1分钟后告警

### 查看监控指标

```bash
# 使用 Prometheus UI
kubectl port-forward -n monitoring svc/prometheus 9090:9090

# 浏览器访问
# http://localhost:9090

# 查询示例：
# up{job="water-cube"}  # 应用可用性
# rate(http_requests_total[5m])  # 请求速率
# container_memory_usage_bytes  # 内存使用
```

### 设置告警接收器

修改 `monitoring.yaml` 中的告警规则，配置接收器：

```yaml
groups:
- name: water-cube
  rules:
  - alert: HighErrorRate
    # ... 告警规则
    annotations:
      summary: "高错误率告警"
      # 配置告警通知（邮件/Slack/钉钉等）
```

## 故障排查

### 日志收集

```bash
# 查看所有组件日志
kubectl logs -n water-cube -l app=water-cube

# 实时查看日志
kubectl logs -n water-cube -l app=web -f

# 查看特定 Pod 的历史日志
kubectl logs -n water-cube <pod-name> --previous
```

### 连接调试

```bash
# 进入 Pod 交互式 Shell
kubectl exec -n water-cube -it <pod-name> -- /bin/bash

# 测试网络连接
kubectl run -n water-cube -it --rm debug --image=busybox -- /bin/sh
# 在 Pod 内执行：
# wget http://web:8000
# nc -zv mysql 3306
# redis-cli -h redis ping
```

### 事件查看

```bash
# 查看命名空间事件
kubectl get events -n water-cube

# 查看特定 Pod 的事件
kubectl describe pod -n water-cube <pod-name>
```

### 性能诊断

```bash
# 查看资源使用情况
kubectl top nodes
kubectl top pods -n water-cube

# 查看 HPA 状态
kubectl describe hpa -n water-cube web-hpa

# 查看扩缩容历史
kubectl get events -n water-cube --sort-by='.lastTimestamp'
```

## 生产环境建议

### 1. 安全性

- [ ] 使用 Sealed Secrets 或 External Secrets 管理敏感信息
- [ ] 启用 Pod Security Policy (PSP)
- [ ] 使用 Network Policies 限制网络流量
- [ ] 启用 RBAC 和细粒度权限控制
- [ ] 定期更新镜像，扫描安全漏洞

### 2. 高可用

- [ ] 配置多个节点的数据库主从复制
- [ ] 部署 Redis Sentinel 或 Cluster
- [ ] 配置备份和恢复策略
- [ ] 部署多个 Ingress Controller 实例
- [ ] 使用 Pod Disruption Budget 保证可用性

### 3. 性能优化

- [ ] 调整 HPA 参数以优化自动扩缩容
- [ ] 启用 Pod 预启动和预缓存
- [ ] 配置请求和响应缓存
- [ ] 使用 CDN 加速静态资源
- [ ] 优化数据库连接池参数

### 4. 监控日志

- [ ] 部署 Prometheus 和 Grafana 监控
- [ ] 配置 ELK 或其他日志聚合系统
- [ ] 设置告警通知 (邮件/Slack/钉钉)
- [ ] 定期审计和分析日志

### 5. 备份恢复

- [ ] 定期备份 MySQL 数据
- [ ] 定期备份 Kubernetes 资源配置
- [ ] 测试恢复过程
- [ ] 记录 RTO 和 RPO

## 更新和回滚

### 更新应用

```bash
# 更新镜像标签
kustomize edit set image water-cube-web=your-registry/water-cube-web:v2

# 重新部署
kustomize build . | kubectl apply -f -

# 查看更新进度
kubectl rollout status -n water-cube deployment/web

# 等待所有 Pod 就绪
kubectl wait --for=condition=ready pod -l app=web -n water-cube --timeout=300s
```

### 回滚应用

```bash
# 查看部署历史
kubectl rollout history -n water-cube deployment/web

# 回滚到上一个版本
kubectl rollout undo -n water-cube deployment/web

# 回滚到指定版本
kubectl rollout undo -n water-cube deployment/web --to-revision=2

# 查看回滚进度
kubectl rollout status -n water-cube deployment/web
```

## 清理资源

```bash
# 删除所有部署的资源
kustomize build . | kubectl delete -f -

# 或删除整个命名空间
kubectl delete namespace water-cube

# 验证删除
kubectl get namespace water-cube
```

## 参考资源

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Django 部署指南](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Kustomize 官方文档](https://kustomize.io/)
- [Ingress Nginx 文档](https://kubernetes.github.io/ingress-nginx/)
- [Cert-Manager 文档](https://cert-manager.io/)

## 技术支持

如有问题，请：

1. 查看本文档的故障排查部分
2. 检查 Kubernetes 事件和 Pod 日志
3. 联系 DevOps 团队
4. 提交问题报告（包含日志和配置）
