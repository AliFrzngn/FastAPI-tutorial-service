from fastapi import FastAPI
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
    return {"message": "Hello, World!"}


@app.get("/names")
def retrieve_names_list():
    return names_list


@app.get("/names/{name_id}")
def retrieve_names_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"detail": "Object Not Found!"}

@app.post("/names")
def create_name(name:str):
    name_obj ={"id": random.randint(6,100), "name": name}
    names_list.append(name_obj)
    return name_obj

@app.put("/names/{name_id}")
def update_names_detail(name_id: int, name: str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return name
    return {"detail": "object not found"}

@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "object removed succesfully"}
    return {"detail": "object not found"}