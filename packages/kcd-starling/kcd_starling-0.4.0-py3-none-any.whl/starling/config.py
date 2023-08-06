class Config(dict):
    def __init__(self, defaults: dict = None) -> None:
        super().__init__(defaults or {})


CONFIG = Config({'task_retry_times': 3, 'specific_task_retry_times': 5})
