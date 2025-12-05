# Kubernetes 部署总结

## 概述

本项目已完全支持 Kubernetes 容器化部署，提供了多种部署方式和完整的文档支持。

## 部署方案对比

| 方案 | 适用场景 | 复杂度 | 维护成本 | 特点 |
|------|--------|--------|---------|------|
| **Kustomize** | 小到中型项目 | 低 | 低 | 简单易用，支持多环境覆盖 |
| **Helm Chart** | 中到大型项目 | 中 | 中 | 强大的包管理，支持发布 |
| **ArgoCD (GitOps)** | 大型企业 | 高 | 高 | 自动化 CD，声明式配置 |

## 文件结构

### K8s 基础配置

```
k8s/
├── namespace.yaml                 # 命名空间
├── configmap.yaml                 # 配置映射
├── secret.yaml                    # 敏感信息
├── mysql-deployment.yaml          # MySQL StatefulSet
├── redis-deployment.yaml          # Redis StatefulSet
├── web-rbac.yaml                 # RBAC 权限
├── web-deployment.yaml           # Web 应用 Deployment
├── ingress.yaml                  # Ingress 配置
├── hpa.yaml                      # 自动扩缩容
├── monitoring.yaml               # Prometheus 监控
├── kustomization.yaml            # Kustomize 基础
└── overlays/                     # 环境覆盖
    ├── dev/                      # 开发环境 (1 副本)
    ├── staging/                  # 测试环境 (2 副本)
    └── prod/                     # 生产环境 (3 副本)
```

### Helm Chart

```
helm/
├── Chart.yaml                    # Chart 元数据
├── values.yaml                   # 默认值
├── README.md                     # 使用说明
└── templates/                    # K8s 资源模板
```

### ArgoCD GitOps

```
argocd/
├── README.md                     # 部署说明
├── application-dev.yaml          # 开发环境应用
├── application-staging.yaml      # 测试环境应用
└── application-prod.yaml         # 生产环境应用
```

## 快速开始

### 方案 1: Kustomize (推荐用于学习)

```bash
# 验证配置
./deploy.sh dev validate

# 部署开发环境
./deploy.sh dev deploy

# 查看状态
./deploy.sh dev status

# 查看日志
./deploy.sh dev logs

# 清理资源
./deploy.sh dev cleanup
```

### 方案 2: Helm Chart (推荐用于生产)

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

### 方案 3: ArgoCD (推荐用于企业)

```bash
# 安装 ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 部署应用
kubectl apply -f argocd/application-dev.yaml
kubectl apply -f argocd/application-staging.yaml
kubectl apply -f argocd/application-prod.yaml

# 查看应用状态
argocd app list
argocd app get water-cube-dev
```

## 部署流程

### 1. 前置准备

```bash
# 验证集群
kubectl cluster-info
kubectl get nodes

# 验证必需工具
kubectl version --client
kustomize version
helm version
```

### 2. 构建 Docker 镜像

```bash
# 构建镜像
docker build -t your-registry/water-cube-web:latest .

# 推送到仓库
docker push your-registry/water-cube-web:latest

# 更新 Kustomize/Helm 中的镜像地址
# k8s/overlays/[env]/kustomization.yaml
# helm/values.yaml
```

### 3. 配置敏感信息

```bash
# 编辑 secret 配置
# k8s/secret.yaml
# helm/values.yaml

# 包括以下敏感信息:
# - Django SECRET_KEY
# - MySQL 数据库密码
# - Redis 密码
# - 支付 API 密钥
```

### 4. 选择部署方案并部署

**使用 Kustomize:**
```bash
./deploy.sh prod deploy
```

**使用 Helm:**
```bash
helm install water-cube ./helm -f helm/values-prod.yaml
```

**使用 ArgoCD:**
```bash
kubectl apply -f argocd/application-prod.yaml
```

## 环境配置

### 开发环境 (1 副本)

```bash
# 最低配置，用于本地开发测试
./deploy.sh dev deploy

# 特点：
# - 1 个 Web Pod
# - 1 个 MySQL Pod
# - 1 个 Redis Pod
# - DEBUG=True
# - 无自动扩缩容
```

### 测试环境 (2 副本)

```bash
# 中等配置，用于 QA 测试
./deploy.sh staging deploy

# 特点：
# - 2 个 Web Pods (负载均衡)
# - 1 个 MySQL Pod
# - 1 个 Redis Pod
# - DEBUG=False
# - LOG_LEVEL=DEBUG
```

### 生产环境 (3+ 副本)

