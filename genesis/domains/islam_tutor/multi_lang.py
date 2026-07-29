import json
import os

class MultiLanguageRouter:
    """Handles localization of the app interface and religious contents."""
    
    SUPPORTED_LANGUAGES = ["de", "tr", "en", "ar"]
    
    def __init__(self, locales_dir: str = None):
        self.current_language = "de"
        if locales_dir is None:
            self.locales_dir = os.path.join(os.path.dirname(__file__), "locales")
        else:
            self.locales_dir = locales_dir
        self.db = self._load_translations()
            
    def _load_translations(self):
        db = {}
        for lang in self.SUPPORTED_LANGUAGES:
            file_path = os.path.join(self.locales_dir, f"{lang}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    db[lang] = json.load(f)
            else:
                db[lang] = {}
        return db

    def set_language(self, lang: str):
        if lang in self.SUPPORTED_LANGUAGES:
            self.current_language = lang
        else:
            raise ValueError(f"Language {lang} not supported.")
            
    def get_ui_text(self, key: str) -> str:
        return self.db.get(self.current_language, {}).get(key, key)
