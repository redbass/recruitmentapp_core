from exceptions import BaseRecruitmentAppException


class ParametersException(BaseRecruitmentAppException):
    pass


class ActionNotAllowed(BaseRecruitmentAppException):
    pass
