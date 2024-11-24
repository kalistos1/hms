from .models import Notification

def default(request):
    if 'selection_data_obj' in request.session:
        total_selected_items = len(request.session['selection_data_obj'])
    else:
        total_selected_items = 0
    
    try:
        noti = Notification.objects.filter(user=request.user, seen=False)
    except:
        noti = None

    return {
        "total_selected_items": total_selected_items,
        "noti": noti,
    }


# def cart_data(request):
#     cart = request.session.get('cart', {})
#     total_items = sum(item['quantity'] for item in cart.values())
#     return {
#         'cart': cart,
#         'total_cart_items': total_items
#     }
