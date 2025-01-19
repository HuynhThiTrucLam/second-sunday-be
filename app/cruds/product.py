from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas import product as schemas
from fastapi import HTTPException

def get_product(db: Session, product_id: int):
    query_str = text(
        """
        SELECT
            p.*,
            pv.id as product_variant_id,
            pv.QUAN_IN_STOCK,
            s.VALUE as size_name,
            s.id as size_id,
            c.VALUE as color_name,
            c.id as color_id,
            i.URL1, i.URL2, i.URL3, i.URL4,
            p.POLICY,
            p.CARE_INSTRUCTION,
            p.RATING,
            p.CATEGORY_ID,
            cat.NAME as category_name
        FROM PRODUCTS AS p
        LEFT JOIN PRODUCT_VARIANT AS pv ON pv.PRODUCT_ID = p.ID
        LEFT JOIN SIZES AS s ON s.ID = pv.SIZE_ID
        LEFT JOIN COLORS AS c ON c.ID = pv.COLOR_ID
        LEFT JOIN IMAGES AS i ON i.ID = pv.IMAGE_ID
        LEFT JOIN CATEGORYS AS cat ON cat.ID = p.CATEGORY_ID
        WHERE p.ID = :product_id
        ORDER BY p.ID, pv.COLOR_ID, pv.SIZE_ID
        """
    )
    products = db.execute(query_str, {"product_id": product_id}).fetchall()

    if not products:
        return None

    result = {
        "id": products[0].ID,
        "name": products[0].NAME,
        "description": products[0].DESCRIPTION,
        "price": products[0].PRICE,
        "category": {'id':products[0].CATEGORY_ID, 'name': products[0].category_name},
        "policy": products[0].POLICY,
        "care_instructions": products[0].CARE_INSTRUCTION,
        "rating": products[0].RATING,
        "colors": [],
    }
    for product in products:
        existing_color = next(
            (c for c in result["colors"] if c["id"] == product.color_id), None
        )
        if existing_color:
            existing_size = next(
                (s for s in existing_color["sizes"] if s["id"] == product.size_id), None
            )
            if existing_size:
                existing_size["inventory"] += product.QUAN_IN_STOCK
            else:
                existing_color["sizes"].append(
                    {
                        "id": product.size_id,
                        "name": product.size_name,
                        "inventory": product.QUAN_IN_STOCK,
                    }
                )
        else:
            result["colors"].append(
                {
                    "id": product.color_id,
                    "name": product.color_name,
                    "images": [product.URL1, product.URL2, product.URL3, product.URL4],
                    "sizes": [
                        {
                            "id": product.size_id,
                            "name": product.size_name,
                            "inventory": product.QUAN_IN_STOCK,
                        }
                    ],
                }
            )

    return result

