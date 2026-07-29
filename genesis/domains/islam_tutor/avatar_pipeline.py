from genesis.domains.islam_tutor.models import AvatarPoseCommand
from genesis.domains.islam_tutor.namaz_trainer import NamazState, NamazTrainer
from genesis.domains.islam_tutor.multi_lang import MultiLanguageRouter

class AvatarPipeline:
    """Connects the logical NamazState to visual and audio rendering commands for UI/MCP."""
    
    def __init__(self):
        self.trainer = NamazTrainer()
        self.router = MultiLanguageRouter()
        
    def generate_pose_command(self, state: NamazState) -> AvatarPoseCommand:
        """Generates the structured command object for rendering the 3D avatar."""
        instructions = self.trainer.set_state(state)
        
        # In a real scenario, joint angles would be derived from a 3D animation dict.
        # We mock joint angles for demonstration
        mock_angles = {
            NamazState.QIYAM: {"spine": 90, "knees": 180},
            NamazState.RUKU: {"spine": 0, "knees": 180},
            NamazState.SUJUD: {"spine": 0, "knees": 45}
        }
        
        # UI mapping from localization
        key_map = {
            NamazState.QIYAM: "namaz_qiyam",
            NamazState.RUKU: "namaz_ruku",
            NamazState.SUJUD: "namaz_sujud"
        }
        
        ui_text = self.router.get_ui_text(key_map.get(state, "namaz_qiyam"))
        
        return AvatarPoseCommand(
            state_name=state.value,
            joint_angles=mock_angles.get(state, {}),
            audio_file=instructions["audio"],
            ui_text=ui_text,
            ui_translation=instructions["translation"]
        )
