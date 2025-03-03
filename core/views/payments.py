import razorpay
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, View, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs

from core.mixins import DataProviderMixin
from core.models.payments import Payment
from core.models import Journal
from core.razorpay import initiate_payment, client


class PaymentView(DataProviderMixin, TemplateView):
    template_name = "payments/payments.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_data()
        ctx.update(
            {
                "journals": Journal.objects.all(),
            }
        )
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        data["order_id"] = initiate_payment(
            int(data["amount"]), data["currency"].upper()
        )
        payment = Payment.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            country=data.get("country"),
            amount=data.get("amount"),
            currency=data.get("currency"),
            remarks=data.get("remarks"),
            rzp_order_id=data.get("order_id"),
        )
        payment.save()
        data["RAZORPAY_API_KEY"] = settings.RAZORPAY_API_KEY
        return JsonResponse(json.dumps(data), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class PaymentCallbackView(DataProviderMixin, View):

    def post(self, request, *args, **kwargs):
        data = parse_qs(request.body.decode())
        order_id = data.get("razorpay_order_id", [""])[0]
        payment_id = data.get("razorpay_payment_id", [""])[0]
        signature = data.get("razorpay_signature", [""])[0]

        print(order_id, payment_id, signature)
        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            payment = Payment.objects.get(rzp_order_id=order_id)
            payment.rzp_payment_id = payment_id
            payment.rzp_signature = signature
            payment.payment_verified = True
            payment.save()
            return redirect("payments-success")
        except razorpay.errors.SignatureVerificationError as e:
            return redirect("payments-failed")


class PaymentSuccessView(DataProviderMixin, TemplateView):
    template_name = "payments/success.html"


class PaymentFailedView(DataProviderMixin, TemplateView):
    template_name = "payments/failed.html"
