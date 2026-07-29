from genesis.domains.islam_tutor.namaz_trainer import NamazTrainer, NamazState
from genesis.domains.islam_tutor.avatar_pipeline import AvatarPipeline

def test_namaz_trainer_state_transitions():
    trainer = NamazTrainer()
    assert trainer.current_state == NamazState.QIYAM
    
    inst = trainer.set_state(NamazState.RUKU)
    assert trainer.current_state == NamazState.RUKU
    assert inst["audio"] == "ruku.mp3"

def test_avatar_pipeline_generates_command():
    pipeline = AvatarPipeline()
    cmd = pipeline.generate_pose_command(NamazState.SUJUD)
    
    assert cmd.state_name == "Sujud"
    assert "spine" in cmd.joint_angles
    assert cmd.joint_angles["knees"] == 45
    assert cmd.audio_file == "sujud.mp3"
