from django.shortcuts import render,redirect

from django.contrib import messages

from decouple import config

from django.db.models import Sum

from django.urls import reverse_lazy

from django.views.generic import View,TemplateView,UpdateView,DetailView

from store.forms import SignUpForm,SignInForm,UserProfileForm

from store.models import UserProfile,Project,CartItems,OrderSummary,Cart

from django.contrib.auth import authenticate,login


class SignUpview(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,'register.html',{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"REGISTERED SUCCESSFULLY")

            return redirect("signin")
        
        else:

            messages.error(request,"REGISTRATION FAILED")

            return render(request,'register.html',{"form":form_instance})



class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,'login.html',{'form':form_instance})


    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_obj=authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                return redirect('index')

        return render(request,'login.html',{'form':form_instance}) 


class IndexView(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(owner=request.user)

        return render(request,self.template_name,{"projects":qs })



class ProfileUpdateView(UpdateView):

    model=UserProfile

    form_class=UserProfileForm

    template_name='profile_update.html'

    success_url=reverse_lazy("index")


class ProjectDetailView(DetailView):

    template_name='project_detail.html'

    context_object_name="project"

    model=Project



class AddToCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_obj=Project.objects.get(id=id)

        CartItems.objects.create(

                                    cart_object=request.user.basket,
                                    project_object=project_obj

        )

        return redirect("index")


class MyCartView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)

        total=request.user.basket.cart_total

        return render(request,'cart.html',{"cartitems":qs,"total":total,})



class CartDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        CartItems.objects.get(id=id).delete()

        return redirect("cart")


KEY_SECRET=config("KEY_SECRET")

KEY_ID=config("KEY_ID") 
import razorpay
class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        
        total=request.user.basket.cart_total*100

        data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        #create order object

           
        order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get("id"),total=request.user.basket.cart_total)
           
        #    product_obj=ci.product_object

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)


        for ci in cart_items:

            order_summary_obj.project_object.add(ci.project_object)

            print("==========================",order_summary_obj)

        order_summary_obj.save()
                

        print(payment)

        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }

        return render(request,'payment.html',{"context":context})


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")

class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        order_summary_obj=OrderSummary.objects.get(order_id=request.POST.get("razorpay_order_id"))

        login(request,order_summary_obj.user_object)

        # 'razorpay_payment_id': ['pay_Osc4W3SzwsS9D4'], 'razorpay_order_id': ['order_Osc45PLWmmuS2r'], 'razorpay_signature': ['0ddd337bace49384729e5bb28dcb3b115e6b41df29bd0d4e6ef189d81748931d'

        try:
            client.utility.verify_payment_signature(request.POST)

            print("payment success")

            order_id=request.POST.get("razorpay_order_id")


            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)

            

            

            cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

            for ci in cart_items:
                ci.is_order_placed=True

                ci.save()

        except:
            print("payment failed")

        
        return redirect("index")









































