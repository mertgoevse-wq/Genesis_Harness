import hashlib
import json
import os

class QuranSystem:
    """Manages the Quran texts, transliteration, and translation."""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        else:
            self.data_dir = data_dir
        self.verified_hashes = self._load_hashes()
        
    def _load_hashes(self):
        hash_file = os.path.join(self.data_dir, "quran_hashes.json")
        if os.path.exists(hash_file):
            with open(hash_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _validate_file(self, filepath: str, expected_hash: str) -> bool:
        """Validates that the source text matches the verified hash. Never generate text freely."""
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Normalize line endings to avoid hash mismatches across OS
        content = content.replace("\r\n", "\n")
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        return content_hash == expected_hash
        
    def get_verse(self, surah_id: int, ayah_id: int, language: str = "de"):
        """Pipeline: Arabisch -> Transliteration -> Übersetzung"""
        surah_key = f"surah_{surah_id}"
        if surah_key not in self.verified_hashes:
            raise ValueError(f"Sura {surah_id} ist nicht in den verifizierten Quellen enthalten.")
            
        expected_hash = self.verified_hashes[surah_key]
        filepath = os.path.join(self.data_dir, f"{surah_key}.json")
        
        if not self._validate_file(filepath, expected_hash):
            raise ValueError(f"Security Alert: Hash mismatch for Sura {surah_id}! Possible data tampering.")
            
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        verse = data.get("verses", {}).get(str(ayah_id))
        if not verse:
            raise ValueError(f"Ayah {ayah_id} not found in Sura {surah_id}.")
            
        return {
            "arabic_tajweed": verse.get("arabic_tajweed", ""),
            "transliteration": verse.get("transliteration", ""),
            "translation": verse.get("translations", {}).get(language, "")
        }
