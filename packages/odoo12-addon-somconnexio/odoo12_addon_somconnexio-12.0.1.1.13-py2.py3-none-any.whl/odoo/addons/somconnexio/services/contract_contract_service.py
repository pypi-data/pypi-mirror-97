class ContractService:
    def __init__(self, env):
        self.env = env

    def create(self, **params):
        self.env['contract.contract'].with_delay().create_contract(**params)
        return {"result": "OK"}