```bash
# 完整配置，用于生产部署
./deploy.sh prod deploy

# 特点：
# - 3-20 个 Web Pods (自动扩缩容)
# - 1 个 MySQL Pod (建议配置主从复制)
# - 1 个 Redis Pod (建议配置集群)
# - DEBUG=False
# - LOG_LEVEL=WARNING
# - 资源限额和配额
```

## 核心组件

### Web 应用 (Deployment)

```yaml
- 3 个副本（生产环境）
- 副本滚动更新策略
- CPU/内存资源限制
- HTTP 健康检查 (Liveness + Readiness)
- 安全上下文配置
- Pod 反亲和性配置
```

### MySQL 数据库 (StatefulSet)

```yaml
- 1 个副本（Headless Service）
- 持久化存储 (10Gi)
- 存活和就绪探针
- 自动字符集配置 (utf8mb4)
```

### Redis 缓存 (StatefulSet)

```yaml
- 1 个副本（Headless Service）
- 持久化存储 (5Gi, AOF)
- 存活和就绪探针
- 内存限制和驱逐策略
```

### Ingress

```yaml
- 支持 HTTP/HTTPS
- 多个虚拟主机
- 自动 TLS 证书管理 (Cert-Manager)
- 请求体大小限制 (50MB)
- 连接超时优化
```

### 自动扩缩容 (HPA)

```yaml
- CPU 目标利用率: 70%
- 内存目标利用率: 80%
- 最小副本: 3
- 最大副本: 10
- Pod 中断预算 (PDB): 最少可用 2 个
```

### 监控和告警 (Prometheus)

```yaml
- ServiceMonitor 配置
- PrometheusRule 告警规则
- 4 个核心告警:
  1. 高错误率告警 (>5%, 5分钟)
  2. 高内存使用率告警 (>80%, 5分钟)
  3. 数据库连接错误告警 (2分钟)
  4. Redis 不可用告警 (1分钟)
```

## 常用操作

### 查看部署状态

```bash
# 查看所有资源
kubectl get all -n water-cube

# 查看 Pods 详细信息
kubectl get pods -n water-cube -o wide

# 查看 Deployments 状态
kubectl get deployments -n water-cube

# 查看 Services
kubectl get svc -n water-cube

# 查看 Ingress
kubectl get ingress -n water-cube

# 查看 PVC
kubectl get pvc -n water-cube
```

### 调试和排查

```bash
# 查看 Pod 日志
kubectl logs -n water-cube -l app=web

# 进入 Pod Shell
kubectl exec -it <pod-name> -n water-cube -- bash

# 查看事件
kubectl get events -n water-cube

# 查看资源使用
kubectl top pods -n water-cube

# 端口转发
kubectl port-forward svc/web 8000:8000 -n water-cube
```

### 更新和回滚

```bash
# 更新镜像
kubectl set image deployment/web web=your-registry/water-cube-web:v2 -n water-cube

# 查看更新进度
kubectl rollout status deployment/web -n water-cube

# 查看历史版本
kubectl rollout history deployment/web -n water-cube

# 回滚到上一个版本
kubectl rollout undo deployment/web -n water-cube

# 回滚到特定版本
kubectl rollout undo deployment/web --to-revision=2 -n water-cube
```

## 数据库和缓存

### MySQL 访问

```bash
# 连接字符串
mysql -h mysql.water-cube.svc.cluster.local -u root -p -D water_cube_db

# 或在 Pod 中执行
kubectl exec -it mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD -D water_cube_db

# 备份数据库
kubectl exec mysql-0 -n water-cube -- \
  mysqldump -u root -p$MYSQL_ROOT_PASSWORD water_cube_db > backup.sql
```

### Redis 访问

```bash
# 连接到 Redis
kubectl exec -it redis-0 -n water-cube -- redis-cli

# 查看内存使用
kubectl exec redis-0 -n water-cube -- redis-cli INFO memory

# 查看统计信息
kubectl exec redis-0 -n water-cube -- redis-cli INFO stats
```

## 安全建议

### 1. Secret 管理

❌ **不推荐**: 在 YAML 中以明文存储敏感信息

✅ **推荐做法**:
- 使用 Sealed Secrets 或 External Secrets
- 使用云厂商的密钥管理服务 (AWS Secrets Manager, Azure Key Vault 等)
- 使用 RBAC 限制 Secret 访问权限

### 2. 网络安全

```yaml
# 配置 Network Policies 限制流量
# 只允许从 Ingress 访问 Web
# 只允许 Web 访问 MySQL 和 Redis
```

### 3. Pod 安全

```yaml
# 启用 Pod Security Standards
pod-security.kubernetes.io/enforce: restricted

# 设置安全上下文
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

## 性能优化

### 资源配置

```yaml
# Web 应用 (优化后)
requests:
  cpu: 250m
  memory: 256Mi
