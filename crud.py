from sqlalchemy.orm import Session
import models, schemas
import bcrypt
from datetime import datetime


# def get_total_users(db: Session,
#     # skip: int = 0, limit: int = 100
#     ):
#     return db.query(models.User.id).count()



def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.deleted_at == None).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(
        models.User.id == id,
        models.User.deleted_at == None,
        models.Item.deleted_at == None).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(username=user.username,
                          password=hashed_password.decode('utf-8'),
                          # password=hashed_password, # for instead of postgresql
                          fullname=user.fullname,
                          email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db_user.fullname = db_user.fullname if user.fullname is None or user.fullname == "" else user.fullname
    db_user.email = db_user.email if user.email is None or user.email == "" else user.email
    db_user.is_active = db_user.is_active if user.is_active is None or user.is_active == "" else user.is_active
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    db_user.deleted_at = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user
    # db.delete(db_user)
    # db.commit()


def get_users(db: Session):
    return db.query(models.User).filter(models.User.deleted_at == None)


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.User = get_user_by_username(db, username=user.username)
    # print(db_user_info.password.decode('utf-8'))
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))


def create_new_item(db: Session, item: schemas.ItemBase):
    db_item = models.Item(title=item.title, content=item.content, owner_id=item.owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).first()
    db_item.title = item.title
    db_item.content = item.content
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_items(db: Session):
    return db.query(models.Item).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id,
                                        models.Item.deleted_at == None
                                        ).first()
