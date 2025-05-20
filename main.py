from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from rembg import remove

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5500"] if using Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-bg")
async def remove_background(image: UploadFile = File(...)):
    input_path = f"{UPLOAD_DIR}/{image.filename}"
    output_path = f"{OUTPUT_DIR}/no-bg-{image.filename}"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    with open(input_path, "rb") as i:
        input_data = i.read()
        output_data = remove(input_data)

    with open(output_path, "wb") as o:
        o.write(output_data)

    return FileResponse(output_path, media_type="image/png", filename=f"no-bg-{image.filename}")
