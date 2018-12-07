from io import BytesIO

from flask import send_file, request
from flask_jwt_extended import get_jwt_identity

from api.handler import json_response
from auth.api_token import api_token_required
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from exceptions.auth import UnauthorizedException
from model.company import company
from model.company.company import get_company
from model.user import UserType

EMPTY_IMAGE = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00' \
              b'\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE' \
              b'\x00\x00\x00\xa7z=\xda\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00' \
              b'\x00\x00\nIDAT\x08\xd7c`\x00\x00\x00\x02\x00\x01\xe2!\xbc3' \
              b'\x00\x00\x00\x00IEND\xaeB`\x82'


@jwt_required
@json_response
def upload_company_logo(company_id):

    if 'file' not in request.files:
        raise ParametersException("The field `file` is required")

    identity = get_jwt_identity()
    if identity['role'] == UserType.CANDIDATE:
        raise UnauthorizedException()

    elif identity['role'] == UserType.HIRING_MANAGER:
        user_company = get_company(company_id=company_id)

        if not user_company:
            raise ParametersException("Invalid company id")

        if identity['username'] not in user_company['admin_user_ids']:
            raise UnauthorizedException()

    file = request.files['file']

    company.store_company_logo(company_id=company_id, file=file.stream)

    return None


@api_token_required
def get_company_logo(company_id):

    logo = company.get_company_logo(company_id=company_id)
    if not logo:
        logo = BytesIO(EMPTY_IMAGE)

    return send_file(logo, 'application/octet-stream')
