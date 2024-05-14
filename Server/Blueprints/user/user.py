from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import ShopService
from Server.Forms import CreateOrderForm, OrderItemUpdateForm

from Server.database import TypeOrder

from Server.Models import state_order, type_order

user_router = Blueprint("user", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "index", "title": "главная"},
    {"url": "shop", "title": "магазин"},
]


@user_router.before_request
def is_user():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "user" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@user_router.route("/car/add/<uuid>")
@login_required
def add_car(uuid: str):
    cart = session.get("car")
    if uuid not in session["car"]:
        cart[uuid] = 0
    cart[uuid] += 1
    session["car"] = cart
    return redirect(f"/shop")


@user_router.route("/car")
@login_required
def car():
    cart: dict = session.get("car")
    service = ShopService()
    order_drone_product = service.get_list_product_by_uuid(list(cart.keys()), cart)
    sum_cart = 0
    for prod in order_drone_product:
        sum_cart += prod.count * prod.price
    return render_template("car.html", menu=menu, user=current_user, products=order_drone_product, sum_cart=sum_cart)


@user_router.route("/car/delete/<uuid>")
@login_required
def delete_car(uuid: str):
    cart: dict = session.get("car")
    cart.pop(uuid)
    session["car"] = cart
    return redirect(url_for("user_blueprint.car"))


@user_router.route("/car/update/<uuid>", methods=["GET", "POST"])
@login_required
def update_car(uuid: str):
    form = OrderItemUpdateForm()
    if request.method == "GET":
        cart: dict = session.get("car")

        form.count.data = cart[uuid]
        return render_template("update_item_order.html",
                               menu=menu,
                               user=current_user,
                               form=form,
                               uuid_item=uuid)
    elif request.method == "POST":
        count = form.count.data
        cart: dict = session.get("car")
        if count <= 0:
            return redirect(url_for("user_blueprint.delete_car", uuid=uuid))
        else:
            cart[uuid] = count
        session["car"] = cart
        print(url_for("user_blueprint.car"))
        return redirect(url_for("user_blueprint.car"))


@user_router.route("/list_order", methods=["GET"])
@login_required
def list_order():
    service = ShopService()
    list_order_json = service.get_list_order_by_user_id(current_user.user.id)
    return render_template("list_order.html", menu=menu, user=current_user, orders=list_order_json, state_order=state_order)


@user_router.route("/info_order/<uuid>", methods=["GET"])
@login_required
def info_order(uuid: str):
    service = ShopService()
    order = service.get_order_by_uuid(uuid)
    return render_template("info_order.html", menu=menu, user=current_user, order=order, type_order=type_order, state_order=state_order)


@user_router.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    form = CreateOrderForm()
    service = ShopService()
    workshop = service.get_list_workshop()
    form.workshops.choices = [(g.trace_id, g.name) for g in workshop]
    if request.method == "GET":
        cart = session.get("car")
        form.type_order.data = 1
        order_sweet_product = service.get_list_product_by_uuid(list(cart.keys()), cart)
        sum_cart = 0
        for prod in order_sweet_product:
            sum_cart += prod.count * prod.price

        return render_template("create_order.html",
                               menu=menu,
                               user=current_user,
                               form=form,
                               sum_cart=sum_cart,
                               products=order_sweet_product)
    elif request.method == "POST":
            address = ""
            type_order = TypeOrder.in_hall
            if int(form.type_order.data) == TypeOrder.in_hall.value:
                address = service.get_address_by_workshop_uuid(form.workshops.data)
                print("Тип заказа: в зале")
            else:
                type_order = TypeOrder.with_myself
                address = f"{form.city.data} {form.street.data} {form.home.data} {form.apartment.data} {form.floor.data}"
                print("Тип заказа: Доставка")
            cart = session.get("car")
            order = service.create_order(type_order, address, form.description.data, cart, current_user.user.id)
            if order is not None:
                session["car"] = {}
                return redirect(url_for('user_blueprint.info_order',  uuid=order.trace_id))
            else:
                return redirect(url_for("user_blueprint.create_order"))