from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.discount import DiscountRequest, DiscountResponse
from fastapi import HTTPException

def create_discount(db: Session, discount: DiscountRequest) -> DiscountResponse:
    try:
        query_str = text(
            """
            INSERT INTO DISCOUNT (code, type, START_DATE, HSD, QUANTITY, DESCRIPTION, TYPOF, VALUE)
            OUTPUT inserted.ID, inserted.code, inserted.type, inserted.START_DATE, inserted.HSD, inserted.QUANTITY, inserted.DESCRIPTION, inserted.TYPOF, inserted.VALUE
            VALUES (:code, :type, :start_date, :hsd, :quantity, :description, :typof, :value);
            """
        )

        db_discount = db.execute(
            query_str,
            {
                "code": discount.code,
                "type": discount.type,
                "start_date": discount.start_date,
                "hsd": discount.hsd,
                "quantity": discount.quantity,
                "description": discount.description,
                "typof": discount.typof,
                "value": discount.value,
            },
        ).fetchone()
        db.commit()
        return DiscountResponse(
            id=db_discount.ID,
            start_date=db_discount.START_DATE,
            hsd=db_discount.HSD,
            quantity=db_discount.QUANTITY,
            description=db_discount.DESCRIPTION,
            typof=db_discount.TYPOF,
            value=db_discount.VALUE,
            code=db_discount.code,
            type=db_discount.type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_discount(db: Session, discount_id: int) -> DiscountResponse:
    try:
        query_str = text(
            """
            SELECT ID, code, type, START_DATE, HSD, QUANTITY, DESCRIPTION, TYPOF, VALUE
            FROM DISCOUNT
            WHERE ID = :discount_id;
            """
        )

        db_discount = db.execute(query_str, {"discount_id": discount_id}).fetchone()
        if db_discount:
            return DiscountResponse(
                id=db_discount.ID,
                start_date=db_discount.START_DATE,
                hsd=db_discount.HSD,
                quantity=db_discount.QUANTITY,
                description=db_discount.DESCRIPTION,
                typof=db_discount.TYPOF,
                value=db_discount.VALUE,
                code=db_discount.code,
                type=db_discount.type
            )
        else:
            raise HTTPException(status_code=404, detail="Discount not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_discounts(db: Session, skip: int = 0, limit: int = 100) -> list[DiscountResponse]:
    try:
        query_str = text(
            """
            SELECT ID, code, type, START_DATE, HSD, QUANTITY, DESCRIPTION, TYPOF, VALUE
            FROM DISCOUNT
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_discounts = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        return [
            DiscountResponse(
                id=discount.ID,
                start_date=discount.START_DATE,
                hsd=discount.HSD,
                quantity=discount.QUANTITY,
                description=discount.DESCRIPTION,
                typof=discount.TYPOF,
                value=discount.VALUE,
                code=discount.code,
                type=discount.type
            )
            for discount in db_discounts
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_discount(db: Session, discount_id: int, discount: DiscountRequest) -> bool:
    try:
        query_str = text(
            """
            UPDATE DISCOUNT
            SET START_DATE = :start_date, HSD = :hsd, QUANTITY = :quantity, DESCRIPTION = :description, TYPOF = :typof, VALUE = :value, code = :code, type = :type
            WHERE ID = :discount_id;
            """
        )

        db.execute(
            query_str,
            {
                "discount_id": discount_id,
                "start_date": discount.start_date,
                "hsd": discount.hsd,
                "quantity": discount.quantity,
                "description": discount.description,
                "typof": discount.typof,
                "value": discount.value,
                "code": discount.code,
                "type": discount.type
            },
        )
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_discount(db: Session, discount_id: int) -> bool:
    try:
        query_str = text(
            """
            DELETE FROM DISCOUNT
            WHERE ID = :discount_id;
            """
        )

        db.execute(query_str, {"discount_id": discount_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))