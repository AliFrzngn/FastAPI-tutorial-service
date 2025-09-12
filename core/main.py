from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import random
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App says hello")
    yield
    print("App says goodbye")


app = FastAPI(lifespan=lifespan)


names_list = [
    {"id":1, "name": "ali"},
    {"id":2, "name": "maryam"},
    {"id":3, "name": "arousha"},
    {"id":4, "name": "zahra"},
    {"id":5, "name": "BAgher"}
]


@app.get("/")
def root():
    return JSONResponse(content = {"message": "Hello World!!!"}, status_code=status.HTTP_202_ACCEPTED)


@app.get("/names",status_code=status.HTTP_201_CREATED)
def retrieve_names_list(q : str | 
                        None = Query(
                            alias="search",
                              example="ali",
                              description="it will search the names"
                              ,default = None, max_length=50)
                              ):
    if q:
        return [item for item in names_list if item ["name"] == q]
    return names_list


@app.get("/names/{name_id}")
def retrieve_names_detail(name_id:int = Path(title = "object id in name",
                                             description="the id of the name in names"
                                             )):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Object Not Found")

@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name:str = Body(embed=True)):
    name_obj ={"id": random.randint(6,100), "name": name}
    names_list.append(name_obj)
    return name_obj

@app.put("/names/{name_id}",status_code=status.HTTP_200_OK)
def update_names_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Object Not Found")

@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content = {"detail": "Object Removed!"}, status_code = status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Object Not Found")

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}

@app.post("/upload_multiple")
async def upload_multiple(files: List[UploadFile]):
    return[
        {"filename": file.filename, "content_type": file.content_type}
        for file in files
    ]