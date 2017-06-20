from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.views import APIView

from trymakeAPI.API_1_0.mod_customer.models import Customer


class AllCustomerView(APIView):
    def get(self, request):
        customer_list = Customer.objects.all()
        response = dict()
        response["customers"] = [i.serialize for i in customer_list]
        response["status"] = 'OK'
        response["success"] = True
        response["count"] = len(customer_list)
        return JsonResponse(response)


class CreateCustomer(APIView):
    def post(self, request):
        try:
            customer = Customer.create(request.POST["username"],
                                       request.POST["email"],
                                       request.POST["password"],
                                       request.POST["first_name"],
                                       request.POST["last_name"])
        except KeyError:
            return JsonResponse({"status":"fail","success":False,"reason":"Missing Data"})
        except IntegrityError as e:
            return JsonResponse({"status": "fail", "success": False, "reason": str(e)})

        return JsonResponse({"status":"ok","success":True,"username":customer.user.username})