# Kubernetes 快速参考

水立方舞蹈工作室管理系统的 Kubernetes 部署快速参考指南。

## 项目结构

```
k8s/
├── namespace.yaml              # 命名空间定义
├── configmap.yaml              # 配置映射
├── secret.yaml                 # 敏感信息
├── mysql-deployment.yaml       # MySQL StatefulSet
├── redis-deployment.yaml       # Redis StatefulSet
├── web-deployment.yaml         # Web 应用 Deployment
├── web-rbac.yaml              # RBAC 权限配置
├── ingress.yaml               # Ingress 配置
├── hpa.yaml                   # 自动扩缩容
├── monitoring.yaml            # Prometheus 监控
├── kustomization.yaml         # Kustomize 基础配置
└── overlays/                  # 环境覆盖
    ├── dev/                   # 开发环境
    ├── staging/               # 测试环境
    └── prod/                  # 生产环境
```

## 部署命令速查

### 快速部署

```bash
# 开发环境
./deploy.sh dev deploy

# 测试环境
./deploy.sh staging deploy

# 生产环境
./deploy.sh prod deploy
```

### 常用操作

```bash
# 查看部署状态
./deploy.sh [env] status

# 查看日志
./deploy.sh [env] logs

# 执行数据库迁移
./deploy.sh [env] migrate

# 回滚部署
./deploy.sh [env] rollback

# 清理资源
./deploy.sh [env] cleanup
```

## kubectl 常用命令

### 查看资源

```bash
# 查看所有资源
kubectl get all -n water-cube

# 查看 Pods
kubectl get pods -n water-cube -o wide
kubectl describe pod <pod-name> -n water-cube
kubectl logs <pod-name> -n water-cube

# 查看 Services
kubectl get svc -n water-cube
kubectl get endpoints -n water-cube

# 查看 Deployments
kubectl get deployments -n water-cube
kubectl rollout status deployment/web -n water-cube

# 查看 StatefulSets
kubectl get statefulsets -n water-cube

# 查看 Ingress
kubectl get ingress -n water-cube
kubectl describe ingress water-cube-ingress -n water-cube

# 查看 PVC
kubectl get pvc -n water-cube
kubectl describe pvc <pvc-name> -n water-cube
```

### 调试

```bash
# 进入 Pod 交互式 Shell
kubectl exec -it <pod-name> -n water-cube -- /bin/bash

# 执行命令
kubectl exec <pod-name> -n water-cube -- python manage.py shell

# 查看 Pod 事件
kubectl describe pod <pod-name> -n water-cube

# 查看命名空间事件
kubectl get events -n water-cube --sort-by='.lastTimestamp'

# 端口转发
kubectl port-forward svc/web 8000:8000 -n water-cube
kubectl port-forward svc/mysql 3306:3306 -n water-cube
kubectl port-forward svc/redis 6379:6379 -n water-cube

# 查看资源使用情况
kubectl top nodes
kubectl top pods -n water-cube
```

### 配置管理

```bash
# 查看 ConfigMap
kubectl get configmap -n water-cube
kubectl describe configmap water-cube-config -n water-cube

# 查看 Secret
kubectl get secret -n water-cube
kubectl describe secret water-cube-secret -n water-cube

# 编辑 ConfigMap
kubectl edit configmap water-cube-config -n water-cube

# 编辑 Secret
kubectl edit secret water-cube-secret -n water-cube
```

### 更新部署

```bash
# 更新镜像
kubectl set image deployment/web web=your-registry/water-cube-web:v2 -n water-cube

# 查看部署历史
kubectl rollout history deployment/web -n water-cube

# 回滚到上一个版本
kubectl rollout undo deployment/web -n water-cube

# 回滚到特定版本
kubectl rollout undo deployment/web --to-revision=2 -n water-cube

# 暂停部署更新
kubectl rollout pause deployment/web -n water-cube

# 恢复部署更新
kubectl rollout resume deployment/web -n water-cube
```

### 扩缩容

```bash
# 查看 HPA 状态
kubectl get hpa -n water-cube
kubectl describe hpa web-hpa -n water-cube

# 手动扩缩容
kubectl scale deployment web --replicas=5 -n water-cube

# 查看扩缩容事件
kubectl get events -n water-cube --field-selector involvedObject.kind=HorizontalPodAutoscaler
```

## 常见故障排查

### Pod 无法启动

```bash
# 1. 查看 Pod 状态
kubectl describe pod <pod-name> -n water-cube

# 2. 查看 Pod 日志
kubectl logs <pod-name> -n water-cube
kubectl logs <pod-name> -n water-cube --previous  # 查看历史日志

# 3. 查看初始化容器日志（如果有）
kubectl logs <pod-name> -c migrate -n water-cube

# 4. 常见原因及解决方案：
# - ImagePullBackOff: 镜像不存在或无权访问
#   解决: 检查镜像地址和凭证
# - CrashLoopBackOff: 应用启动失败
#   解决: 检查应用日志和配置
# - Pending: 资源不足或 PVC 绑定失败
#   解决: 检查节点资源和存储类配置
```

### 数据库连接错误

```bash
# 1. 检查 MySQL 是否运行
kubectl get pod -n water-cube -l app=mysql
kubectl logs mysql-0 -n water-cube

# 2. 测试连接
kubectl exec -it <web-pod> -n water-cube -- \
  python manage.py shell
# 在 shell 中：
from django.db import connection
connection.ensure_connection()  # 测试连接

# 3. 查看 MySQL 服务
kubectl get svc mysql -n water-cube
kubectl exec -it mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SHOW DATABASES;"
```

