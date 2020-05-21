from django.shortcuts import render

from cart.cart import Cart
from .models import OrderItem
from .forms import OrderForm

def order_create(request):
    # 장바구니에 존재하는 상품 정보 받아오기
    cart = Cart(request)
    # 주문 정보가 입력 완료된 상황(결제 폼 작성 완료하여 POST 형태로 request를 받은 상황)
    if request.method == "POST":
        form = OrderForm(request.POST)
        # 작성한 폼 validation 진행
        if form.is_valid():
            order = form.save()
            for item in cart:
                # 장바구니에 들어있는 모든 상품 정보를 OrderItem 모델에 저장
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            return render(request, 'order/order_created.html', {'order': order})
    # 주문 정보가 입력되지 않은 상황(처음 결제페이지로 이동한 상황)
    else:
        form = OrderForm()

    return render(request, 'order/order_create.html', {'form':form})