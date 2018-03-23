class BaseRecruitmentAppException(Exception):

    def __init__(self,
                 msg: str,
                 ref_id: str = None):
        super().__init__(msg)
        self.ref_id = ref_id
