from app.api.supplies.schemas import CreateSupplySchema, UpdateSupplySchema
from app.api.suppliers.crud import get_supplier_by_id
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from flask import jsonify, Response
from app.models import db, Supply
from app.core import logger


def create_supply(data: CreateSupplySchema) -> Supply | tuple[Response, int]:
    try:
        supplier = get_supplier_by_id(supplier_id=data.supplier_id)
        if isinstance(supplier, tuple):
            return supplier
        supply = Supply(
            product_name=data.product_name,
            quantity=data.quantity,
            price=data.price,
            supplier_id=data.supplier_id,
            delivery_date=data.delivery_date,
            status=data.status,
        )
        db.session.add(supply)
        db.session.commit()

        return supply
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


def get_supply_by_id(supply_id: int) -> Supply | tuple[Response, int]:
    try:
        supply = Supply.query.filter_by(id=supply_id).first()
        if supply is None:
            raise NotFound(f"Supply {supply_id} not found")
        return supply
    except NotFound as not_found_err:
        logger.info(f"NotFound error: {not_found_err}")
        return jsonify({"error": str(not_found_err)}), 404
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_supplies() -> list[Supply] | tuple[Response, int]:
    try:
        supply = Supply.query.order_by(Supply.id).all()
        return supply
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def update_supply(
    supply_id: int, data: UpdateSupplySchema
) -> Supply | tuple[Response, int]:
    try:
        supply = get_supply_by_id(supply_id=supply_id)
        if isinstance(supply, tuple):
            return supply
        for kay, value in data.model_dump(exclude_unset=True).items():
            setattr(supply, kay, value)
        db.session.commit()
        return supply
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


def delete_supply(supply_id: int) -> None | tuple[Response, int]:
    try:
        supply = get_supply_by_id(supply_id=supply_id)
        if isinstance(supply, tuple):
            return supply
        db.session.delete(supply)
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
