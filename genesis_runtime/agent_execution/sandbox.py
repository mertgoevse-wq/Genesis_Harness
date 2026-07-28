class ExecutionSandbox:
    def execute_safe(self, func, *args):
        return func(*args)
