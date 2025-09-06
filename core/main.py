from fastapi import FastAPI, Query, status, HTTPException, Path
from fastapi.responses import JSONResponse
import random

app = FastAPI()


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

@app.post("/names")
def create_name(name:str):
    name_obj ={"id": random.randint(6,100), "name": name}
    names_list.append(name_obj)
    return name_obj

@app.put("/names/{name_id}",status_code=status.HTTP_200_OK)
def update_names_detail(name_id: int, name: str):
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