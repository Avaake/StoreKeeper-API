from app.models import Supplier, db
from sqlalchemy.exc import IntegrityError
from typing import Union
from app.core import logger
from flask import jsonify, Response
from app.api.suppliers.schemas import CreateSupplierSchema, UpdateSupplierSchema
from sqlalchemy import func
from werkzeug.exceptions import NotFound


def create_supplier(data: CreateSupplierSchema) -> Supplier | tuple[Response, int]:
    try:
        supplier = Supplier(
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            address=data.address,
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "This supplier already exists"}), 400
    except Exception as err:
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_supplier_by_id(supplier_id) -> Supplier | tuple[Response, int]:
    try:
        supplier = Supplier.query.filter_by(id=supplier_id).first()
        if supplier is None:
            raise NotFound("Supplier not found")
        return supplier
    except NotFound as not_found_err:
        logger.info(f"NotFound error: {not_found_err}")
        return jsonify({"error": str(not_found_err)}), 404
    except Exception as err:
        logger.error(f"Unhandled exception: {err}")


def get_suppliers(
    supplier_name: Union[str, None] = None
) -> list[Supplier] | tuple[Response, int]:
    try:
        suppliers = Supplier.query.order_by(Supplier.id)
        # search
        if supplier_name:
            suppliers = suppliers.filter(
                func.lower(Supplier.name).ilike(f"%{supplier_name}%")
            )
        return suppliers.all()
    except Exception as err:
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def update_supplier(
    supplier_id: int, data: UpdateSupplierSchema
) -> Supplier | tuple[Response, int]:
    try:
        supplier = get_supplier_by_id(supplier_id=supplier_id)
        if isinstance(supplier, tuple):
            return supplier
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(supplier, key, value)
        return supplier
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return (
            jsonify(
                {
                    "error": "There was an issue processing your request. Please try again later."
                }
            ),
            422,
        )
    except Exception as err:
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def delete_supplier(supplier_id: int) -> None | tuple[Response, int]:
    try:
        supplier = get_supplier_by_id(supplier_id=supplier_id)
        if isinstance(supplier, tuple):
            return supplier
        db.session.delete(supplier)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return (
            jsonify(
                {
                    "error": "There was an issue processing your request. Please try again later."
                }
            ),
            422,
        )
    except Exception as err:
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500