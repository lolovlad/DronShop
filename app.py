from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_uuid import FlaskUUID
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from Server.database import db, Role, User, Drone, Component, Workshop, Type
from Server.Models import UserSession

from Server.Repository import UserRepository
from Server.Models import GetUser
from Server.Service import LoginService, UserService, ShopService
from Server.AdminView import *
from Server.Forms import LoginForm, RegistrationForm, SearchDroneProduct

from Server.Blueprints.user.user import user_router
from Server.Blueprints.manager.manager import manager_router
from Server.Blueprints.worker.worker import worker_router

app = Flask(__name__)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = '/Files'


app.register_blueprint(manager_router, name="manager_blueprint", url_prefix="/manager")
app.register_blueprint(user_router, name="user_blueprint", url_prefix="/user")
app.register_blueprint(worker_router, name="worker_blueprint", url_prefix="/worker")

flask_uuid = FlaskUUID()

db.init_app(app)
flask_uuid.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)


route = {
    "worker": "/worker",
    "manager": "manager_blueprint.index",
    "admin": "/admin",
    "user": "/"
}

menu = [
    {"url": "index", "title": "главная"},
    {"url": "shop", "title": "товары"},
]


@login_manager.user_loader
def load_user(id_user) -> UserSession:
    repo = UserRepository(db.session)
    try:
        return UserSession(GetUser.model_validate(repo.get_user(int(id_user)), from_attributes=True))
    except:
        return UserSession(None)


@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" in user_roles:
            return redirect(route["worker"])
        elif "manager" in user_roles:
            return redirect(url_for(route["manager"]))
        elif "admin" in user_roles:
            return redirect(route["admin"])
        else:
            return render_template("index.html", exception="", menu=menu, user=current_user)

    else:
        return render_template("index.html", exception="", menu=menu, user=current_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            login_service = LoginService()
            user = login_service.login_user(form.email.data, form.password.data)
            if user is None:
                return redirect("login")
            login_user(UserSession(user))
            session["car"] = {}
            return redirect("/")
        return redirect("login")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            user_service = UserService()
            user = user_service.registration(
                form.name.data,
                form.surname.data,
                form.patronymics.data,
                form.phone.data,
                form.email.data,
                form.password.data
            )
            login_user(UserSession(user))
            session["car"] = {}
            return redirect(url_for('index'))
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)


@app.route("/shop", methods=["GET", "POST"])
def shop():
    form = SearchDroneProduct()
    shop_service = ShopService()
    args = request.args
    tag = args.get("type")

    form.tag.choices = [(i.id, i.name) for i in shop_service.get_list_tag()]
    form.tag.choices.append((0, "все"))
    if request.method == "GET":
        if tag is None or int(tag) == 0:
            sweet_products = shop_service.get_drone()
        else:
            sweet_products = shop_service.get_drone_by_tag(int(tag))

        return render_template("shop.html",
                               title="Магазин",
                               menu=menu,
                               user=current_user,
                               sweet_products=sweet_products,
                               form=form)
    elif request.method == "POST":
        return redirect(url_for("shop", type=form.tag.data))


@app.route("/product/<uuid>/", methods=["GET"])
def product(uuid: str):
    if request.method == "GET":
        service = ShopService()
        sweet_product = service.get_product(uuid)
        return render_template("product_information.html",
                               title=sweet_product.name,
                               menu=menu,
                               user=current_user,
                               product=sweet_product)


@app.route("/init_app/<password>", methods=["GET"])
def create_user_admin(password):
    if request.method == "GET":
        if password == "AdminCreate":
            roles = [
                Role(
                    name="worker",
                    description="worker"
                ),
                Role(
                    name="manager",
                    description="manager"
                ),
                Role(
                    name="admin",
                    description="admin"
                ),
                Role(
                    name="user",
                    description="user"
                ),
            ]

            db.session.add_all(roles)
            db.session.commit()

            admin_user = User(
                name="Иван",
                surname="Иван",
                patronymics="Иван",

                phone="9033499161",
                email="admin@admin.ru",

                role=roles[2],
                passport_series="0000",
                passport_number="123456"
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.commit()

            return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


admin = Admin(app, name="Панель Админ", template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(UserAdminView(User, db.session, name="Пользователь"))
admin.add_view(ModelView(Role, db.session, name="Роли"))
admin.add_view(DroneAdminView(Drone, db.session, name="Модели дронов"))
admin.add_view(ModelView(Component, db.session, name="Комплектующие"))
admin.add_view(ModelView(Type, db.session, name="Типы дронов"))
admin.add_view(WorkshopAdminView(Workshop, db.session, name="Цеха"))

admin.add_link(LogoutMenuLink(name="Выход", category="", url="/logout"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
