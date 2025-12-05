# Kubernetes 部署完整指南

## 项目已支持 Kubernetes 完整部署 ✨

水立方舞蹈工作室管理系统现已完全支持 Kubernetes 容器化部署，提供了三种部署方案。

## 📚 核心文档

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| **[K8S_FILES_OVERVIEW.md](./K8S_FILES_OVERVIEW.md)** | 📋 K8s 文件完整清单和快速导航 | 10 min |
| **[K8S_DEPLOY_GUIDE.md](./K8S_DEPLOY_GUIDE.md)** | 📖 详细部署步骤和故障排查 | 30 min |
| **[K8S_QUICK_REFERENCE.md](./K8S_QUICK_REFERENCE.md)** | ⚡ kubectl 命令速查表 | 5 min |
| **[K8S_SUMMARY.md](./K8S_SUMMARY.md)** | 📊 架构、最佳实践和对比分析 | 20 min |

## 🚀 三种部署方案

### 1️⃣ Kustomize (推荐首选)

**适用**: 学习、小型项目、快速部署

```bash
# 一行命令快速部署
./deploy.sh prod deploy

# 详细步骤
./deploy.sh dev validate        # 验证配置
./deploy.sh dev generate        # 生成清单
./deploy.sh dev deploy          # 部署应用
./deploy.sh dev status          # 查看状态
./deploy.sh dev logs            # 查看日志
./deploy.sh dev cleanup         # 清理资源
```

**优势**:
- ✅ 学习曲线平缓
- ✅ 配置简单清晰
- ✅ 支持多环境覆盖
- ✅ 无需安装额外工具 (kubectl 内置支持)

**文件位置**:
- 基础: `k8s/` (11 个文件)
- 环境覆盖: `k8s/overlays/` (dev/staging/prod)
- 部署脚本: `deploy.sh`

---

### 2️⃣ Helm Chart (企业首选)

**适用**: 生产环境、需要版本管理、团队协作

```bash
# 一行命令安装
helm install water-cube ./helm --namespace water-cube --create-namespace

# 更多用法
helm lint ./helm                              # 验证
helm template water-cube ./helm               # 预览
helm install water-cube ./helm                # 安装
helm upgrade water-cube ./helm                # 升级
helm rollback water-cube                      # 回滚
helm uninstall water-cube -n water-cube       # 卸载
```

**优势**:
- ✅ 强大的参数化配置
- ✅ 支持版本管理
- ✅ 易于发布和共享
- ✅ 支持依赖管理

**文件位置**:
- Chart: `helm/Chart.yaml`
- 配置: `helm/values.yaml`
- 使用: `helm/README.md`

---

### 3️⃣ ArgoCD (自动化首选)

**适用**: 企业 GitOps、多集群管理、自动化 CD

```bash
# 安装 ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 部署应用
kubectl apply -f argocd/application-dev.yaml
kubectl apply -f argocd/application-staging.yaml
kubectl apply -f argocd/application-prod.yaml

# 查看状态
argocd app list
argocd app get water-cube-dev
```

**优势**:
- ✅ GitOps 流程
- ✅ 自动化部署
- ✅ 声明式管理
- ✅ 多集群支持

**文件位置**:
- 应用配置: `argocd/application-*.yaml`
- 使用指南: `argocd/README.md`

---

## 📊 部署方案对比

| 特性 | Kustomize | Helm | ArgoCD |
|------|-----------|------|--------|
| 学习难度 | ⭐ 简单 | ⭐⭐ 中等 | ⭐⭐⭐ 复杂 |
| 部署速度 | ⚡⚡⚡ 快 | ⚡⚡ 中 | ⚡ 自动 |
| 多环境支持 | ✅ | ✅ | ✅ |
| 版本管理 | ❌ | ✅ | ✅ |
| GitOps | ❌ | ❌ | ✅ |
| 适用规模 | 小-中 | 中-大 | 大型企业 |
| 推荐指数 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## ⚡ 快速选择指南

```
选择你的场景:

┌─────────────────────────────────────────┐
│ 我是开发者，想快速部署测试            │
│ → 使用 Kustomize                        │
│   ./deploy.sh dev deploy                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 我们有生产环境，需要可靠部署            │
│ → 使用 Helm Chart                       │
│   helm install water-cube ./helm        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 我们是大企业，需要自动化 GitOps         │
│ → 使用 ArgoCD                           │
│   kubectl apply -f argocd/application-*.yaml │
└─────────────────────────────────────────┘
```

