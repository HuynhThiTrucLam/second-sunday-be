from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.category import CategoryRequest, CategoryResponse
from fastapi import HTTPException
from datetime import datetime


def create_category(db: Session, category: CategoryRequest):
    try:
        query_str = text(
            """
            INSERT INTO CATEGORYS (NAME)
            OUTPUT inserted.ID, inserted.NAME
            VALUES (:name);
            """
        )

        db_category = db.execute(
            query_str,
            {
                "name": category.name.upper(),
            },
        ).fetchone()
        db.commit()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_category(db: Session, category_id: int):
    try:
        query_str = text(
            """
            SELECT ID as id, NAME as name
            FROM CATEGORYS
            WHERE ID = :category_id;
            """
        )

        db_category = db.execute(query_str, {"category_id": category_id}).fetchone()
        return db_category

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    try:
        query_str = text(
            """
            SELECT ID as id, NAME as name
            FROM CATEGORYS
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_categories = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        return db_categories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_category(db: Session, category_id: int, category: CategoryRequest):
    try:
        query_str = text(
            """
            UPDATE CATEGORYS
            SET NAME = :name
            WHERE ID = :category_id
            OUTPUT inserted.ID, inserted.NAME;
            """
        )

        db_category = db.execute(
            query_str,
            {
                "category_id": category_id,
                "name": category.name.upper(),
            },
        ).fetchone()
        db.commit()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_category(db: Session, category_id: int):
    try:
        query_str = text(
            """
            DELETE FROM CATEGORYS
            WHERE ID = :category_id
            OUTPUT deleted.ID, deleted.NAME;
            """
        )

        db_category = db.execute(query_str, {"category_id": category_id}).fetchone()
        db.commit()
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))