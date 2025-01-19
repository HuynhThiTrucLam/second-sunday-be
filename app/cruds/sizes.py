from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.sizes import SizeRequest, SizeResponse
from fastapi import HTTPException

def create_size(db: Session, size: SizeRequest) -> SizeResponse:
    try:
        query_str = text(
            """
            INSERT INTO SIZES (VALUE)
            OUTPUT inserted.ID, inserted.VALUE
            VALUES (:value);
            """
        )

        db_size = db.execute(
            query_str,
            {
                "value": size.value.upper(),
            },
        ).fetchone()
        db.commit()
        return SizeResponse(id=db_size.ID, value=db_size.VALUE)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_size(db: Session, size_id: int) -> SizeResponse:
    try:
        query_str = text(
            """
            SELECT ID, VALUE
            FROM SIZES
            WHERE ID = :size_id;
            """
        )

        db_size = db.execute(query_str, {"size_id": size_id}).fetchone()
        if db_size:
            return SizeResponse(id=db_size.ID, value=db_size.VALUE)
        else:
            raise HTTPException(status_code=404, detail="Size not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_sizes(db: Session, skip: int = 0, limit: int = 100) -> list[SizeResponse]:
    try:
        query_str = text(
            """
            SELECT ID, VALUE
            FROM SIZES
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_sizes = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        return [SizeResponse(id=size.ID, value=size.VALUE) for size in db_sizes]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_size(db: Session, size_id: int, size: SizeRequest) -> bool:
    try:
        query_str = text(
            """
            UPDATE SIZES
            SET VALUE = :value
            WHERE ID = :size_id;
            """
        )

        db.execute(
            query_str,
            {
                "size_id": size_id,
                "value": size.value.upper(),
            },
        )
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_size(db: Session, size_id: int) -> bool:
    try:
        query_str = text(
            """
            DELETE FROM SIZES
            WHERE ID = :size_id;
            """
        )

        db.execute(query_str, {"size_id": size_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))