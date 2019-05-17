from exceptions import BaseRecruitmentAppException


class StripeException(BaseRecruitmentAppException):
    pass


class SendgridException(BaseRecruitmentAppException):
    def __init__(self, e: Exception):
        super().__init__(str(e),  ref_id="")
