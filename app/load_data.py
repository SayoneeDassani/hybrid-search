import pandas as pd
from app.database import SessionLocal
from app.models import MagazineInfo, MagazineContent
import numpy as np
from datetime import datetime
from dateutil import parser


def get_dummy_embedding(text: str) -> list:
    # Replace with real embeddings if needed
    np.random.seed(abs(hash(text)) % (2**32))
    vec = np.random.rand(1536).astype(np.float32)
    return (vec / np.linalg.norm(vec)).tolist()

def load_data(info_path: str, content_path: str):
    session = SessionLocal()

    # Read CSVs
    df_info = pd.read_csv(info_path)
    df_content = pd.read_csv(content_path)

    for _, row in df_info.iterrows():
        magazine = MagazineInfo(
            id=int(row["id"]),
            title=row["title"],
            author=row["author"],
            publication_date = parser.parse(str(row["publication_date"])),
            category=row["category"]
        )
        session.merge(magazine)

    for _, row in df_content.iterrows():
        content_text = row["content"]
        embedding = get_dummy_embedding(content_text)
        content = MagazineContent(
            id=int(row["id"]),
            magazine_id=int(row["magazine_id"]),
            content=content_text,
            vector_representation=embedding
        )
        session.merge(content)

    session.commit()
    session.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    load_data("data/magazine_info.csv", "data/magazine_content.csv")
