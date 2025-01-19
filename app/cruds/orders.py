from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.orders import OrderRequest, OrderResponse, OrderDetailResponse
from fastapi import HTTPException
from datetime import datetime

def create_order(db: Session, order: OrderRequest) -> True:
    try:
        query_str = text(
            """
            INSERT INTO ORDERS (ACCOUNT_ID, CREATE_AT, SHIP_AMOUNT, DISCOUNT_ID, STATUS)
            OUTPUT inserted.ID, inserted.ACCOUNT_ID, inserted.CREATE_AT, inserted.CONFIRM_AT, inserted.SHIP_AMOUNT, inserted.DISCOUNT_ID, inserted.STATUS
            VALUES (:account_id, :create_at, :ship_amount, :discount_id, 'CONFIRM');
            """
        )

        db_order = db.execute(
            query_str,
            {
                "account_id": order.account_id,
                "create_at": datetime.now(),
                "ship_amount": order.ship_amount,
                "discount_id": order.discount_id if order.discount_id  and order.discount_id !=0 else None,
            },
        ).fetchone()
        db.commit()

        for detail in order.order_details:
            query_str = text(
                """
                INSERT INTO ORDERDETAIL (ORDER_ID, PRODUCT_VARIANT_ID, COUNT)
                VALUES (:order_id, :product_variant_id, :count);
                """
            )
            db.execute(
                query_str,
                {
                    "order_id": db_order.ID,
                    "product_variant_id": detail.product_variant_id,
                    "count": detail.count,
                },
            )

        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_order(db: Session, order_id: int) -> OrderResponse:
    try:
        query_str = text(
            """
            SELECT ID, ACCOUNT_ID, CREATE_AT, CONFIRM_AT, SHIP_AMOUNT, DISCOUNT_ID, STATUS, ACCOUNTS.USERNAME
            FROM ORDERS
            JOIN ACCOUNTS ON ORDERS.ACCOUNT_ID = ACCOUNTS.ID
            WHERE ID = :order_id;
            """
        )

        db_order = db.execute(query_str, {"order_id": order_id}).fetchone()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        query_str = text(
            """
            SELECT ID, ORDER_ID, PRODUCT_VARIANT_ID, COUNT
            FROM ORDERDETAIL
            WHERE ORDER_ID = :order_id;
            """
        )

        db_order_details = db.execute(query_str, {"order_id": order_id}).fetchall()
        order_details = [
            OrderDetailResponse(
                id=detail.ID,
                order_id=detail.ORDER_ID,
                product_variant_id=detail.PRODUCT_VARIANT_ID,
                count=detail.COUNT,
            )
            for detail in db_order_details
        ]

        return OrderResponse(
            id=db_order.ID,
            account_id=db_order.ACCOUNT_ID,
            create_at=db_order.CREATE_AT,
            confirm_at=db_order.CONFIRM_AT,
            ship_amount=db_order.SHIP_AMOUNT,
            discount_id=db_order.DISCOUNT_ID,
            status=db_order.STATUS,
            order_details=order_details,
            customer=db_order.USERNAME
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_orders(type: str, db: Session, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
    try:
        base_query = """
            SELECT 
                O.ID,
                O.ACCOUNT_ID,
                O.CREATE_AT,
                O.CONFIRM_AT,
                O.SHIP_AMOUNT,
                O.DISCOUNT_ID,
                O.STATUS,
                A.USERNAME
            FROM ORDERS O
            JOIN ACCOUNTS A ON O.ACCOUNT_ID = A.ID
        """

        if type != "ALL":
            base_query += " WHERE O.STATUS = :status"

        query_str = text(
            base_query + """
            ORDER BY O.ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        params = {"skip": skip, "limit": limit}
        if type != "ALL":
            params["status"] = type

        db_orders = db.execute(query_str, params).fetchall()
        orders = []
        for db_order in db_orders:
            query_str = text(
                """
                SELECT 
                    OD.ID,
                    OD.ORDER_ID,
                    OD.PRODUCT_VARIANT_ID,
                    OD.COUNT
                FROM ORDERDETAIL OD
                WHERE OD.ORDER_ID = :order_id;
                """
            )

            db_order_details = db.execute(query_str, {"order_id": db_order.ID}).fetchall()
            order_details = [
                OrderDetailResponse(
                    id=detail.ID,
                    order_id=detail.ORDER_ID,
                    product_variant_id=detail.PRODUCT_VARIANT_ID,
                    count=detail.COUNT,
                )
                for detail in db_order_details
            ]

            orders.append(OrderResponse(
                id=db_order.ID,
                account_id=db_order.ACCOUNT_ID,
                create_at=db_order.CREATE_AT,
                confirm_at=db_order.CONFIRM_AT,
                ship_amount=db_order.SHIP_AMOUNT,
                discount_id=db_order.DISCOUNT_ID,
                status=db_order.STATUS,
                order_details=order_details,
                customer=db_order.USERNAME,
            ))

        return orders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_order(db: Session, order_id: int, order: OrderRequest) -> bool:
    try:
        query_str = text(
            """
            UPDATE ORDERS
            SET ACCOUNT_ID = :account_id, CONFIRM_AT = :confirm_at, SHIP_AMOUNT = :ship_amount, DISCOUNT_ID = :discount_id, STATUS = :status
            WHERE ID = :order_id;
            """
        )

        db.execute(
            query_str,
            {
                "order_id": order_id,
                "account_id": order.account_id,
                "confirm_at": datetime.now(),
                "ship_amount": order.ship_amount,
                "discount_id": order.discount_id,
                "status": order.status,
            },
        )

        query_str = text(
            """
            DELETE FROM ORDERDETAIL WHERE ORDER_ID = :order_id;
            """
        )
        db.execute(query_str, {"order_id": order_id})

        for detail in order.order_details:
            query_str = text(
                """
                INSERT INTO ORDERDETAIL (ORDER_ID, PRODUCT_VARIANT_ID, COUNT)
                VALUES (:order_id, :product_variant_id, :count);
                """
            )
            db.execute(
                query_str,
                {
                    "order_id": order_id,
                    "product_variant_id": detail.product_variant_id,
                    "count": detail.count,
                },
            )

        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_order(db: Session, order_id: int) -> bool:
    try:
        query_str = text(
            """
            DELETE FROM ORDERS
            WHERE ID = :order_id;
            """
        )

        db.execute(query_str, {"order_id": order_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))