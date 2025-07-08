import uvicorn

from fastapi import FastAPI, HTTPException, Response, status


app = FastAPI(debug=True, docs_url="/")

users = []


@app.get("/get_users/")
async def get_all_users():
    return {"users": users}


@app.post("/get_users/{name}")
async def add_user(name: str, response: Response):
    if name in users:
        raise HTTPException(status_code=400, detail=f"Name '{name}' already exists")
    users.append(name)
    response.status_code = status.HTTP_201_CREATED
    return {"name": name}

@app.delete("/delete_users/{name}")
async def delete_user(name: str, response: Response):
    if name not in users:
        raise HTTPException(status_code=404, detail=f"Name '{name}' not found")
    users.remove(name)
    response.status_code = status.HTTP_200_OK
    return {"message": f"Name '{name}' deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)