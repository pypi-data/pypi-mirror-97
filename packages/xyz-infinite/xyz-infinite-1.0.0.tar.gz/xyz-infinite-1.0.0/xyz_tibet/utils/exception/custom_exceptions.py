# -*- coding: utf-8 -*-
"""
自定义各种异常
"""


class ParamCheckError(Exception):
    def __init__(self, e):
        super(ParamCheckError, self).__init__(e)


class LogicRunError(Exception):
    def __init__(self, e):
        super(LogicRunError, self).__init__(e)


class ApiError(Exception):
    message = 'Runtime api error occurred.'

    def __init__(self, message=None, *args, **kwargs):
        if message:
            self.message = message
        super(ApiError, self).__init__(self.message, *args, **kwargs)


class EvaluationTagExist(ApiError):
    message = "评教标签已存在"


class EvaluationTagNotFound(ApiError):
    message = "评教标签不存在"


class EvaluationTagReDeleted(ApiError):
    message = "评教标签已删除，请勿重复操作"


class EvaluationResultNotFound(ApiError):
    message = "学生评教不存在"


class EvaluationResultReDeleted(ApiError):
    message = "学生评教已删除，请勿重复操作"


class VideoManageDirExist(ApiError):
    message = "播单已存在"


class VideoManageDirNotFound(ApiError):
    message = "播单不存在"


class VideoNotFound(ApiError):
    message = "视频不存在"


class VideoStatusError(ApiError):
    message = "视频状态错误，禁止修改"


class EvaluationDeadlineInvalid(ApiError):
    message = "学生评教截止时间无效"


class ExcelSheetListOutOfRangeError(ApiError):
    message = "超出Excel工作簿范围"


class FakeUniversityNotFound(ApiError):
    message = "该演示大学不存在"


class IsNotAdminUser(ApiError):
    message = "该用户不是管理员"


class UserNotExist(ApiError):
    message = "该用户不存在"


class ProPPTAlreadyExist(Exception):
    message = "300301"