def get_products(db: Session, skip: int = 0, limit: int = 10, type: str = "ALL"):
    query_str = """
        SELECT
            p.*,
            p.id as PROD_ID,
            pv.id as product_variant_id,
            pv.QUAN_IN_STOCK,
            s.VALUE as size_name,
            s.id as size_id,
            c.VALUE as color_name,
            c.id as color_id,
            i.*,
            p.POLICY,
            p.CARE_INSTRUCTION,
            p.RATING,
            p.CATEGORY_ID,
            cat.NAME as category_name,
            p.MATERIAL
        FROM PRODUCTS AS p
        LEFT JOIN PRODUCT_VARIANT AS pv ON pv.PRODUCT_ID = p.ID
        LEFT JOIN SIZES AS s ON s.ID = pv.SIZE_ID
        LEFT JOIN COLORS AS c ON c.ID = pv.COLOR_ID
        LEFT JOIN IMAGES AS i ON i.ID = pv.IMAGE_ID
        LEFT JOIN CATEGORYS AS cat ON cat.ID = p.CATEGORY_ID
        """
    if type != "ALL":
        query_str += " WHERE p.CATEGORY_ID = :type"

    query_str = text(query_str + """
        ORDER BY p.ID, pv.COLOR_ID, pv.SIZE_ID
        OFFSET :skip ROWS
        FETCH NEXT :limit ROWS ONLY;
    """)
    products = db.execute(query_str, {"skip": skip, "limit": limit, "type": type}).fetchall()

    result = []
    for product in products:
        existing_product = next((p for p in result if p["id"] == product.ID), None)
        if existing_product:
            existing_color = next(
                (c for c in existing_product["colors"] if c["id"] == product.color_id),
                None,
            )
            if existing_color:
                existing_size = next(
                    (s for s in existing_color["sizes"] if s["id"] == product.size_id),
                    None,
                )
                if existing_size:
                    existing_size["inventory"] += product.QUAN_IN_STOCK
                else:
                    existing_color["sizes"].append(
                        {
                            "id": product.size_id,
                            "name": product.size_name,
                            "inventory": product.QUAN_IN_STOCK,
                        }
                    )
            else:
                existing_product["colors"].append(
                    {
                        "id": product.color_id,
                        "name": product.color_name,
                        "images": [product.URL1, product.URL2, product.URL3, product.URL4],
                        "sizes": [
                            {
                                "id": product.size_id,
                                "name": product.size_name,
                                "inventory": product.QUAN_IN_STOCK,
                            }
                        ],
                    }
                )
        else:
            product_data = {
                "id": product.PROD_ID,
                "name": product.NAME,
                "description": product.DESCRIPTION,
                "price": product.PRICE,
                "material": product.MATERIAL,
                "category_id": product.CATEGORY_ID,
                "policy": product.POLICY,
                "care_instructions": product.CARE_INSTRUCTION,
                "rating": product.RATING,
                "category": {'id':product.CATEGORY_ID, 'name': product.category_name},
                "colors": [
                    {
                        "id": product.color_id,
                        "name": product.color_name,
                        "images": [product.URL1, product.URL2, product.URL3, product.URL4],
                        "sizes": [
                            {
                                "id": product.product_variant_id,
                                "name": product.size_name,
                                "inventory": product.QUAN_IN_STOCK,
                            }
                        ],
                    }
                ],
            }
            result.append(product_data)

    return result

