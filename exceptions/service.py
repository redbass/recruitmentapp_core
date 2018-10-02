class ServiceError(Exception):
    def __init__(self, service_name):
        super().__init__("The service is temporarily unavailable")
        self.service_name = service_name
