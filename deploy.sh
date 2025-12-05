#!/bin/bash

# Kubernetes 部署脚本
# 用法: ./deploy.sh [dev|staging|prod] [action]
# 示例: ./deploy.sh prod deploy

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
ENVIRONMENT=${1:-dev}
ACTION=${2:-deploy}
NAMESPACE="water-cube"

# 函数定义
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 验证环境
check_prerequisites() {
    print_header "检查前置条件"
    
    # 检查 kubectl
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl 未安装"
        exit 1
    fi
    print_success "kubectl 已安装"
    
    # 检查 kustomize
    if ! command -v kustomize &> /dev/null; then
        print_error "kustomize 未安装"
        exit 1
    fi
    print_success "kustomize 已安装"
    
    # 检查集群连接
    if ! kubectl cluster-info &> /dev/null; then
        print_error "无法连接到 Kubernetes 集群"
        exit 1
    fi
    print_success "已连接到 Kubernetes 集群"
    
    # 验证环境
    if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
        print_error "无效的环境: $ENVIRONMENT (应为 dev|staging|prod)"
        exit 1
    fi
    print_success "环境: $ENVIRONMENT"
}

# 验证配置文件
validate_config() {
    print_header "验证配置文件"
    
    local kustomize_path="k8s/overlays/$ENVIRONMENT"
    
    if [ ! -d "$kustomize_path" ]; then
        print_error "配置目录不存在: $kustomize_path"
        exit 1
    fi
    
    if [ ! -f "$kustomize_path/kustomization.yaml" ]; then
        print_error "kustomization.yaml 不存在: $kustomize_path/kustomization.yaml"
        exit 1
    fi
    
    print_success "配置文件有效"
}

# 生成部署清单
generate_manifests() {
    print_header "生成部署清单"
    
    local kustomize_path="k8s/overlays/$ENVIRONMENT"
    kustomize build "$kustomize_path" > manifests-$ENVIRONMENT.yaml
    
    print_success "清单已生成: manifests-$ENVIRONMENT.yaml"
    
    # 显示摘要
    echo ""
    echo "部署清单摘要:"
    grep "^kind:" manifests-$ENVIRONMENT.yaml | sort | uniq -c
}

# 预检查
pre_deploy_check() {
    print_header "预部署检查"
    
    # 检查命名空间
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        print_warning "命名空间 $NAMESPACE 不存在，将创建"
        kubectl create namespace $NAMESPACE
        print_success "命名空间已创建"
    else
        print_success "命名空间已存在: $NAMESPACE"
    fi
    
    # 检查存储类
    if ! kubectl get storageclass standard &> /dev/null; then
        print_warning "存储类 standard 不存在"
        echo "提示: 请确保集群有默认的存储类"
    else
        print_success "存储类可用: standard"
    fi
}

# 部署应用
deploy() {
    print_header "部署应用"
    
    local kustomize_path="k8s/overlays/$ENVIRONMENT"
    
    # 执行部署
    kustomize build "$kustomize_path" | kubectl apply -f -
    
    print_success "部署命令已执行"
    
    # 等待部署就绪
    print_header "等待部署就绪"
    
    kubectl rollout status -n $NAMESPACE deployment/web --timeout=5m
    print_success "Web 应用已就绪"
    
    kubectl wait --for=condition=ready pod -l app=mysql -n $NAMESPACE --timeout=5m
    print_success "MySQL 已就绪"
    
    kubectl wait --for=condition=ready pod -l app=redis -n $NAMESPACE --timeout=5m
    print_success "Redis 已就绪"
}

# 验证部署
verify_deployment() {
    print_header "验证部署"
    
    echo ""
    echo "Pods 状态:"
    kubectl get pods -n $NAMESPACE -o wide
    
    echo ""
    echo "Services 状态:"
    kubectl get svc -n $NAMESPACE
    
    echo ""
    echo "PVC 状态:"
    kubectl get pvc -n $NAMESPACE
    
    echo ""
    echo "Deployments 状态:"
    kubectl get deployments -n $NAMESPACE
    
    echo ""
    echo "Ingress 状态:"
    kubectl get ingress -n $NAMESPACE
}

