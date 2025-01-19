from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.feedbacks import FeedbackRequest, FeedbackResponse
from fastapi import HTTPException
from datetime import datetime

def create_feedback(db: Session, feedback: FeedbackRequest) -> FeedbackResponse:
    try:
        query_str = text(
            """
            INSERT INTO FEEDBACKS (CREATE_AT, ACCOUNT_ID, PRODUCT_ID, RATING, CONTENT, REPLY_CONTENT)
            OUTPUT inserted.ID, inserted.CREATE_AT, inserted.ACCOUNT_ID, inserted.PRODUCT_ID, inserted.RATING, inserted.CONTENT, inserted.REPLY_CONTENT
            VALUES (:create_at, :account_id, :product_id, :rating, :content, :reply_content);
            """
        )

        db_feedback = db.execute(
            query_str,
            {
                "create_at": datetime.now(),
                "account_id": feedback.account_id,
                "product_id": feedback.product_id,
                "rating": float(feedback.rating),
                "content": feedback.content,
                "reply_content": feedback.reply_content,
            },
        ).fetchone()
        db.commit()
        return FeedbackResponse(
            id=db_feedback.ID,
            create_at=db_feedback.CREATE_AT,
            account_id=db_feedback.ACCOUNT_ID,
            product_id=db_feedback.PRODUCT_ID,
            rating=db_feedback.RATING,
            content=db_feedback.CONTENT,
            reply_content=db_feedback.REPLY_CONTENT,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_feedback(db: Session, feedback_id: int) -> FeedbackResponse:
    try:
        query_str = text(
            """
            SELECT ID, CREATE_AT, ACCOUNT_ID, PRODUCT_ID, RATING, CONTENT, REPLY_CONTENT
            FROM FEEDBACKS
            WHERE ID = :feedback_id;
            """
        )

        db_feedback = db.execute(query_str, {"feedback_id": feedback_id}).fetchone()
        if db_feedback:
            return FeedbackResponse(
                id=db_feedback.ID,
                create_at=db_feedback.CREATE_AT,
                account_id=db_feedback.ACCOUNT_ID,
                product_id=db_feedback.PRODUCT_ID,
                rating=db_feedback.RATING,
                content=db_feedback.CONTENT,
                reply_content=db_feedback.REPLY_CONTENT,
            )
        else:
            raise HTTPException(status_code=404, detail="Feedback not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100) -> list[FeedbackResponse]:
    try:
        query_str = text(
            """
            SELECT ID, CREATE_AT, ACCOUNT_ID, PRODUCT_ID, RATING, CONTENT, REPLY_CONTENT
            FROM FEEDBACKS
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_feedbacks = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        return [
            FeedbackResponse(
                id=feedback.ID,
                create_at=feedback.CREATE_AT,
                account_id=feedback.ACCOUNT_ID,
                product_id=feedback.PRODUCT_ID,
                rating=feedback.RATING,
                content=feedback.CONTENT,
                reply_content=feedback.REPLY_CONTENT,
            )
            for feedback in db_feedbacks
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_feedback(db: Session, feedback_id: int, feedback: FeedbackRequest) -> bool:
    try:
        query_str = text(
            """
            UPDATE FEEDBACKS
            SET ACCOUNT_ID = :account_id, PRODUCT_ID = :product_id, RATING = :rating, CONTENT = :content, REPLY_CONTENT = :reply_content
            WHERE ID = :feedback_id;
            """
        )

        db.execute(
            query_str,
            {
                "feedback_id": feedback_id,
                "account_id": feedback.account_id,
                "product_id": feedback.product_id,
                "rating": feedback.rating,
                "content": feedback.content,
                "reply_content": feedback.reply_content,
            },
        )
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_feedback(db: Session, feedback_id: int) -> bool:
    try:
        query_str = text(
            """
            DELETE FROM FEEDBACKS
            WHERE ID = :feedback_id;
            """
        )

        db.execute(query_str, {"feedback_id": feedback_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))