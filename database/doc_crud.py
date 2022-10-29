from datetime import datetime

import bcrypt as bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_doc_by_id(db: Session, doc_id: int):
    return db.query(models.Document).filter(models.Document.doc_id == doc_id).first()

def get_docs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()


def upload_doc(db: Session, metaData: schemas.DocMetaData):
    db_doc = models.Document( doc_id=metaData.doc_id,
        name=metaData.name, user_id=metaData.user_id,
        data_created=datetime.now(), s3_bucket_path=metaData.s3_bucket_path
        )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def delete_doc(db: Session, doc_id: int):
    db.query(models.Document).filter(models.Document.doc_id == doc_id).delete()
    db.commit()
    return