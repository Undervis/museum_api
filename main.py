import io

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import db
from starlette.responses import StreamingResponse

app = FastAPI()


class Date(BaseModel):
    day: int
    month: int
    year: int
    title: str
    description: str


@app.post("/add_date")
async def add(date: Date):
    id = db.add_date(date.day, date.month, date.year, date.title, date.description)
    return {'error': 0, 'message': 'Success', "id": id}


@app.post("/edit_date/date_id/{id}")
async def edit(date: Date, id: int):
    db.edit_date(date.day, date.month, date.year, date.title, date.description, id)
    return {'error': 0, 'message': 'Success', "id": id}


@app.post("/load_image/date_id/{id}")
async def load(id: int, file: UploadFile = File(None)):
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
    return data
