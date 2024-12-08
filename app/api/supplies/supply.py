from app.api.supplies.schemas import (
    CreateSupplySchema,
    ReadSupplySchema,
    UpdateSupplySchema,
)
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from app.core import settings, logger
from pydantic import ValidationError
from app.api.supplies import crud

bp = Blueprint("supplies", __name__, url_prefix=settings.api_prefix.supplies)


@bp.route("", methods=["POST"])
@jwt_required()
def create_supplies():
    try:
        data = CreateSupplySchema(**request.json)
        supply = crud.create_supply(data)
        if isinstance(supply, tuple):
            return supply

        return (
            jsonify(
                {
                    "message": "Supply created successfully",
                    "supply": ReadSupplySchema.model_validate(supply).model_dump(),
                }
            ),
            201,
        )

    except ValidationError as err:
        logger.info(f"Validation Error: {err.errors()}")
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


@bp.route("", methods=["GET"])
@jwt_required()
def get_supplies():
    try:
        supplies = crud.get_supplies()
        if isinstance(supplies, tuple):
            return supplies

        return (
            jsonify(
                {
                    "supplies": [
                        ReadSupplySchema.model_validate(supply).model_dump()
                        for supply in supplies
                    ],
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


@bp.route("<int:supply_id>", methods=["GET"])
@jwt_required()
def get_supply(supply_id: int):
    try:
        supply = crud.get_supply_by_id(supply_id=supply_id)
        if isinstance(supply, tuple):
            return supply

        return (
            jsonify(
                {
                    "supply": ReadSupplySchema.model_validate(supply).model_dump(),
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


@bp.route("<int:supply_id>", methods=["PATCH"])
@jwt_required()
def update_supply(supply_id: int):
    try:
        data = UpdateSupplySchema(**request.json)
        supply = crud.update_supply(supply_id=supply_id, data=data)
        if isinstance(supply, tuple):
            return supply
        return (
            jsonify(
                {
                    "supply": ReadSupplySchema.model_validate(supply).model_dump(),
                }
            ),
            200,
        )
    except ValidationError as err:
        logger.info(f"Validation Error: {err.errors()}")
        return jsonify({"error": "validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


@bp.route("<int:supply_id>", methods=["DELETE"])
@jwt_required()
def delete_supply(supply_id: int):
    try:
        supply = crud.delete_supply(supply_id=supply_id)
        if isinstance(supply, tuple):
            return supply
        return jsonify(""), 204
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500