---

## 📦 部署包含的组件

### 应用层
- **Web 应用** (Deployment)
  - 3 个副本（生产环境）
  - 自动扩缩容 (HPA)
  - 健康检查 (Liveness + Readiness)
  - 滚动更新策略

### 数据层
- **MySQL 8.0** (StatefulSet)
  - 持久化存储 (10Gi)
  - 自动备份就绪
  - utf8mb4 字符集

- **Redis 7** (StatefulSet)
  - 持久化存储 (5Gi)
  - AOF 持久化模式
  - 内存限制

### 网络层
- **Ingress**
  - HTTP/HTTPS 支持
  - 自动 TLS 证书 (Cert-Manager)
  - 多虚拟主机

### 可靠性
- **RBAC** 权限管理
- **Pod Disruption Budget** 中断预算
- **Network Policies** 网络隔离

### 监控
- **Prometheus** 监控
- **4 个告警规则** 自动告警

---

## 🎯 三种环境配置

| 环境 | Web 副本 | 特点 | 场景 |
|------|---------|------|------|
| **dev** | 1 | DEBUG=True, 本地镜像 | 开发测试 |
| **staging** | 2 | DEBUG=False, 日志详细 | QA 测试 |
| **prod** | 3-20 | 自动扩缩容, HPA 启用 | 生产环境 |

---

## 🔑 关键文件说明

### Kustomize 基础配置 (k8s/)

```
k8s/namespace.yaml         - 命名空间定义
k8s/configmap.yaml         - 应用配置 (DEBUG, 时区等)
k8s/secret.yaml            - 敏感信息 (密码, API KEY)
k8s/mysql-deployment.yaml  - MySQL 数据库
k8s/redis-deployment.yaml  - Redis 缓存
k8s/web-deployment.yaml    - Web 应用
k8s/web-rbac.yaml          - 权限配置
k8s/ingress.yaml           - 网络入口
k8s/hpa.yaml               - 自动扩缩容
k8s/monitoring.yaml        - Prometheus 监控
k8s/kustomization.yaml     - Kustomize 基础
```

### 环境覆盖配置 (k8s/overlays/)

```
overlays/dev/              - 开发环境 (1 副本, DEBUG=True)
overlays/staging/          - 测试环境 (2 副本, DEBUG=False)
overlays/prod/             - 生产环境 (3+ 副本, HPA 启用)
```

### Helm Chart (helm/)

```
helm/Chart.yaml            - Chart 元数据
helm/values.yaml           - 配置参数
helm/README.md             - Helm 使用指南
```

### ArgoCD (argocd/)

```
argocd/application-dev.yaml        - 开发环境自动部署
argocd/application-staging.yaml    - 测试环境自动部署
argocd/application-prod.yaml       - 生产环境手动部署
argocd/README.md                   - GitOps 指南
```

---

## 📈 工作流程

### 标准部署流程

```
1. 选择方案 (Kustomize/Helm/ArgoCD)
    ↓
2. 配置环境变量 (secret.yaml 或 values.yaml)
    ↓
3. 构建 Docker 镜像
    ↓
4. 执行部署命令
    ↓
5. 验证部署状态
    ↓
6. 查看日志和监控
    ↓
7. 根据需要扩缩容或回滚
```

### 更新应用流程

```
Kustomize:
1. 更新镜像标签
2. 执行 ./deploy.sh prod deploy
3. kubectl 自动执行滚动更新

Helm:
1. 更新 values.yaml 中的镜像
2. 执行 helm upgrade
3. Helm 自动执行滚动更新

ArgoCD:
1. 推送代码到 Git
2. ArgoCD 自动检测变化
3. 自动部署或手动同步
```

---

## ✅ 验证部署

```bash
# 1. 查看所有资源
kubectl get all -n water-cube

# 2. 查看 Pod 状态 (实时监视)
kubectl get pods -n water-cube -w

# 3. 查看部署进度
kubectl rollout status deployment/web -n water-cube

# 4. 查看服务
kubectl get svc -n water-cube

# 5. 查看 Ingress
kubectl get ingress -n water-cube

# 6. 访问应用
kubectl port-forward svc/web 8000:8000 -n water-cube
# 浏览器访问: http://localhost:8000
```

