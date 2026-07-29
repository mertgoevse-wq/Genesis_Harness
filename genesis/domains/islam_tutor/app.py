from fastapi import FastAPI, HTTPException
from genesis.domains.islam_tutor.models import VerseResponse, QiblaRequest, QiblaResponse
from genesis.domains.islam_tutor.quran_system import QuranSystem
from genesis.domains.islam_tutor.qibla_calculator import QiblaCalculator
from genesis.domains.islam_tutor.namaz_trainer import NamazTrainer, NamazState

app = FastAPI(title="Islam Tutor API", description="API for the Islam Tutor MVP")

quran_sys = QuranSystem()
qibla_calc = QiblaCalculator()
namaz_trainer = NamazTrainer()

@app.get("/")
def root():
    return {"status": "Islam Tutor is active"}

@app.get("/quran/verse", response_model=VerseResponse)
def get_verse(surah: int, ayah: int, lang: str = "de"):
    try:
        data = quran_sys.get_verse(surah, ayah, lang)
        return VerseResponse(
            surah_id=surah,
            ayah_id=ayah,
            arabic_tajweed=data["arabic_tajweed"],
            transliteration=data["transliteration"],
            translation=data["translation"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/qibla/calculate", response_model=QiblaResponse)
def calculate_qibla(req: QiblaRequest):
    direction = qibla_calc.calculate_direction(req.latitude, req.longitude)
    distance = qibla_calc.calculate_distance(req.latitude, req.longitude)
    return QiblaResponse(direction_degrees=direction, distance_km=distance)
