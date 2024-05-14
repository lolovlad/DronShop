from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import UserService, OrderService, ShopService
from Server.Forms import UserForm, OrderUpdateForm, OrderItemUpdateForm

from Server.database import TypeOrder, StatusOrder

from Server.Models import state_order, type_order

manager_router = Blueprint("manager", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "manager_blueprint.user", "title": "Клиенты"},
    {"url": "manager_blueprint.order", "title": "Заказы"},
]


@manager_router.before_request
def is_manager():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "manager" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@manager_router.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", menu=menu, user=current_user)


@manager_router.route("/user", methods=["GET"])
@login_required
def user():
    service = UserService()
    users_entity = service.get_list_by_user()
    return render_template("user.html", menu=menu, user=current_user, users=users_entity)


@manager_router.route("/user/update/<uuid>", methods=["POST", "GET"])
@login_required
def user_update(uuid: str):
    form = UserForm()
    service = UserService()
    user = service.get_user_by_uuid(uuid)
    if request.method == "GET":

        form.name.data = user.name
        form.surname.data = user.surname
        form.patronymics.data = user.patronymics
        form.phone.data = user.phone
        form.email.data = user.email

        return render_template("user_update.html", menu=menu, user=current_user, user_target=user, form=form)
    else:
        if form.validate_on_submit():
            service.update_user(uuid,
                                form.name.data,
                                form.surname.data,
                                form.patronymics.data,
                                form.phone.data,
                                form.email.data)

        return redirect(url_for("manager_blueprint.user"))


@manager_router.route("/order", methods=["GET"])
@login_required
def order():
    service = OrderService()
    order_entity = service.get_list_order()
    return render_template("order.html", menu=menu, user=current_user, orders=order_entity, state_order=state_order,
                           type_order=type_order)


@manager_router.route("/order/update/<uuid>", methods=["POST", "GET"])
@login_required
def order_update(uuid: str):
    form = OrderUpdateForm()
    service_order = OrderService()
    service_shop = ShopService()
    workshop = service_shop.get_list_workshop()
    form.workshop.choices = [(g.trace_id, g.name) for g in workshop]

    form.state_order.choices = [(g.name, state_order[g.value]) for g in StatusOrder]

    if request.method == "GET":
        order = service_order.get_order(uuid)

        if order.type_order == TypeOrder.in_hall:
            workshop = service_order.get_workshop_by_address(order.address)
            form.workshop.data = workshop.trace_id
        else:
            form.address.data = order.address
        form.state_order.data = order.status_order.name
        return render_template("order_update.html", menu=menu,
                               user=current_user,
                               order=order,
                               form=form,
                               type_order=type_order)

    elif request.method == "POST":
        order = service_order.get_order(uuid)

        if order.type_order == TypeOrder.in_hall:
            address = service_shop.get_address_by_workshop_uuid(form.workshop.data)
        else:
            address = form.address.data

        service_order.update(uuid, address, form.state_order.data)
        return redirect(url_for("manager_blueprint.order"))


@manager_router.route("/order_cart/delete/<int:id_order>/<int:id_drone>", methods=["GET"])
@login_required
def delete_order_sweet_product(id_order: int, id_drone: int):
    if request.method == "GET":
        service = OrderService()
        service.delete_order_drone(id_order, id_drone)
        order = service.get_order_by_id(id_order)
        return redirect(url_for('manager_blueprint.order_update', uuid=order.trace_id))


@manager_router.route("/order/back/<int:id_order>", methods=["GET"])
@login_required
def back_order(id_order: int):
    if request.method == "GET":
        service = OrderService()
        order = service.get_order_by_id(id_order)
        return redirect(url_for("manager_blueprint.order_update", uuid=order.trace_id))


@manager_router.route("/order_cart/update/<int:id_order>/<int:id_drone>", methods=["POST", "GET"])
@login_required
def order_car_update(id_order: int, id_drone: int):
    service = OrderService()
    form = OrderItemUpdateForm()
    if request.method == "GET":
        drone_order = service.get_order_drone(id_order, id_drone)
        form.count.data = drone_order.count
        return render_template("order_drone_update.html",
                               menu=menu,
                               user=current_user,
                               product=drone_order,
                               form=form,
                               type_order=type_order)
    elif request.method == "POST":
        if form.validate_on_submit():
            service.update_order_drone(id_order, id_drone, form.count.data)
            return redirect(url_for("manager_blueprint.back_order", id_order=id_order))