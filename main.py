import io

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import db
from starlette.responses import StreamingResponse

app = FastAPI()


class Date(BaseModel):
    id: int
    day: int
    month: int
    year: int
    title: str
    description: str


class DateId(BaseModel):
    id: int


@app.post("/add_date")
async def add(date: Date):
    id = db.add_date(date.day, date.month, date.year, date.title, date.description)
    return {'error': 0, 'message': 'Success', "id": id}


@app.post("/edit_date")
async def edit(date: Date):
    db.edit_date(date.day, date.month, date.year, date.title, date.description, date.id)
    return {'error': 0, 'message': 'Success', "id": id}


@app.delete("/delete_date/{id}")
async def delete(id: int):
    db.delete_date(id)
    return {"success": 1}


@app.post("/load_image")
async def load(id: str = Form(None), file: UploadFile = File(None)):
    try:
        with open("images/" + str(file.filename), 'wb+') as f:
            f.write(file.file.read())
        db.upload_img("images/" + str(file.filename), id)
    except:
        return {'error': 2, 'message': 'File uploading error'}
    return {'error': 0, 'message': 'Success'}


@app.get('/images/{name}')
async def get_img(name: str):
    with open('images/' + name, 'rb') as f:
        img = f.read()
    return StreamingResponse(io.BytesIO(img), media_type="image")


@app.get("/get_dates")
async def get():
    data = []
    for date in db.get_dates():
        data.append({'id': date[0], 'title': date[1],
                     'description': date[2], 'day': date[3], 'month': date[4], 'year': date[5],
                     'image': date[6]})
    if len(data) == 0:
        data.append({"id": 0, "title": "Нулевая запись",
                     "description": "После добавления новой даты запись удалится сама",
                     "day": 1, "month": 1, "year": 1970, "image": "images/null_image.jpg"})
    return data


@app.get("/get_date/{id}")
async def get_date(id: int):
    data = db.get_date(id)
    return {'id': data[0], 'title': data[1],
            'description': data[2], 'day': data[3], 'month': data[4], 'year': data[5],
            'image': data[6]}
