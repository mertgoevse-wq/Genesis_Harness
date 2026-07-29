from enum import Enum

class NamazState(Enum):
    QIYAM = "Qiyam"
    TAKBIR = "Takbir"
    RUKU = "Ruku"
    SUJUD = "Sujud"
    JALSA = "Jalsa"
    TASHAHHUD = "Tashahhud"
    SALAM = "Salam"

class NamazTrainer:
    """Interactive 3D/2D Avatar Namaz Trainer."""
    
    def __init__(self):
        self.current_state = NamazState.QIYAM
        
    def set_state(self, state: NamazState):
        self.current_state = state
        return self.get_avatar_instructions()
        
    def get_avatar_instructions(self):
        """Returns details for UI/Avatar Agent based on state."""
        instructions = {
            NamazState.QIYAM: {"position": "Standing", "audio": "qiyam.mp3", "text": "...", "translation": "..."},
            NamazState.TAKBIR: {"position": "Hands to ears", "audio": "allahu_akbar.mp3", "text": "اللَّهُ أَكْبَر", "translation": "Allah ist der Größte"},
            NamazState.RUKU: {"position": "Bowing", "audio": "ruku.mp3", "text": "...", "translation": "Ehre sei meinem Herrn, dem Allmächtigen"},
            NamazState.SUJUD: {"position": "Prostration", "audio": "sujud.mp3", "text": "...", "translation": "Ehre sei meinem Herrn, dem Allerhöchsten"},
            NamazState.JALSA: {"position": "Sitting between Sujud", "audio": "jalsa.mp3", "text": "...", "translation": "O Allah vergib mir"},
            NamazState.TASHAHHUD: {"position": "Sitting down", "audio": "tashahhud.mp3", "text": "...", "translation": "..."},
            NamazState.SALAM: {"position": "Turning head", "audio": "salam.mp3", "text": "...", "translation": "Friede sei mit euch"}
        }
        return instructions.get(self.current_state, instructions[NamazState.QIYAM])
        
    def init_pose_detection(self):
        """Prepares MediaPipe / Camera MCP configuration for live tracking."""
        return {"engine": "MediaPipe", "mcp_required": "mobile-mcp"}
