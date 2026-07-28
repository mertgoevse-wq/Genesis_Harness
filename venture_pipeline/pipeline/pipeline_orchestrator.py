from venture_pipeline.pipeline.venture_lifecycle import VentureLifecycle
class PipelineOrchestrator:
    def run_pipeline(self, idea_name: str):
        vl = VentureLifecycle(idea_name)
        while vl.stage != "BUILD":
            vl.advance()
        return {"venture": idea_name, "final_stage": vl.stage}
