from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/send")
async def send(info : Request):
    req_info = await info.json()
    return {
        "name" : "Pick Up Vamsi",
        "date" : "12/12/2022",
        "time": "12:01",
        "tod" : "am",
        "all_day" : False
    }