### 静态文件问题

```bash
# 1. 检查 PVC 挂载
kubectl describe pod <web-pod> -n water-cube | grep -A 5 Mounts

# 2. 收集静态文件
kubectl exec <web-pod> -n water-cube -- \
  python manage.py collectstatic --noinput

# 3. 检查文件权限
kubectl exec <web-pod> -n water-cube -- \
  ls -la /app/staticfiles/
```

### Ingress 问题

```bash
# 1. 检查 Ingress 配置
kubectl describe ingress water-cube-ingress -n water-cube

# 2. 检查 Ingress Controller
kubectl get pods -n ingress-nginx

# 3. 检查 Ingress Controller 日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 4. 测试后端连接
kubectl exec -it <ingress-pod> -n ingress-nginx -- \
  curl -I http://web:8000
```

## 性能优化建议

### CPU 和内存

```bash
# 查看资源使用情况
kubectl top pods -n water-cube

# 根据实际使用情况调整资源限制
# 在 overlays/[env]/kustomization.yaml 中修改：
patches:
- target:
    kind: Deployment
    name: web
  patch: |-
    - op: replace
      path: /spec/template/spec/containers/0/resources/requests/cpu
      value: "500m"
```

### 数据库优化

```bash
# 查看 MySQL 连接数
kubectl exec mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SHOW STATUS LIKE 'Threads%';"

# 查看慢查询
kubectl exec mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SELECT * FROM mysql.slow_log\G"
```

### Redis 优化

```bash
# 查看 Redis 内存使用
kubectl exec redis-0 -n water-cube -- redis-cli INFO memory

# 查看 Redis 统计信息
kubectl exec redis-0 -n water-cube -- redis-cli INFO stats
```

## 监控和告警

### Prometheus 查询示例

```bash
# 应用可用性
up{job="water-cube"}

# 请求速率（5分钟）
rate(http_requests_total[5m])

# 错误率
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# 内存使用率
container_memory_usage_bytes{pod=~"web-.*"} / container_spec_memory_limit_bytes{pod=~"web-.*"}

# CPU 使用率
rate(container_cpu_usage_seconds_total{pod=~"web-.*"}[5m])

# 数据库连接数
mysql_global_status_threads_connected

# Redis 内存使用
redis_memory_used_bytes / redis_memory_max_bytes
```

## 备份和恢复

### 备份 MySQL

```bash
# 备份数据库
kubectl exec mysql-0 -n water-cube -- \
  mysqldump -u root -p$MYSQL_ROOT_PASSWORD water_cube_db > backup.sql

# 从 Pod 中复制备份文件
kubectl cp water-cube/mysql-0:/var/lib/mysql ./mysql-backup

# 或使用 Percona Xtrabackup
kubectl exec mysql-0 -n water-cube -- \
  xtrabackup --backup --target-dir=/backup
```

### 恢复 MySQL

```bash
# 恢复数据库
kubectl exec -i mysql-0 -n water-cube -- \
  mysql -u root -p$MYSQL_ROOT_PASSWORD water_cube_db < backup.sql
```

### 备份 Kubernetes 资源

```bash
# 导出所有资源配置
kubectl get all -n water-cube -o yaml > k8s-backup.yaml

# 导出特定资源类型
kubectl get deployments,statefulsets,services,pvc -n water-cube -o yaml > k8s-resources.yaml
```

## 安全建议

### Secrets 管理

```bash
# 使用 Sealed Secrets（推荐）
# 1. 安装 Sealed Secrets Controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# 2. 创建 sealed secret
echo -n 'your-secret-value' | kubectl create secret generic my-secret \
  --dry-run=client --from-file=- | kubeseal > my-sealed-secret.yaml

# 3. 应用 sealed secret
kubectl apply -f my-sealed-secret.yaml
```

### Pod 安全策略

```bash
# 检查 Pod Security Policy
kubectl get psp

# 应用 Pod Security Standards
kubectl label namespace water-cube \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

### Network Policies

```bash
# 查看 NetworkPolicy
kubectl get networkpolicy -n water-cube

# 限制入站流量
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-network-policy
  namespace: water-cube
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 3306  # MySQL
    - protocol: TCP
      port: 6379  # Redis
EOF
```

## 有用的工具

### kubectx/kubens - 快速切换上下文和命名空间

```bash
# 安装
brew install kubectx

# 使用
kubectx              # 列出所有上下文
kubectx <context>   # 切换上下文
kubens              # 列出所有命名空间
kubens water-cube   # 切换命名空间
```

### kube-ps1 - Bash/Zsh 提示符显示当前上下文

```bash
# 安装
git clone https://github.com/jonmosco/kube-ps1.git
echo 'source ~/.kube/kube-ps1.sh' >> ~/.zshrc

# 在提示符中显示
echo 'PS1="$(kube_ps1)$PS1"' >> ~/.zshrc
```

### k9s - Kubernetes 命令行 UI

```bash
# 安装
brew install k9s

# 使用
k9s -n water-cube
```

## 参考资源

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Kustomize 官方文档](https://kustomize.io/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes 最佳实践](https://kubernetes.io/docs/concepts/configuration/overview/)