---

## 🐛 故障排查

### Pod 无法启动？

```bash
# 1. 查看 Pod 状态
kubectl describe pod <pod-name> -n water-cube

# 2. 查看 Pod 日志
kubectl logs <pod-name> -n water-cube

# 3. 检查初始化容器日志
kubectl logs <pod-name> -c migrate -n water-cube
```

### 数据库连接失败？

```bash
# 1. 检查 MySQL Pod
kubectl get pod -l app=mysql -n water-cube

# 2. 测试连接
kubectl exec -it <web-pod> -n water-cube -- \
  python manage.py shell
```

### Ingress 不工作？

```bash
# 1. 检查 Ingress Controller
kubectl get pods -n ingress-nginx

# 2. 检查 Ingress 配置
kubectl describe ingress water-cube-ingress -n water-cube
```

更多故障排查方法见: **K8S_QUICK_REFERENCE.md**

---

## 📚 文档导航

### 快速入门
1. **K8S_FILES_OVERVIEW.md** - 了解有哪些文件
2. **K8S_SUMMARY.md** - 了解部署架构
3. 选择一种方案开始部署

### 详细部署
- **K8S_DEPLOY_GUIDE.md** - 完整部署步骤
- **helm/README.md** - Helm 使用
- **argocd/README.md** - ArgoCD 使用

### 日常运维
- **K8S_QUICK_REFERENCE.md** - kubectl 命令速查

---

## 🎓 学习建议

### 初学者路线

```
Day 1: 了解概念
├─ 阅读 K8S_FILES_OVERVIEW.md
├─ 了解三种部署方案的区别
└─ 查看项目的 K8s 文件结构

Day 2: 实践部署
├─ 使用 Kustomize 部署开发环境
├─ ./deploy.sh dev deploy
├─ 验证应用启动
└─ 查看日志

Day 3: 学习运维
├─ 学习 K8S_QUICK_REFERENCE.md 的常用命令
├─ 练习查看日志、扩缩容等操作
├─ 测试更新和回滚
└─ 了解监控告警
```

### 进阶学习

```
深入了解:
├─ Helm Chart 参数化配置
├─ ArgoCD GitOps 工作流
├─ Prometheus 监控系统
├─ 多集群部署
└─ 高可用架构设计
```

---

## 🔐 安全建议

### ❌ 不要这样做

```
- 在代码中提交 Secret
- 在 YAML 中明文写密码
- 使用默认的 Django SECRET_KEY
- 允许所有 IP 访问
```

### ✅ 推荐做法

```
- 使用 Sealed Secrets 或 External Secrets
- 使用云厂商密钥管理服务
- 使用强随机密钥
- 使用 Ingress 和防火墙限制访问
- 启用 RBAC 和 Network Policies
```

---

## 📞 需要帮助？

1. **查看相关文档**
   - 问题和解决方案通常在 K8S_DEPLOY_GUIDE.md 的故障排查部分

2. **使用命令速查表**
   - K8S_QUICK_REFERENCE.md 包含常用的所有命令

3. **查看 Pod 日志**
   - `kubectl logs -n water-cube <pod-name>`

4. **查看事件**
   - `kubectl get events -n water-cube`

5. **阅读完整部署指南**
   - K8S_DEPLOY_GUIDE.md 涵盖所有可能的场景

---

## 📊 项目统计

```
K8s 配置文件:
├─ 基础配置: 11 个文件 (883 行)
├─ 环境覆盖: 9 个文件 (203 行)
├─ Helm: 3 个文件 (162 行)
├─ ArgoCD: 4 个文件 (115 行)
├─ 脚本: 1 个 (392 行)
└─ 文档: 5 个 (3,116 行)

总计: 33 个文件, 4,871 行配置和文档
```

---

## 🎉 开始部署！

```bash
# 最快的开始方式 (Kustomize):
./deploy.sh prod deploy

# 最灵活的方式 (Helm):
helm install water-cube ./helm

# 最自动化的方式 (ArgoCD):
kubectl apply -f argocd/application-prod.yaml

# 然后查看状态:
kubectl get all -n water-cube
```

**下一步**: 阅读 [K8S_FILES_OVERVIEW.md](./K8S_FILES_OVERVIEW.md) 了解更多详情。