def create_product(db: Session, product: schemas.ProductRequest):
    query_str = text(
        """
        SELECT ID FROM PRODUCTS WHERE NAME = :name
        """
    )
    result = db.execute(query_str, {"name": product.name})
    db_product = result.fetchone()

    if db_product:
        db_product_id = db_product[0]
    else:
        query_str = text(
            """
            INSERT INTO PRODUCTS (NAME, PRICE, DESCRIPTION, CATEGORY_ID, POLICY, CARE_INSTRUCTION, MATERIAL)
            OUTPUT inserted.ID
            VALUES (:name, :price, :description , :category_id, :policy, :care_instructions, :material)
            """
        )
        result = db.execute(
            query_str,
            {
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "category_id": product.category_id,
                "policy": product.policy,
                "care_instructions": product.care_instructions,
                "material": product.material,
            },
        )
        db_product_id = result.fetchone()[0]

    color_ids = []
    for color in product.colors:
        query_str = text(
            """
            SELECT ID, VALUE FROM COLORS WHERE VALUE = :color
            """
        )
        result = db.execute(query_str, {"color": color.name})
        db_color = result.fetchone()

        if not db_color:
            query_str = text(
                """
                INSERT INTO COLORS (VALUE)
                OUTPUT inserted.ID, inserted.VALUE
                VALUES (:color)
                """
            )
            result = db.execute(query_str, {"color": color.name})
            db_color_id = result.fetchone()
        else:
            db_color_id = db_color

        images_str = (
            ",".join(color.images) if isinstance(color.images, list) else color.images
        )

        image_sql = text(
            """
                INSERT INTO IMAGES (URL1, URL2, URL3, URL4)
                OUTPUT inserted.ID as id
                VALUES (:url1, :url2, :url3, :url4)
            """
        )
        image_result = db.execute(
            image_sql,
            {
                "url1": color.images[0],
                "url2": color.images[1] if len(color.images) > 1 else None,
                "url3": color.images[2] if len(color.images) > 2 else None,
                "url4": color.images[3] if len(color.images) > 3 else None,
            },
        )
        image_result = image_result.fetchone()
        
        color_ids.append(
            {
                "id": db_color_id.ID,
                "name": db_color_id.VALUE,
                "images": images_str.split(","),
                "sizes": [],
            }
        )
        for size in color.sizes:
            query_str = text(
                """
                SELECT ID, VALUE FROM SIZES WHERE VALUE = :size
                """
            )
            result = db.execute(query_str, {"size": size.name})
            db_size = result.fetchone()

            if not db_size:
                query_str = text(
                    """
                    INSERT INTO SIZES (VALUE)
                    OUTPUT inserted.ID, inserted.VALUE
                    VALUES (:size)
                    """
                )
                result = db.execute(query_str, {"size": size.name})
                db_size_id = result.fetchone()
            else:
                db_size_id = db_size

            query_str = text(
                """
                SELECT ID FROM PRODUCT_VARIANT WHERE PRODUCT_ID = :product_id AND COLOR_ID = :color_id AND SIZE_ID = :size_id
                """
            )
            result = db.execute(
                query_str,
                {
                    "product_id": db_product_id,
                    "color_id": db_color_id.ID,
                    "size_id": db_size_id.ID,
                },
            )
            db_product_variant = result.fetchone()
            if db_product_variant:
                raise HTTPException(
                    status_code=400,
                    detail="Product already exists with the same color and size",
                )
            query_str = text(
                """
                INSERT INTO PRODUCT_VARIANT (PRODUCT_ID, COLOR_ID, SIZE_ID, QUAN_IN_STOCK, IMAGE_ID)
                VALUES (:product_id, :color_id, :size_id, :inventory, :image_id)
                """
            )
            db.execute(
                query_str,
                {
                    "product_id": db_product_id,
                    "color_id": db_color_id.ID,
                    "size_id": db_size_id.ID,
                    "inventory": size.inventory,
                    "image_id": image_result.id,  # Assuming image_id is handled separately
                },
            )
            color_ids[-1]["sizes"].append(
                {
                    "id": db_size_id.ID,
                    "name": db_size_id.VALUE,
                    "inventory": size.inventory,
                }
            )
    db.commit()

    return schemas.ProductResponse(
        colors=color_ids,
        description=product.description,
        id=db_product_id,
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        category={'id':product.category_id, 'name': "Category Name"},
        policy=product.policy,
        care_instructions=product.care_instructions,
        material=product.material,
        rating=product.rating,
    )

