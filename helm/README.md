# Helm Chart - 水立方舞蹈工作室管理系统

## 概述

这是水立方舞蹈工作室管理系统的 Helm Chart，用于在 Kubernetes 集群中快速部署应用。

## 快速开始

### 1. 前置要求

- Kubernetes 1.24+
- Helm 3.0+
- Docker 镜像仓库（用于存储应用镜像）

### 2. 安装

#### 从本地 Chart 安装

```bash
# 验证 Chart
helm lint ./helm

# 安装应用
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace \
  -f helm/values.yaml

# 或使用自定义配置
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace \
  -f helm/values.yaml \
  -f helm/values-prod.yaml
```

#### 从 Helm 仓库安装（如果已发布）

```bash
# 添加仓库
helm repo add water-cube https://your-helm-repo.com
helm repo update

# 安装
helm install water-cube water-cube/water-cube-studio \
  --namespace water-cube \
  --create-namespace
```

### 3. 验证安装

```bash
# 检查部署状态
helm status water-cube -n water-cube

# 列出所有资源
kubectl get all -n water-cube

# 查看 Pod 日志
kubectl logs -n water-cube -l app=web
```

### 4. 卸载

```bash
# 卸载应用
helm uninstall water-cube -n water-cube

# 删除命名空间
kubectl delete namespace water-cube
```

## 自定义配置

### 覆盖值

```bash
# 使用自定义值文件安装
helm install water-cube ./helm \
  -f helm/values.yaml \
  -f helm/values-custom.yaml

# 或使用 --set 选项
helm install water-cube ./helm \
  --set web.replicaCount=5 \
  --set image.web.tag=v2.0.0
```

### 常用配置示例

#### 生产环境

```bash
helm install water-cube ./helm \
  --set web.replicaCount=5 \
  --set web.autoscaling.enabled=true \
  --set web.autoscaling.maxReplicas=20 \
  --set config.DEBUG=false \
  --set web.ingress.enabled=true \
  --set web.ingress.hosts[0].host=water-cube.com
```

#### 开发环境

```bash
helm install water-cube ./helm \
  --set web.replicaCount=1 \
  --set web.autoscaling.enabled=false \
  --set config.DEBUG=true \
  --set web.resources.requests.memory=128Mi
```

### 修改 values 文件

编辑 `helm/values.yaml`：

```yaml
# 修改副本数
web:
  replicaCount: 5

# 修改镜像
image:
  web:
    repository: your-registry/water-cube-web
    tag: v2.0.0

# 修改 Ingress 配置
web:
  ingress:
    hosts:
      - host: water-cube.yourdomain.com
        paths:
          - path: /
            pathType: Prefix
```

## 升级应用

### 升级到新版本

```bash
# 更新 Chart
helm repo update

# 升级应用
helm upgrade water-cube ./helm \
  --namespace water-cube \
  -f helm/values.yaml

# 验证升级
helm rollout history water-cube -n water-cube

# 查看升级进度
helm status water-cube -n water-cube
```

### 回滚到上一个版本

```bash
# 查看发布历史
helm history water-cube -n water-cube

# 回滚到上一个版本
helm rollback water-cube -n water-cube

# 回滚到特定版本
helm rollback water-cube 1 -n water-cube
```

## 故障排查

### Chart 验证

```bash
# 验证 Chart 语法
helm lint ./helm

# 生成 manifests 预览
helm template water-cube ./helm > manifests.yaml

# 使用 dry-run 测试安装
helm install water-cube ./helm --dry-run --debug
```

### 查看已安装的 Chart

```bash
# 列出所有发布
helm list -n water-cube

# 查看发布详情
helm get values water-cube -n water-cube
helm get manifest water-cube -n water-cube
```

### 常见问题

#### 镜像拉取失败

```yaml
# 检查 values.yaml 中的镜像配置
image:
  web:
    repository: your-registry/water-cube-web  # 确保地址正确
    pullPolicy: IfNotPresent

# 添加镜像拉取密钥（如果需要）
imagePullSecrets:
  - name: dockercfg
```

#### Pod 启动失败

```bash
# 查看 Pod 日志
kubectl logs -n water-cube <pod-name>

# 查看 Pod 描述
kubectl describe pod -n water-cube <pod-name>

# 检查资源限制
kubectl top pods -n water-cube
```

#### Ingress 不工作

```bash
# 检查 Ingress Controller
kubectl get pods -n ingress-nginx

# 检查 Ingress 配置
kubectl get ingress -n water-cube

# 验证 Ingress 规则
kubectl describe ingress -n water-cube
```

## Helm Chart 结构

```
helm/
├── Chart.yaml                 # Chart 元数据
├── values.yaml               # 默认值
├── charts/                   # 依赖 Chart
├── templates/                # Kubernetes 资源模板
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── deployment-web.yaml
│   ├── statefulset-mysql.yaml
│   ├── statefulset-redis.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── rbac.yaml
└── README.md
```

## 值（Values）参考

### 顶级键

| 键 | 默认值 | 说明 |
|----|--------|------|
| `namespace` | `water-cube` | Kubernetes 命名空间 |
| `image` | - | Docker 镜像配置 |
| `web` | - | Web 应用配置 |
| `mysql` | - | MySQL 数据库配置 |
| `redis` | - | Redis 缓存配置 |
| `config` | - | 应用配置 |
| `secrets` | - | 敏感信息 |
| `rbac` | - | RBAC 配置 |
| `monitoring` | - | 监控配置 |

### Web 应用配置

```yaml
web:
  replicaCount: 3              # 副本数
  
  resources:
    requests:
      cpu: 250m               # CPU 请求
      memory: 256Mi           # 内存请求
    limits:
      cpu: 500m               # CPU 限制
      memory: 512Mi           # 内存限制
  
  autoscaling:
    enabled: true             # 启用自动扩缩容
    minReplicas: 3            # 最小副本数
    maxReplicas: 10           # 最大副本数
    cpuTarget: 70             # CPU 目标利用率
    memoryTarget: 80          # 内存目标利用率
  
  service:
    type: ClusterIP           # 服务类型
    port: 8000                # 服务端口
  
  ingress:
    enabled: true             # 启用 Ingress
    className: nginx          # Ingress Controller 类名
    hosts:
      - host: water-cube.local
        paths:
          - path: /
            pathType: Prefix
```

## 部署到不同环境

### 开发环境

```bash
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace \
  -f helm/values-dev.yaml
```

### 测试环境

```bash
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace \
  -f helm/values-staging.yaml
```

### 生产环境

```bash
helm install water-cube ./helm \
  --namespace water-cube \
  --create-namespace \
  -f helm/values-prod.yaml
```

## 与 ArgoCD 集成

创建 ArgoCD Application：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: water-cube-helm
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/your-org/water-cube-studio.git
    targetRevision: main
    path: helm
    helm:
      values: |
        web:
          replicaCount: 3
      valueFiles:
      - helm/values-prod.yaml
  
  destination:
    server: https://kubernetes.default.svc
    namespace: water-cube
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 发布 Helm Chart

### 将 Chart 推送到仓库

```bash
# 打包 Chart
helm package ./helm

# 上传到 Helm 仓库
# （具体命令取决于你的仓库平台）

# 更新仓库索引
helm repo index . --url https://your-helm-repo.com
```

## 参考资源

- [Helm 官方文档](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kubernetes Helm Hub](https://hub.helm.sh/)

## 许可证

Apache License 2.0
