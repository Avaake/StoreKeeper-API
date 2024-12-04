from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.api.suppliers import crud
from app.core import settings
from app.core import logger
from app.api.suppliers.schemas import (
    CreateSupplierSchema,
    ReadSupplierSchema,
    SearchSupplierSchema,
    UpdateSupplierSchema,
)

bp = Blueprint("suppliers", __name__, url_prefix=settings.api_prefix.suppliers)


@bp.route("", methods=["POST"])
def create_supplier():
    try:
        data = CreateSupplierSchema(**request.json)
        supplier = crud.create_supplier(data=data)
        if isinstance(supplier, tuple):
            return supplier
        return (
            jsonify(
                {
                    "massage": "Supplier created successfully",
                    "supplier": ReadSupplierSchema.model_validate(
                        supplier
                    ).model_dump(),
                }
            ),
            201,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("", methods=["GET"])
def get_suppliers():
    try:
        suppliers = crud.get_suppliers()
        return jsonify(
            {
                "suppliers": [
                    ReadSupplierSchema.model_validate(supplier).model_dump()
                    for supplier in suppliers
                ]
            }
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/search", methods=["GET"])
def search_supplier_with_name():
    try:
        qwery_params = SearchSupplierSchema(**request.args)
        suppliers = crud.get_suppliers(supplier_name=qwery_params.q.lower()) or []
        return jsonify(
            {
                "suppliers": [
                    ReadSupplierSchema.model_validate(supplier).model_dump()
                    for supplier in suppliers
                ]
            }
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id: int):
    try:
        supplier = crud.get_supplier_by_id(supplier_id=supplier_id) or []
        if isinstance(supplier, tuple):
            return supplier
        return (
            jsonify(
                {"supplier": ReadSupplierSchema.model_validate(supplier).model_dump()}
            ),
            200,
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again lat"}), 500


@bp.route("<int:supplier_id>", methods=["PATCH"])
def update_supplier(supplier_id: int):
    try:
        data = UpdateSupplierSchema(**request.json)
        supplier = crud.update_supplier(supplier_id=supplier_id, data=data)
        if isinstance(supplier, tuple):
            return supplier
        return (
            jsonify(
                {"supplier": ReadSupplierSchema.model_validate(supplier).model_dump()}
            ),
            200,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id: int):
    try:
        supplier = crud.delete_supplier(supplier_id=supplier_id)
        if isinstance(supplier, tuple):
            return supplier
        return jsonify(""), 204
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
