from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/submit")
async def submit_data(request: Request):
    data = await request.json()
    print("from frontend:", data)
    return {"message": "ok"}
