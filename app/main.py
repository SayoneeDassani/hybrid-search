from fastapi import FastAPI, Query
from app.database import SessionLocal
from app.models import MagazineInfo, MagazineContent
from sqlalchemy.sql import text
from app.load_data import get_dummy_embedding

app = FastAPI(title="Hybrid Search API")

@app.get("/search")
def hybrid_search(q: str = Query(..., description="Search query")):
    session = SessionLocal()
    embedding = get_dummy_embedding(q)


    vector_sql = f"ARRAY[{', '.join([str(x) for x in embedding])}]::vector"
    query = text(f"""
    SELECT mi.id, mi.title, mi.author, mi.category, mi.publication_date,
           mc.content,
           (1 - (mc.vector_representation <#> {vector_sql})) AS similarity
    FROM magazine_info mi
    JOIN magazine_content mc ON mi.id = mc.magazine_id
    WHERE mi.title ILIKE :q OR mi.author ILIKE :q OR mc.content ILIKE :q
    ORDER BY similarity DESC
    LIMIT 10;
""")


    results = session.execute(query, {
        "vector": embedding,
        "q": f"%{q}%"
    }).fetchall()

    session.close()

    return [{
        "id": r.id,
        "title": r.title,
        "author": r.author,
        "category": r.category,
        "publication_date": r.publication_date,
        "content": r.content,
        "similarity": round(r.similarity, 4)
    } for r in results]
