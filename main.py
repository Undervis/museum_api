import io

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import db
from starlette.responses import StreamingResponse

app = FastAPI()


class Date(BaseModel):
    date: str
    title: str
    description: str


@app.post("/add_date/uid/{uid}")
async def add(date: Date, uid: str):
    if not db.check_uid(uid):
        id = db.add_date(date.date, date.title, date.description)
        return {'error': 0, 'message': 'Success', "id": id}
    else:
        return {'error': 4, 'message': 'Access denied'}


@app.post("/edit_date/uid/{uid}/date_id/{id}")
async def edit(date: Date, uid: str, id: int):
    if not db.check_uid(uid):
        db.edit_date(date.date, date.title, date.description, id)
        return {'error': 0, 'message': 'Success', "id": id}
    else:
        return {'error': 4, 'message': 'Access denied'}


@app.post("/load_image/uid/{uid}/date_id/{id}")
async def load(id: int, uid: str, file: UploadFile = File(None)):
    if not db.check_uid(uid):
        try:
            with open("images/" + str(file.filename), 'wb+') as f:
                f.write(file.file.read())
            db.upload_img("images/" + str(file.filename), id)
        except:
            return {'error': 2, 'message': 'File uploading error'}
        return {'error': 0, 'message': 'Success'}
    else:
        return {'error': 4, 'message': 'Access denied'}


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
                     'description': date[2], 'date': date[3],
                     'image': date[4]})
    return data