# 显示访问信息
show_access_info() {
    print_header "访问信息"
    
    echo ""
    echo "环境: $ENVIRONMENT"
    echo ""
    
    if [[ "$ENVIRONMENT" == "dev" ]]; then
        echo "本地端口转发:"
        echo "  kubectl port-forward -n $NAMESPACE svc/web 8000:8000"
        echo ""
        echo "访问地址: http://localhost:8000"
        echo "后台地址: http://localhost:8000/admin/"
    else
        echo "Ingress 地址:"
        kubectl get ingress -n $NAMESPACE -o wide
        
        echo ""
        print_warning "提示: 请确保 DNS 正确配置或更新 /etc/hosts"
    fi
    
    echo ""
    echo "数据库连接:"
    echo "  Host: mysql.$NAMESPACE.svc.cluster.local"
    echo "  Port: 3306"
    echo "  Database: water_cube_db"
    
    echo ""
    echo "Redis 连接:"
    echo "  Host: redis.$NAMESPACE.svc.cluster.local"
    echo "  Port: 6379"
}

# 查看日志
view_logs() {
    print_header "应用日志"
    
    echo ""
    echo "选择要查看日志的组件:"
    echo "1. web (Django 应用)"
    echo "2. mysql (数据库)"
    echo "3. redis (缓存)"
    echo "4. 全部"
    echo "0. 返回"
    
    read -p "请选择 [0-4]: " choice
    
    case $choice in
        1)
            kubectl logs -n $NAMESPACE -l app=web -f --tail=100
            ;;
        2)
            kubectl logs -n $NAMESPACE -l app=mysql -f --tail=100
            ;;
        3)
            kubectl logs -n $NAMESPACE -l app=redis -f --tail=100
            ;;
        4)
            kubectl logs -n $NAMESPACE -l app=water-cube -f --tail=100
            ;;
        0)
            return
            ;;
        *)
            print_error "无效选择"
            ;;
    esac
}

# 执行数据库迁移
run_migrations() {
    print_header "执行数据库迁移"
    
    # 获取 web pod 名称
    local pod=$(kubectl get pod -n $NAMESPACE -l app=web -o jsonpath='{.items[0].metadata.name}')
    
    if [ -z "$pod" ]; then
        print_error "找不到 web Pod"
        exit 1
    fi
    
    print_success "使用 Pod: $pod"
    
    echo ""
    echo "执行迁移..."
    kubectl exec -n $NAMESPACE -it $pod -- python manage.py migrate
    
    print_success "迁移完成"
}

# 清理资源
cleanup() {
    print_header "清理资源"
    
    read -p "确定要删除所有资源吗? (yes/no): " confirm
    
    if [[ "$confirm" != "yes" ]]; then
        print_warning "取消清理"
        return
    fi
    
    local kustomize_path="k8s/overlays/$ENVIRONMENT"
    
    print_warning "删除资源..."
    kustomize build "$kustomize_path" | kubectl delete -f - --ignore-not-found
    
    print_success "资源已删除"
}

# 回滚部署
rollback() {
    print_header "回滚部署"
    
    echo ""
    echo "部署历史:"
    kubectl rollout history -n $NAMESPACE deployment/web
    
    echo ""
    read -p "输入要回滚到的版本号 (留空则回滚到上一个版本): " revision
    
    if [ -z "$revision" ]; then
        kubectl rollout undo -n $NAMESPACE deployment/web
        print_success "已回滚到上一个版本"
    else
        kubectl rollout undo -n $NAMESPACE deployment/web --to-revision=$revision
        print_success "已回滚到版本 $revision"
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
用法: ./deploy.sh [环境] [操作]

环境:
  dev          开发环境 (1 个副本)
  staging      测试环境 (2 个副本)
  prod         生产环境 (3 个副本)

操作:
  deploy       部署应用（默认）
  validate     验证配置
  generate     生成部署清单
  status       显示部署状态
  logs         查看日志
  migrate      执行数据库迁移
  rollback     回滚部署
  cleanup      清理资源
  help         显示此帮助信息

示例:
  ./deploy.sh dev deploy
  ./deploy.sh prod status
  ./deploy.sh staging logs
  ./deploy.sh dev cleanup

EOF
}

# 主函数
main() {
    case $ACTION in
        deploy)
            check_prerequisites
            validate_config
            generate_manifests
            pre_deploy_check
            deploy
            verify_deployment
            show_access_info
            ;;
        validate)
            check_prerequisites
            validate_config
            print_success "配置有效"
            ;;
        generate)
            check_prerequisites
            validate_config
            generate_manifests
            ;;
        status)
            check_prerequisites
            verify_deployment
            show_access_info
            ;;
        logs)
            check_prerequisites
            view_logs
            ;;
        migrate)
            check_prerequisites
            run_migrations
            ;;
        rollback)
            check_prerequisites
            rollback
            ;;
        cleanup)
            check_prerequisites
            cleanup
            ;;
        help)
            show_help
            ;;
        *)
            print_error "未知操作: $ACTION"
            show_help
            exit 1
            ;;
    esac
}

# 入口点
main
