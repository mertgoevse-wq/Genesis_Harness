import pytest
import os
import json
import hashlib
from genesis.domains.islam_tutor.quran_system import QuranSystem

def test_quran_validation_success(tmp_path):
    # Setup mock data dir
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    mock_surah = {
        "surah_id": 1,
        "verses": {
            "1": {
                "arabic_tajweed": "بِسْمِ اللَّهِ",
                "transliteration": "Bismillah",
                "translations": {"de": "Im Namen Allahs"}
            }
        }
    }
    surah_content = json.dumps(mock_surah, indent=4)
    # Norm newline
    surah_content = surah_content.replace("\r\n", "\n")
    expected_hash = hashlib.sha256(surah_content.encode('utf-8')).hexdigest()
    
    with open(data_dir / "surah_1.json", "w", encoding="utf-8") as f:
        f.write(surah_content)
        
    with open(data_dir / "quran_hashes.json", "w", encoding="utf-8") as f:
        json.dump({"surah_1": expected_hash}, f)
        
    sys = QuranSystem(data_dir=str(data_dir))
    verse = sys.get_verse(1, 1, "de")
    assert verse["transliteration"] == "Bismillah"
    assert verse["translation"] == "Im Namen Allahs"

def test_quran_validation_failure(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Write manipulated file
    with open(data_dir / "surah_1.json", "w", encoding="utf-8") as f:
        f.write("FAKE CONTENT")
        
    # Valid hash is different
    with open(data_dir / "quran_hashes.json", "w", encoding="utf-8") as f:
        json.dump({"surah_1": "123456789"}, f)
        
    sys = QuranSystem(data_dir=str(data_dir))
    with pytest.raises(ValueError, match="Hash mismatch"):
        sys.get_verse(1, 1, "de")
