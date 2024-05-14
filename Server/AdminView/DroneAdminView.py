from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField, FileUploadField
from random import getrandbits

from markupsafe import Markup

from Server.database import Drone
from uuid import uuid4
import os
import os.path as op
from flask import url_for

from werkzeug.utils import secure_filename


file_path = os.path.abspath(os.path.dirname(__name__))


def name_gen_image(model, file_data) -> str:
    return str(getrandbits(20))


def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('file-%s%s' % parts)


def list_thumbnail(view, content, model: Drone, name):
    url = url_for('static', filename=os.path.join('img/', model.image))
    return Markup(f"<img src={url} width=100>")


def list_file(view, content, model: Drone, name):
    url = url_for('static', filename=os.path.join('instructions/', model.instructions))
    return Markup(f"<a href={url}>Документ</a>")

def list_description(view, content, model: Drone, name):
    text = model.description
    if len(model.description) > 40:
        text = model.description[:41] + "..."
    return Markup(f"<p>{text}</p>")


class DroneAdminView(ModelView):
    form_columns = [
        'name',
        'price_drone',
        'weight_drone',
        'width',
        'length',
        'height',
        'description',
        'components',
        'type',
        'image',
        "instructions"
    ]
    form_extra_fields = {
        'image': ImageUploadField('Image',
                                  base_path=os.path.join(file_path, "static/img/"),
                                  url_relative_path='img/',
                                  namegen=name_gen_image,
                                  allowed_extensions=['jpg', 'png', 'jpeg'],
                                  max_size=(1200, 780, True),
                                  thumbnail_size=(200, 200, True)),
        'instructions': FileUploadField('Instruction',
                                        base_path=os.path.join(file_path, "static/instructions/"),
                                        relative_path='instructions/',
                                        namegen=prefix_name,
                                        allowed_extensions=['docx', 'pdf'],)
    }

    column_formatters = {
        "image": list_thumbnail,
        "instructions": list_file,
        "description": list_description
    }

    def create_form(self, obj=None):
        return super(DroneAdminView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(DroneAdminView, self).edit_form(obj)

    def on_model_change(self, form, model: Drone, is_created):
        model.trace_id = str(uuid4())
