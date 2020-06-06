from flask_restx import Namespace, fields


class UserDTO:
    user_api = Namespace("User", description="User related operations")
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
    client_api = Namespace("Client", description="Client related operations")
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
    investor_api = Namespace("Investor", description="Investor related operations")
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
    sme_api = Namespace("SME", description="SME related operations")
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
    document_api = Namespace("Document", description="Document related operations")
    document = document_api.model(
        "document",
        {
            "name": fields.String(required=False, description="Document name"),
            "file_name": fields.String(required=False, description="File name"),
            "file_type": fields.String(required=False, description="File type"),
            "file_size": fields.String(description="File size. Max upload size=5MB"),
        },
    )


class FundingDTO:
    funding_api = Namespace("Funding", description="Funding related operations")
    funding_application = funding_api.model(
        "funding_application",
        {
            "number": fields.String(
                required=True, description="Funding application number"
            ),
            "status": fields.String(
                required=True, description="Funding applicatio status"
            ),
            "sme_email": fields.String(required=True, description="SME email"),
        },
    )

    funding_criteria = funding_api.model(
        "funding_criteria",
        {
            "title": fields.String(required=True, description="Funding criteria title"),
            "description": fields.String(
                required=True, description="Description of funding criteria"
            ),
            "investor_email": fields.String(required=True),
        },
    )

    funding_criteria_display = funding_api.model(
        "funding_criteria_display",
        {
            "name": fields.String(description="Funding Criteria name"),
            "description": fields.String(description="Description of funding criteria"),
            "investor": fields.Nested(InvestorDTO().investor, description="Investor"),
        },
    )


class FundingProjectDTO:
    funding_project_api = Namespace(
        "Funding Project", description="Funding project related operations"
    )
    funding_project = funding_project_api.model(
        "funding_project",
        {
            "number": fields.String(required=True, description="Project number"),
            "title": fields.String(required=True, description="Project title"),
            "description": fields.String(
                required=True, description="Project description"
            ),
            "relevance": fields.String(required=True, description="Project relevance"),
            "objectives": fields.String(
                required=True, description="Project objectives"
            ),
            "justification": fields.String(
                required=True, description="Project justification"
            ),
            "work_plan": fields.String(required=True, description="Project work plan"),
            "status": fields.String(required=True, description="Project status"),
            "fund_amount": fields.Float(
                required=True, description="Project fund amount"
            ),
            "start_date": fields.Date(description="Project starting date"),
            "end_date": fields.Date(description="Project ending date"),
            "investor_email": fields.String(
                required=True, description="Investor email"
            ),
            "funding_application_number": fields.String(
                required=True, description="Funding application number"
            ),
        },
    )


class FundingDetailDTO:
    funding_detail_api = Namespace(
        "Funding Detail", description="Funding detail related operations"
    )
    funding_detail = funding_detail_api.model(
        "funding_detail",
        {
            "title": fields.String(required=True, description="Funding detail title"),
            "description": fields.String(description="Description of funding detail"),
            # "funding_project_number": fields.String(required=True),
        },
    )


class LoginDTO:
    login_api = Namespace("Login", description="User login")
    login = login_api.model(
        "Login",
        {
            "email address": fields.String(required=True, description="user email"),
            "password": fields.String(required=True, description="user password"),
        },
    )
