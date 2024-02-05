from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from databases import Database
import uvicorn

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)

metadata = MetaData()


clients = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("firstname", String(50)),
    Column("lastname", String(50)),
    Column("email", String(128))
)


products = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("description", String(255)),
    Column("price", Float)
)


orders = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_client", Integer, foreign_key=clients.c.id),
    Column("id_product", Integer, foreign_key=products.c.id),
    Column("date_order", Date),
    Column("status", String, default="Создан")
)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)


class ClientIn(BaseModel):
    firstname: str = Field(..., max_length=50)
    lastname: str = Field(max_length=50)
    email: str = Field(..., max_length=128)


class Client(BaseModel):
    id: int
    firstname: str = Field(..., max_length=50)
    lastname: str = Field(max_length=50)
    email: str = Field(..., max_length=128)


class ProductIn(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field(max_length=255)
    price: float


class Product(BaseModel):
    id: int
    name: str = Field(..., max_length=50)
    description: str = Field(max_length=255)
    price: float


class OrderIn(BaseModel):
    id_client: int
    id_product: int
    date_order: datetime
    status: str

class Order(BaseModel):
    id: int
    id_client: int
    id_product: int
    date_order: datetime
    status: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/clients/")
async def read_clients():
    query = clients.select()
    return await database.fetch_all(query)


@app.get("/clients/{client_id}")
async def read_clients_id(client_id: int):
    query = clients.select().where(clients.c.id == client_id)
    return await database.fetch_one(query)


@app.post("/clients/")
async def create_client(client: ClientIn):
    query = clients.insert().values(firstname=client.firstname, lastname=client.lastname, email=client.email)
    last_record_id = await database.execute(query)
    return {"added_client": {"id": last_record_id, "firstname": client.firstname}}


@app.put("/clients/{client_id}")
async def update_client(client_id: int, client: Client):
    query = clients.update().where(clients.c.id == client_id).values(firstname=client.firstname, lastname=client.lastname, email=client.email)
    await database.execute(query)
    # return {"id": client_id, "name": client.name}
    return {**client.dict(), "id": client_id}



@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    query = clients.delete().where(clients.c.id == client_id)
    await database.execute(query)
    return {"message": "Client with id: {} has been deleted".format(client_id)}


@app.get("/products/")
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}")
async def read_products_id(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.post("/products/")
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {"added_product": {"id": last_record_id, "name": product.name}}


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    query = products.update().where(products.c.id == product_id).values(name=product.name, description=product.description, price=product.price)
    await database.execute(query)
    return {**product.dict(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_products(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product with id: {} has been deleted".format(product_id)}


@app.get("/orders/")
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}")
async def read_orders_id(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/orders/")
async def create_order(order: OrderIn):
    query = orders.insert().values(id_client=order.id_client, id_product=order.id_product, date_order=order.date_order, status=order.status)
    last_record_id = await database.execute(query)
    return "Good!"


@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    query = orders.update().where(orders.c.id == order_id).values(id_client=order.id_client, id_product=id_product.description, date_order=order.date_order, status=order.status)
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_orders(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Order with id: {} has been deleted".format(order_id)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)