limits:
  cpu: 500m
  memory: 512Mi

# 根据实际使用情况调整
# 监控 top pods 输出
```

### 缓存策略

```yaml
# 启用 Redis 缓存
USE_REDIS: True
CACHE_TIMEOUT: 3600  # 1小时

# Django 缓存配置
CACHES:
  default:
    BACKEND: 'django_redis.cache.RedisCache'
    LOCATION: 'redis://redis:6379/1'
```

### 数据库优化

```bash
# MySQL 连接池
# 配置持久连接以减少开销

# 查询优化
# 添加适当的数据库索引
# 使用查询缓存
```

## 备份和灾难恢复

### 数据库备份

```bash
# 定期备份 (每日)
# 使用 CronJob 自动化备份

kubectl apply -f - << 'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mysql-backup
  namespace: water-cube
spec:
  schedule: "0 2 * * *"  # 每天 02:00 执行
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: mysql-backup
            image: mysql:8.0
            command:
            - /bin/sh
            - -c
            - |
              mysqldump -h mysql -u root -p$MYSQL_ROOT_PASSWORD \
                water_cube_db | gzip > /backup/$(date +%Y%m%d_%H%M%S).sql.gz
            env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: water-cube-secret
                  key: DB_PASSWORD
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

### 完整性检查

```bash
# 定期检查 PVC 状态
kubectl get pvc -n water-cube

# 验证数据库完整性
kubectl exec mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD -e "CHECK TABLE water_cube_db.*;"
```

## 升级和维护

### 滚动更新

```bash
# 更新 Web 应用版本
./deploy.sh prod deploy  # 会自动执行滚动更新

# 不中断服务，逐个替换 Pod
# maxSurge: 1
# maxUnavailable: 0
```

### 定期维护

- 每月更新 Kubernetes
- 每周更新 Docker 基础镜像
- 定期运行安全扫描
- 定期检查依赖更新

## 成本优化

| 优化项 | 效果 | 难度 |
|--------|------|------|
| 关闭开发环境副本 | 节省 30-50% | 低 |
| 优化资源请求和限制 | 节省 10-20% | 中 |
| 使用 Reserved Instances | 节省 30-70% | 高 |
| 启用 Cluster Autoscaler | 按需扩缩 | 中 |

## 监控指标

### 关键指标

- **应用可用性**: 99.5%+
- **平均响应时间**: <200ms
- **错误率**: <0.1%
- **资源利用率**: CPU <70%, Memory <80%
- **数据库连接数**: <20

### 告警阈值

- 错误率 > 5% (5分钟)
- 内存使用率 > 80% (5分钟)
- 响应时间 > 1000ms (10分钟)
- 数据库连接错误 (2分钟)
- Redis 离线 (1分钟)

## 文档导航

| 文档 | 内容 | 适用场景 |
|------|------|---------|
| [K8S_DEPLOY_GUIDE.md](./K8S_DEPLOY_GUIDE.md) | 详细部署指南 | 完整部署流程 |
| [K8S_QUICK_REFERENCE.md](./K8S_QUICK_REFERENCE.md) | 命令速查表 | 日常运维 |
| [helm/README.md](./helm/README.md) | Helm 使用说明 | Helm 部署 |
| [argocd/README.md](./argocd/README.md) | GitOps 指南 | ArgoCD 部署 |

## 下一步

1. **构建镜像**: 执行 Docker 构建并推送到仓库
2. **选择部署方案**: 根据团队规模选择合适的方案
3. **部署应用**: 执行部署脚本或 Helm 命令
4. **验证部署**: 检查所有资源和服务状态
5. **配置监控**: 启用 Prometheus 和告警
6. **设置备份**: 配置定期数据库备份
7. **文档维护**: 根据实际情况更新配置和文档

## 常见问题

**Q: 应该选择哪种部署方案?**
A: 
- 小型项目: Kustomize
- 中大型项目: Helm
- 企业级部署: ArgoCD + Helm

**Q: 如何处理敏感信息?**
A: 使用 Sealed Secrets 或云厂商密钥服务，不要在代码中存储

**Q: 如何扩展副本数?**
A: 通过修改 overlays 中的配置或使用 HPA 自动扩缩容

**Q: 生产环境的推荐配置是什么?**
A: 至少 3 个 Web Pod，启用 HPA，配置备份和监控

## 技术支持

如有问题，请：
1. 查看相关文档
2. 检查 Kubernetes 日志
3. 联系 DevOps 团队
4. 提交 Issue 报告
