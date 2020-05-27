import os

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from .. import db
from ..models.document import Document

UPLOAD_FOLDER = "/tmp/upload"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(content_type):
    return content_type.rsplit("/")[1].lower() in ALLOWED_EXTENSIONS


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def process_file(file):
    filename = secure_filename(file.filename)
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0, 0)
    return filename, file_size, file.content_type


def check_file(filename, file_size, content_type):
    if filename == "":
        response_object = {"status": "error", "message": "File not found"}
        return response_object, 404

    if file_size == 0:
        response_object = {"status": "error", "message": "File empty"}
        return response_object, 404

    if file_size > MAX_CONTENT_LENGTH:
        response_object = {"status": "error", "message": "File exceeds max upload size"}
        return response_object, 413  # payload too large

    if not allowed_file(content_type):
        response_object = {"status": "error", "message": "File extension not allowed"}
        return response_object, 406  # not acceptable
    return None


def save_document(document_name, file):
    filename, file_size, content_type = process_file(file)
    check_file(filename, file_size, content_type)
    abs_path = os.path.join(UPLOAD_FOLDER, filename)
    new_document = Document(
        name=document_name.title(),
        file_name=filename,
        file_type=content_type,
        file_size="".join(
            [
                "{:.1f} kB".format(file_size / 1024)
                if file_size / 1024 < 1000
                else "{:.1f} MB".format(file_size / 1024 / 1024)
            ]
        ),
    )
    file.save(abs_path)
    try:
        commit_changes(new_document)
        response_object = {
            "status": "success",
            "message": "Successfully saved.",
        }
        return response_object, 201
    except Exception:
        response_object = {"status": "error", "message": "Something went wrong"}
        return response_object, 500


def get_document(id):
    return Document.query.filter_by(id=id).first()


def update():
    db.session.commit()


def edit_document(document, document_name, file):
    if document_name:
        document.name = document_name.title()
    if file:
        filename, file_size, content_type = process_file(file)
        check_file(filename, file_size, content_type)
        document.file_name = filename
        document.file_type = content_type
        document.file_size = "".join(
            [
                "{:.1f} kB".format(file_size / 1024)
                if file_size / 1024 < 1000
                else "{:.1f} MB".format(file_size / 1024 / 1024)
            ]
        )
        abs_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(abs_path)
    response_object = {
        "status": "success",
        "message": "Successfully updated.",
    }
    try:
        # document.update()
        db.session.commit()
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 400


def delete_document(document):
    # document.delete()
    try:
        db.session.delete(document)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 400


def get_all_documents():
    return Document.query.all()


def get_all_sme_documents(sme_id):
    return Document.query.filter_by(sme_id=sme_id)


def get_all_funding_detail_documents(funding_detail_id):
    return Document.query.filter_by(funding_detail_id=funding_detail_id)
