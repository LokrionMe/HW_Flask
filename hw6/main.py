from typing import List
import databases
from pydantic import BaseModel, Field
import sqlalchemy
from fastapi import FastAPI
from werkzeug.security import generate_password_hash
from datetime import date

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("Users", metadata,
                         sqlalchemy.Column(
                             "id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("lastname", sqlalchemy.String(64)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(128)),)

goods = sqlalchemy.Table("Goods", metadata,
                         sqlalchemy.Column(
                             "id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(64)),
                         sqlalchemy.Column("description", sqlalchemy.Text),
                         sqlalchemy.Column("price", sqlalchemy.Float),)

orders = sqlalchemy.Table("Orders", metadata,
                          sqlalchemy.Column(
                              "id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column(
                              "id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id")),
                          sqlalchemy.Column("id_good", sqlalchemy.Integer,
                                            sqlalchemy.ForeignKey("Goods.id")),
                          sqlalchemy.Column("date", sqlalchemy.Date),
                          sqlalchemy.Column("status", sqlalchemy.String(40)),)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
app = FastAPI()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    lastname: str = Field(max_length=64)
    email: str = Field(max_length=128)
    password: str = Field(max_length=16)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    lastname: str = Field(max_length=64)
    email: str = Field(max_length=128)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name,
                                  email=user.email, lastname=user.lastname, password=generate_password_hash(user.password))
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


class GoodIn(BaseModel):
    name: str = Field(max_length=64)
    description: str = Field(max_length=500)
    price: float = Field


class Good(BaseModel):
    id: int
    name: str = Field(max_length=64)
    description: str = Field(max_length=500)
    price: float


@app.post("/goods/", response_model=Good)
async def create_good(good: GoodIn):
    query = goods.insert().values(name=good.name,
                                  description=good.description, price=good.price,)
    last_record_id = await database.execute(query)
    return {**good.model_dump(), "id": last_record_id}


@app.get("/goods/", response_model=List[Good])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@app.get("/goods/{good_id}", response_model=Good)
async def read_good(good_id: int):
    query = goods.select().where(goods.c.id == good_id)
    return await database.fetch_one(query)


@app.put("/goods/{good_id}", response_model=Good)
async def update_good(good_id: int, new_good: GoodIn):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.model_dump())
    await database.execute(query)
    return {**new_good.model_dump(), "id": good_id}


@app.delete("/goods/{good_id}")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    await database.execute(query)
    return {'message': 'Good deleted'}


class OrderIn(BaseModel):
    id_user: int
    id_good: int
    date: date
    status: str = Field(max_length=40)


class Order(BaseModel):
    id: int
    id_user: int
    id_good: int
    date: date
    status: str = Field(max_length=40)


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(id_user=order.id_user,
                                   id_good=order.id_good, date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(
        orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
