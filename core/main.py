from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from typing import List
import random
from contextlib import asynccontextmanager
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema
from database import Base, engine, get_db, Person
from sqlalchemy.orm import Session
 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App says hello")
    Base.metadata.create_all(engine)
    yield
    print("App says goodbye")


app = FastAPI(lifespan=lifespan)


names_list = [
    {"id":1, "name": "ali"},
    {"id":2, "name": "maryam"},
    {"id":3, "name": "arousha"},
    {"id":4, "name": "zahra"},
    {"id":5, "name": "bagher"}
]


@app.get("/")
def root():
    return JSONResponse(content = {"message": "Hello World!!!"}, status_code=status.HTTP_202_ACCEPTED)


@app.get("/names", response_model=List[PersonResponseSchema])
def retrieve_names_list(q : str | 
                        None = Query(
                            alias="search",
                              example="ali",
                              description="it will search the names"
                              ,default = None, max_length=50),
                              db:Session = Depends(get_db)
                              ):
    query = db.query(Person)
    if q:
        query = query.filter_by(name=q)
    result = query.all()
    #if q:
    #    return [item for item in names_list if item ["name"] == q]
    return result


@app.get("/names/{name_id}", response_model= PersonResponseSchema)
def retrieve_names_detail(name_id:int = Path(title = "object id in name",
                                             description="the id of the name in names"
                                             ),
                                             db:Session = Depends(get_db)):
    #for name in names_list:
    #    if name["id"] == name_id:
    #        return name
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object Not Found")
    

@app.post("/names", status_code=status.HTTP_201_CREATED, response_model= PersonResponseSchema)
def create_name(request : PersonCreateSchema,db:Session = Depends(get_db)):
    #name_obj = {"id": random.randint(6,100), "name": person.name}
    #names_list.append(name_obj)
    new_person = Person(name=request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@app.put("/names/{name_id}",status_code=status.HTTP_200_OK, response_model= PersonResponseSchema)
def update_names_detail(request: PersonUpdateSchema, name_id: int = Path(), db:Session = Depends(get_db)):
    #for item in names_list:
    #    if item["id"] == name_id:
    #        item["name"] = person.name
    #        return item
        
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Object Not Found")
    

@app.delete("/names/{name_id}")
def delete_name(name_id: int, db:Session = Depends(get_db)):
    #for item in names_list:
    #    if item["id"] == name_id:
    #        names_list.remove(item)
    #        return JSONResponse(content = {"detail": "Object Removed!"}, status_code = status.HTTP_200_OK)
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content = {"detail": "Object Removed!"}, status_code = status.HTTP_200_OK)
    else:
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