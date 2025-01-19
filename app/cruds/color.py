from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.color import ColorRequest, ColorResponse
from fastapi import HTTPException

def create_color(db: Session, color: ColorRequest):
    try:
        query_str = text(
            """
            INSERT INTO COLORS (VALUE)
            OUTPUT inserted.ID, inserted.VALUE
            VALUES (:value);
            """
        )

        db_color = db.execute(
            query_str,
            {
                "value": color.value.upper(),
            },
        ).fetchone()
        db.commit()
        return ColorResponse(
            id=db_color.ID,
            value=db_color.VALUE,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_color(db: Session, color_id: int):
    try:
        query_str = text(
            """
            SELECT ID, VALUE
            FROM COLORS
            WHERE ID = :color_id;
            """
        )

        db_color = db.execute(query_str, {"color_id": color_id}).fetchone()
        return ColorResponse(
            id=db_color.ID,
            value=db_color.VALUE,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_colors(db: Session, skip: int = 0, limit: int = 100):
    try:
        query_str = text(
            """
            SELECT ID, VALUE
            FROM COLORS
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_colors = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        result = []
        for db_color in db_colors:
            result.append(
                ColorResponse(
                    id=db_color.ID,
                    value=db_color.VALUE,
                )
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_color(db: Session, color_id: int, color: ColorRequest):
    try:
        query_str = text(
            """
            UPDATE COLORS
            SET VALUE = :value
            WHERE ID = :color_id;
            """
        )

        db.execute(
            query_str,
            {
                "color_id": color_id,
                "value": color.value.upper(),
            },
        )
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_color(db: Session, color_id: int):
    try:
        query_str = text(
            """
            DELETE FROM COLORS
            WHERE ID = :color_id
            """
        )

        db.execute(query_str, {"color_id": color_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))