def update_product(db: Session, product_id: int, product: schemas.ProductRequest):
    query_str = text(
        """
        SELECT ID FROM PRODUCTS WHERE ID = :product_id
        """
    )
    result = db.execute(query_str, {"product_id": product_id})
    db_product = result.fetchone()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure the rating is within the valid range
    if not (1.0 <= product.rating <= 5.0):
        raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 5.0")

    # Ensure the price is within a reasonable range
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price must be a positive value")

    query_str = text(
        """
        UPDATE PRODUCTS
        SET NAME = :name, PRICE = :price, DESCRIPTION = :description, CATEGORY_ID = :category_id, POLICY = :policy, CARE_INSTRUCTION = :care_instructions
        WHERE ID = :product_id
        """
    )
    db.execute(
        query_str,
        {
            "name": product.name,
            "price": int(product.price),
            "description": product.description,
            "category_id": product.category_id,
            "policy": product.policy,
            "care_instructions": product.care_instructions,
            "product_id": product_id,
        },
    )

    for color in product.colors:
        query_str = text(
            """
            SELECT ID, VALUE FROM COLORS WHERE VALUE = :color
            """
        )
        result = db.execute(query_str, {"color": color.name})
        db_color = result.fetchone()

        if not db_color:
            query_str = text(
                """
                INSERT INTO COLORS (VALUE)
                OUTPUT inserted.ID, inserted.VALUE
                VALUES (:color)
                """
            )
            result = db.execute(query_str, {"color": color.name})
            db_color_id = result.fetchone()
        else:
            db_color_id = db_color

        images_str = (
            ",".join(color.images) if isinstance(color.images, list) else color.images
        )

        image_sql = text(
            """
                INSERT INTO IMAGES (URL1, URL2, URL3, URL4)
                OUTPUT inserted.ID as id
                VALUES (:url1, :url2, :url3, :url4)
            """
        )
        image_result = db.execute(
            image_sql,
            {
                "url1": color.images[0],
                "url2": color.images[1] if len(color.images) > 1 else None,
                "url3": color.images[2] if len(color.images) > 2 else None,
                "url4": color.images[3] if len(color.images) > 3 else None,
            },
        )
        image_result = image_result.fetchone()

        for size in color.sizes:
            query_str = text(
                """
                SELECT ID, VALUE FROM SIZES WHERE VALUE = :size
                """
            )
            result = db.execute(query_str, {"size": size.name})
            db_size = result.fetchone()

            if not db_size:
                query_str = text(
                    """
                    INSERT INTO SIZES (VALUE)
                    OUTPUT inserted.ID, inserted.VALUE
                    VALUES (:size)
                    """
                )
                result = db.execute(query_str, {"size": size.name})
                db_size_id = result.fetchone()
            else:
                db_size_id = db_size

            query_str = text(
                """
                SELECT ID FROM PRODUCT_VARIANT WHERE PRODUCT_ID = :product_id AND COLOR_ID = :color_id AND SIZE_ID = :size_id
                """
            )
            result = db.execute(
                query_str,
                {
                    "product_id": product_id,
                    "color_id": db_color_id.ID,
                    "size_id": db_size_id.ID,
                },
            )
            db_product_variant = result.fetchone()

            if db_product_variant:
                query_str = text(
                    """
                    UPDATE PRODUCT_VARIANT
                    SET QUAN_IN_STOCK = :inventory, IMAGE_ID = :image_id
                    WHERE PRODUCT_ID = :product_id AND COLOR_ID = :color_id AND SIZE_ID = :size_id
                    """
                )
                db.execute(
                    query_str,
                    {
                        "inventory": size.inventory,
                        "product_id": product_id,
                        "color_id": db_color_id.ID,
                        "size_id": db_size_id.ID,
                        "image_id": image_result.id,
                    },
                )
            else:
                query_str = text(
                    """
                    INSERT INTO PRODUCT_VARIANT (PRODUCT_ID, COLOR_ID, SIZE_ID, QUAN_IN_STOCK, IMAGE_ID)
                    VALUES (:product_id, :color_id, :size_id, :inventory, :image_id)
                    """
                )
                db.execute(
                    query_str,
                    {
                        "product_id": product_id,
                        "color_id": db_color_id.ID,
                        "size_id": db_size_id.ID,
                        "inventory": size.inventory,
                        "image_id": image_result.id,
                    },
                )
    db.commit()

    return True

def delete_product(db: Session, product_id: int):
    query_str = text(
        """
        SELECT ID FROM PRODUCTS WHERE ID = :product_id
        """
    )
    result = db.execute(query_str, {"product_id": product_id})
    db_product = result.fetchone()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    query_str = text(
        """
        DELETE FROM PRODUCTS WHERE ID = :product_id
        """
    )
    db.execute(query_str, {"product_id": product_id})
    db.commit()

    return {"message": "Product deleted successfully"}
