from exceptions import BaseRecruitmentAppException


class AuthenticationError(BaseRecruitmentAppException):
    pass


class UnauthorizedException(BaseRecruitmentAppException):

    def __init__(self, ref_id: str = None):
        super().__init__("Unauthorized", ref_id)
