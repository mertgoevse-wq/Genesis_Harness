import sys
import os

# Add parent directory to path to import genesis modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genesis.orchestrator import MasterGenesisOrchestrator

def main():
    print("Starte Islam Tutor Autonomous Development Loop...")
    orchestrator = MasterGenesisOrchestrator()
    
    # Der Intent für den MetaAgent
    intent = "Entwickle den Islam Tutor weiter: Validiere Quran-Daten, implementiere Namaz-Trainer-Posen im UI und generiere arabisches Sprach-Audio."
    
    orchestrator.process_request(intent)
    
if __name__ == "__main__":
    main()
