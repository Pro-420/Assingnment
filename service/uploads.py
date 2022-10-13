from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status
from pandas import read_excel
from fastapi.responses import JSONResponse
from database.service import Database
from os import getcwd, remove
import time


router = APIRouter()
database = Database()

@router.post("/file")
async def fileUploader(request: Request, file: UploadFile = File(...)):
    try:
        filename = getcwd()+"\\uploads\\"+str(time.time())+"-"+file.filename
        f = open(f'{filename}', 'wb')
        content = await file.read()
        f.write(content)
        f.close()
        data = read_excel(filename)
        data['exp']=data['exp'].astype(str)
        data.reset_index(inplace=True)
        status = database.data_insert(data=data)
        if status:
            remove(filename)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content="File inserted successfully")
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File is not uploaded successfully")
        