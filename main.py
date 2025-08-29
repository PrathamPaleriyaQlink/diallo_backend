from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form
from get_transcribe import transcribe_audio, transcribe_audio_openai, transcribe_audio_deepgram
from get_analysis import get_call_analysis
from mongo_utils import update_data, get_all_docs, get_data_by_id
import uuid, os, shutil, subprocess

app = FastAPI(
    title="Qlink iDAC backend API",
    version="0.1.0",
    redoc_url=None,
    docs_url="/api/docs",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TRANSCRIBE_FUNCTIONS = {
    "groq": transcribe_audio,
    "openai": transcribe_audio_openai,
    "deepgram": transcribe_audio_deepgram
}

@app.get("/")
async def root():
    return {"message": "Welcome to Call Analyzer for Diallo by Qlink"}

@app.get("/ping")
def ping():
    """Ping endpoint to check if the server is running."""
    return {"message": "Qlink backend API is up and running"}

@app.post("/transcribe")
async def transcribe(
    tts_model: str,
    file: UploadFile = File(...),
    agent_name: str = Form(...),
    patient_name: str = Form(...),
    agent_phone_number: str = Form(...)
):

    # Store values in lowercase
    agent_name_var = agent_name.lower()
    patient_name_var = patient_name.lower()
    agent_phone_number_var = agent_phone_number.lower()

    ext = file.filename.split(".")[-1].lower()
    temp_filename = f"temp_{uuid.uuid4().hex}.{ext}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    try:
        # Convert GSM → WAV (fastest) or MP3 if needed
        if ext == "gsm":
            wav_filename = f"temp_{uuid.uuid4().hex}.wav"
            subprocess.run(["ffmpeg", "-y", "-i", temp_filename, wav_filename], check=True)
            os.remove(temp_filename)
            temp_filename = wav_filename
            ext = "wav"

        elif ext not in ["wav", "mp3"]:
            mp3_filename = f"temp_{uuid.uuid4().hex}.mp3"
            subprocess.run(["ffmpeg", "-y", "-i", temp_filename, mp3_filename], check=True)
            os.remove(temp_filename)
            temp_filename = mp3_filename
            ext = "mp3"

        transcribe_func = TRANSCRIBE_FUNCTIONS.get(tts_model.lower())
        if not transcribe_func:
            return {
                "success": False,
                "response": f"Invalid tts_model: {tts_model}. Use one of {list(TRANSCRIBE_FUNCTIONS.keys())}."
            }
        transcription = transcribe_func(temp_filename)

        if transcription:
            analysis = get_call_analysis(transcribe=transcription)

            if analysis:
                id = update_data(
                    agent_name=agent_name_var,
                    patient_name=patient_name_var,
                    agent_phone_number=agent_phone_number_var,
                    analystics=analysis,
                    transcribe=transcription
                )

                return {
                    "success": True,
                    "response": id,
                    "analysis": analysis
                }
        
        return {
            "success": False,
            "response": "Error Processing Data."
        }
    
    except Exception as e:
        return {
            "success": False,
            "response": str(e)
        }
    finally:
        os.remove(temp_filename)

@app.get("/docs")
async def fetch_call_by_id(doc_id: str):
    """
    Fetch a single call document by its ID.
    """
    try:
        doc = get_data_by_id(doc_id)
        if not doc:
            return {"success": False, "response": "No Data Found"}
        return {"success": True, "response": doc}
    except Exception as e:
        raise {"success": True, "response": f"Error occuered: {e}"}
    
@app.get("/calls")
async def fetch_all_calls():
    """
    Fetch all call documents with selected fields.
    """
    try:
        docs = get_all_docs()
        return {"success": True, "data": docs}
    except Exception as e:
        raise {"success": True, "response": f"Error occuered: {e}"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)