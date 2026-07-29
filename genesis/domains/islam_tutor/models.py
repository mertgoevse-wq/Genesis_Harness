from pydantic import BaseModel
from typing import List, Optional

class TranslationRequest(BaseModel):
    key: str
    language: str

class VerseResponse(BaseModel):
    surah_id: int
    ayah_id: int
    arabic_tajweed: str
    transliteration: str
    translation: str

class AvatarPoseCommand(BaseModel):
    state_name: str
    joint_angles: dict
    audio_file: Optional[str] = None
    ui_text: str = ""
    ui_translation: str = ""

class QiblaRequest(BaseModel):
    latitude: float
    longitude: float
    
class QiblaResponse(BaseModel):
    direction_degrees: float
    distance_km: float
