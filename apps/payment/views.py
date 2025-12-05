from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.conf import settings
import json
import logging
from datetime import datetime
import uuid
from .models import PaymentRecord, AlipayConfig, WeChatPayConfig, HuPiPayConfig
from apps.classes.models import Enrollment
from apps.students.models import Student

logger = logging.getLogger(__name__)


def create_payment(request):
    """创建支付记录"""
    try:
        enrollment_id = request.GET.get('enrollment_id')
        payment_method = request.GET.get('payment_method', 'alipay_web')  # 默认支付宝网页支付
        
        if not enrollment_id:
            return JsonResponse({'status': 'error', 'message': '报名ID不能为空'})
        
        try:
            enrollment = Enrollment.objects.get(pk=enrollment_id)
        except Enrollment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '报名记录不存在'})
        
        # 检查是否已经支付过
        if enrollment.status == 'paid':
            return JsonResponse({'status': 'error', 'message': '该报名已经支付'})
        
        # 检查是否已有支付记录
        if enrollment.payment_record and enrollment.payment_record.status == 'pending':
            payment_record = enrollment.payment_record
        else:
            # 创建新的支付记录
            order_no = f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
            
            # 计算收费金额
            if enrollment.amount > 0:
                amount = enrollment.amount
            elif enrollment.price_policy:
                amount = enrollment.price_policy.price
            else:
                # 默认按课程最大人数和需要的课次计算，此处省略
                amount = 0
            
            if amount <= 0:
                return JsonResponse({'status': 'error', 'message': '无效的收费金额'})
            
            payment_record = PaymentRecord.objects.create(
                student=enrollment.student,
                order_no=order_no,
                amount=amount,
                payment_method=payment_method,
                status='pending',
            )
            
            # 更新enrollment的支付记录
            enrollment.payment_record = payment_record
            enrollment.save()
        
        # 返回支付页面，包含订单信息
        context = {
            'payment_record': payment_record,
            'enrollment': enrollment,
            'order_no': payment_record.order_no,
            'amount': payment_record.amount,
            'student_name': enrollment.student.real_name,
            'course_name': enrollment.course.name,
        }
        
        return render(request, 'payment/payment_form.html', context)
    except Exception as e:
        logger.error(f"创建支付记录失败: {e}")
        return JsonResponse({'status': 'error', 'message': '创建支付记录失败'})


def payment_list(request):
    """支付记录列表"""
    payments = PaymentRecord.objects.all()
    context = {'payments': payments}
    return render(request, 'payment/payment_list.html', context)


def payment_success(request):
    """支付成功流程"""
    order_no = request.GET.get('order_no', '')
    try:
        payment_record = PaymentRecord.objects.get(order_no=order_no)
        # 更新报名计划是否为已支付
        enrollment = Enrollment.objects.get(payment_record=payment_record)
        enrollment.status = 'paid'
        enrollment.save()
        
        context = {'payment_record': payment_record, 'enrollment': enrollment}
        return render(request, 'payment/payment_success.html', context)
    except (PaymentRecord.DoesNotExist, Enrollment.DoesNotExist):
        return render(request, 'payment/payment_error.html', {'message': '订单不存在'})


def payment_failure(request):
    """支付失败流程"""
    return render(request, 'payment/payment_failure.html')


@csrf_exempt
@require_http_methods(["POST"])
def alipay_notify(request):
    """支付宝异步通知"""
    try:
        # 获取支付宝POST过来的数据
        data = request.POST.dict()
        
        # 验证签名（这里需要实现具体的验证逻辑）
        # 如果验证通过，更新支付记录状态
        order_no = data.get('out_trade_no')
        trade_status = data.get('trade_status')
        
        # TODO: 实现具体的支付宝验签逻辑和订单状态更新
        
        logger.info(f"支付宝异步通知: 订单号={order_no}, 状态={trade_status}")
        
        # 返回成功响应
        return HttpResponse("success")
    except Exception as e:
        logger.error(f"支付宝异步通知处理失败: {e}")
        return HttpResponse("fail")


def alipay_return(request):
    """支付宝同步返回"""
    try:
        # 获取支付宝GET过来的数据
        data = request.GET.dict()
        
        # 验证签名（这里需要实现具体的验证逻辑）
        order_no = data.get('out_trade_no')
        
        # TODO: 实现具体的支付宝验签逻辑
        
        logger.info(f"支付宝同步返回: 订单号={order_no}")
        
        # 重定向到支付成功页面
        return redirect('/payment/success/')
    except Exception as e:
        logger.error(f"支付宝同步返回处理失败: {e}")
        return redirect('/payment/failure/')


@csrf_exempt
@require_http_methods(["POST"])
def wechat_notify(request):
    """微信支付异步通知"""
    try:
        # 获取微信支付POST过来的数据
        data = request.body.decode('utf-8')
        
        # 解析XML数据（这里需要实现具体的解析逻辑）
        # 验证签名（这里需要实现具体的验证逻辑）
        # 如果验证通过，更新支付记录状态
        
        # TODO: 实现具体的微信支付验签逻辑和订单状态更新
        
        logger.info("微信支付异步通知")
        
        # 返回成功响应（XML格式）
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>', 
                          content_type='text/xml')
    except Exception as e:
        logger.error(f"微信支付异步通知处理失败: {e}")
        return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[ERROR]]></return_msg></xml>', 
                          content_type='text/xml')


@csrf_exempt
@require_http_methods(["POST"])
def hupipay_notify(request):
    """虎皮椒支付异步通知"""
    try:
        # 获取虎皮椒POST过来的数据
        data = json.loads(request.body.decode('utf-8'))
        
        # 验证签名（这里需要实现具体的验证逻辑）
        # 如果验证通过，更新支付记录状态
        order_no = data.get('out_trade_no')
        status = data.get('status')
        
        # TODO: 实现具体的虎皮椒验签逻辑和订单状态更新
        
        logger.info(f"虎皮椒异步通知: 订单号={order_no}, 状态={status}")
        
        # 返回成功响应
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"虎皮椒异步通知处理失败: {e}")
        return JsonResponse({'status': 'fail'})
