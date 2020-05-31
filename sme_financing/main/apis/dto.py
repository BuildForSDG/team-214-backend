from flask_restx import Namespace, fields


class UserDTO:
    user_api = Namespace("user", description="User related operations")
    user = user_api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(required=False, description="user public id"),
        },
    )
    userList = user_api.model(
        "userList",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(required=False, description="user public id"),
            "admin": fields.String(required=False, description="user admin status"),
        },
    )


class ClientDTO:
    client_api = Namespace("client", description="Client related operations")
    client = client_api.model(
        "client",
        {
            "lastname": fields.String(required=True, description="Client lastname"),
            "firstname": fields.String(required=True, description="Client firstname"),
            "gender": fields.String(required=True, description="Client gender"),
            "postal_address": fields.String(
                required=True, description="Client postal address"
            ),
            "residential_address": fields.String(
                required=True, description="Client address"
            ),
            "telephone": fields.String(
                required=True, description="Client telephone number"
            ),
            "nationality": fields.String(
                required=True, description="Client nationality"
            ),
            "education_level": fields.String(
                required=True,
                description="""Client education level.
                [Doctorate Degree, Masters Degree, Bachelors Degree, HND]""",
            ),
            "position": fields.String(
                required=True, description="Client position in the SME"
            ),
            "user": fields.Nested(UserDTO().user),
        },
    )


class InvestorDTO:
    investor_api = Namespace("investor", description="Investor related operations")
    investor = investor_api.model(
        "investor",
        {
            "name": fields.String(required=True, description="Investor name"),
            "postal_address": fields.String(
                required=True, description="Investor postal address"
            ),
            "street_address": fields.String(
                required=True, description="Investor street address"
            ),
            "city": fields.String(required=True, description="Investor city"),
            "telephone": fields.String(
                required=True, description="Investor telephone number"
            ),
            "email": fields.String(required=True, description="Investor email"),
            "investor_type": fields.String(required=True, description="Investor type."),
        },
    )


class SMEDTO:
    sme_api = Namespace("sme", description="SME related operations")
    sme_list = sme_api.model(
        "sme_list",
        {
            "name": fields.String(required=True, description="SME name"),
            "postal_address": fields.String(
                required=True, description="SME postal address"
            ),
            "location": fields.String(required=True, description="SME location"),
            "telephone": fields.String(required=True, description="SME telephone"),
            "email": fields.String(required=True, description="SME email address"),
            "description": fields.String(required=True, description="SME description"),
            "sector": fields.String(required=True, description="SME sector"),
            "principal_product_service": fields.String(
                required=True, description="SME principal product/service",
            ),
            "other_product_service": fields.String(
                required=True, description="SME other products/services"
            ),
            "age": fields.String(required=True, description="SME age"),
            "establishment_date": fields.Date(description="SME establishment date"),
            "ownership_type": fields.String(
                required=True, description="SME ownership type"
            ),
            "bank_account_details": fields.String(
                required=True, description="SME bank account details"
            ),
            "employees_number": fields.Integer(
                required=True, description="SME employees_number"
            ),
            "client": fields.Nested(
                ClientDTO().client, description="SME representative"
            ),
        },
    )

    sme = sme_api.model(
        "sme",
        {
            "name": fields.String(required=True, description="SME name"),
            "postal_address": fields.String(
                required=True, description="SME postal address"
            ),
            "location": fields.String(required=True, description="SME location"),
            "telephone": fields.String(required=True, description="SME telephone"),
            "email": fields.String(required=True, description="SME email address"),
            "description": fields.String(required=True, description="SME description"),
            "sector": fields.String(required=True, description="SME sector"),
            "principal_product_service": fields.String(
                required=True, description="SME principal product/service",
            ),
            "other_product_service": fields.String(
                required=True, description="SME other products/services"
            ),
            "age": fields.String(required=True, description="SME age"),
            "establishment_date": fields.Date(description="SME establishment date"),
            "ownership_type": fields.String(
                required=True, description="SME ownership type"
            ),
            "bank_account_details": fields.String(
                required=True, description="SME bank account details"
            ),
            "employees_number": fields.Integer(
                required=True, description="SME employees_number"
            ),
            "client_email": fields.String(required=True, description="Client email"),
        },
    )


class DocumentDTO:
    document_api = Namespace("document", description="Document related operations")
    document = document_api.model(
        "document",
        {
            "name": fields.String(required=False, description="Document name"),
            "file_name": fields.String(required=False, description="File name"),
            "file_type": fields.String(required=False, description="File type"),
            "file_size": fields.String(description="File size. Max upload size=5MB"),
        },
    )


class FundingApplicationDTO:
    funding_api = Namespace("funding", description="Funding related operations")
    funding_application = funding_api.model(
        "funding_application",
        {
            "name": fields.String(required=True, description="Document name"),
            "status": fields.String(required=True, description="Document name"),
            "sme_email": fields.String(required=True, description="Client email"),
        },
    )
