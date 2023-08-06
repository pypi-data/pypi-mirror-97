class InvalidVersion(Exception):
    def __init__(self, version):
        super().__init__(f"The version < {version} > is not valid")