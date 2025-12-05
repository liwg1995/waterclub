# ArgoCD GitOps 配置

## 概述

本配置使用 ArgoCD 实现持续部署 (GitOps)。

## 安装 ArgoCD

```bash
# 创建 argocd 命名空间
kubectl create namespace argocd

# 安装 ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 等待 ArgoCD 启动
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# 获取初始密码
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# 访问 ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# 访问: https://localhost:8080
```

## 目录结构

```
.
└── argocd/
    ├── application-dev.yaml
    ├── application-staging.yaml
    ├── application-prod.yaml
    └── README.md
```

## 创建 ArgoCD Application

```bash
# 开发环境
kubectl apply -f argocd/application-dev.yaml

# 测试环境
kubectl apply -f argocd/application-staging.yaml

# 生产环境
kubectl apply -f argocd/application-prod.yaml

# 查看应用状态
kubectl get applications -n argocd
argocd app list

# 查看应用详情
argocd app get water-cube-dev
```

## 工作流程

1. 开发者推送代码到 Git 仓库
2. ArgoCD 自动检测变化（每3分钟）
3. ArgoCD 自动部署更新
4. 监控系统告警异常

## 同步策略

### 自动同步（推荐用于开发环境）

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
  - CreateNamespace=true
```

### 手动同步（推荐用于生产环境）

```yaml
syncPolicy:
  syncOptions:
  - CreateNamespace=true
```

手动同步命令：
```bash
argocd app sync water-cube-prod
```

## 常用命令

```bash
# 查看应用列表
argocd app list

# 查看应用详情
argocd app get water-cube-dev

# 查看应用健康状态
argocd app get water-cube-dev --refresh

# 强制同步
argocd app sync water-cube-dev --force

# 回滚应用
argocd app rollback water-cube-dev 0

# 删除应用
argocd app delete water-cube-dev --cascade

# 设置自动同步
argocd app set water-cube-dev --auto-prune --self-heal

# 禁用自动同步
argocd app set water-cube-dev --auto-prune=false --self-heal=false

# 暂停应用
kubectl patch application water-cube-dev -p '{"metadata":{"finalizers":["resources-finalizer.argocd.argoproj.io"]}}' --type merge -n argocd

# 监视应用同步进度
watch -n 1 'argocd app get water-cube-dev | grep -A 10 "Status"'
```

## 故障排查

```bash
# 查看 ArgoCD 服务器日志
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server -f

# 查看 ArgoCD 应用控制器日志
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller -f

# 查看应用同步状态
kubectl get application water-cube-dev -n argocd -o yaml

# 查看应用同步失败原因
argocd app get water-cube-dev --refresh
```

## 与 CI/CD 集成

### GitLab CI/CD

```yaml
deploy-dev:
  stage: deploy
  script:
    - argocd app sync water-cube-dev
  only:
    - dev
  when: manual

deploy-prod:
  stage: deploy
  script:
    - argocd app sync water-cube-prod
  only:
    - main
  when: manual
```

### GitHub Actions

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Login to ArgoCD
        run: |
          argocd login ${{ secrets.ARGOCD_SERVER }} \
            --username ${{ secrets.ARGOCD_USERNAME }} \
            --password ${{ secrets.ARGOCD_PASSWORD }}
      
      - name: Sync Application
        run: |
          argocd app sync water-cube-prod --wait
```

## 监控和通知

### 配置 Slack 通知

```yaml
# 编辑 argocd-notifications-cm ConfigMap
kubectl edit configmap argocd-notifications-cm -n argocd

# 添加以下内容
service.slack.token: $slack-token  # 设置 Slack Token

trigger.on-health-degraded: |
  when: app.status.health.status == 'Unknown' or app.status.health.status == 'Degraded'
  oncePer: 15m
  send: [slack-notification]

trigger.on-sync-failed: |
  when: app.status.operationState.phase in ['Error', 'Failed']
  oncePer: 15m
  send: [slack-notification]
```

### 配置钉钉通知

```yaml
# 编辑 argocd-notifications-cm ConfigMap
service.webhook.dingtalk.url: $dingtalk-webhook-url

trigger.on-sync-failed: |
  when: app.status.operationState.phase in ['Error', 'Failed']
  oncePer: 15m
  send: [dingtalk-notification]
```

## 安全性

### 创建只读用户

```bash
# 登录 ArgoCD
argocd login <argocd-server>

# 创建只读账户
argocd account create readonly

# 设置只读权限
argocd account update-password readonly --new-password <password> --current-password <current-password>

# 配置 RBAC
kubectl edit configmap argocd-rbac-cm -n argocd

# 添加角色定义
p, role:readonly, applications, get, */*, allow
p, role:readonly, repositories, get, *, allow
g, readonly, role:readonly
```

### 使用 SSH Keys 连接 Git 仓库

```bash
# 生成 SSH 密钥对
ssh-keygen -t rsa -b 4096 -f argocd-ssh-key

# 将公钥添加到 Git 仓库的部署密钥中

# 创建 Secret
kubectl create secret generic argocd-ssh-key \
  --from-file=ssh-privatekey=argocd-ssh-key \
  -n argocd

# 配置 ArgoCD 使用 SSH
kubectl patch secret argocd-ssh-key -n argocd -p '{"metadata":{"labels":{"argocd.argoproj.io/secret-type":"repository"}}}'
```

## 备份和恢复

### 备份 ArgoCD 配置

```bash
# 导出所有 ArgoCD 资源
kubectl get all -n argocd -o yaml > argocd-backup.yaml

# 导出 Application 配置
kubectl get application -n argocd -o yaml > argocd-applications-backup.yaml

# 导出 Secret
kubectl get secret -n argocd -o yaml > argocd-secrets-backup.yaml
```

### 恢复 ArgoCD 配置

```bash
# 恢复配置
kubectl apply -f argocd-backup.yaml
```

## 参考资源

- [ArgoCD 官方文档](https://argo-cd.readthedocs.io/)
- [ArgoCD 最佳实践](https://argo-cd.readthedocs.io/en/latest/operator-manual/best_practices/)
- [GitOps 工作流程](https://www.gitops.tech/)
