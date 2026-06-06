from app.thesis.services.path_validator import PathValidator

class ThesisPipelineService:
    def __init__(self):
        self.validator = PathValidator()

    def run(self, folder: list[str]) -> dict:
        print("заглушка")