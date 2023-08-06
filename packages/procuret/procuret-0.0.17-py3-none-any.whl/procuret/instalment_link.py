"""
Procuret Python
Instalment Link Module
author: hugh@blinkybeach.com
"""
from procuret.ancillary.communication_option import CommunicationOption
from typing import TypeVar, Type, Union
from procuret.data.codable import Codable, CodingDefinition as CD
from procuret.ancillary.entity_headline import EntityHeadline
from procuret.errors.type_error import ProcuretTypeError
from procuret.http.api_request import ApiRequest, HTTPMethod
from procuret.errors.inconsistent import InconsistentState
from procuret.session import Session
from decimal import Decimal

T = TypeVar('T', bound='InstalmentLink')


class InstalmentLink(Codable):

    PATH = '/instalment-link'

    _LINK_TEMPLATE = 'https://procuret.com/business/signup?supplier_id={entity\
_id}&presented_invoice_id={invoice_id}&presented_invoice_amount={invoice_amoun\
t}'

    coding_map = {
        'supplier': CD(EntityHeadline),
        'invoice_amount': CD(Decimal),
        'invitee_email': CD(str),
        'invoice_identifier': CD(str),
    }

    def __init__(
        self,
        supplier: EntityHeadline,
        invitee_email: str,
        invoice_amount: Decimal,
        invoice_identifier: str
    ) -> None:

        self._supplier = supplier
        self._invitee_email = invitee_email
        self._invoice_amount = invoice_amount
        self._invoice_identifier = invoice_identifier

        return

    invitee_email = property(lambda s: s._invitee_email)
    invoice_amount = property(lambda s: s._invoice_amount)
    invoice_identifier = property(lambda s: s._invoice_identifier)

    url = property(lambda s: s._LINK_TEMPLATE.format(
        entity_id=str(s._supplier.entity_id),
        invoice_id=s._invoice_identifier,
        invoice_amount=str(s._invoice_amount)
    ))

    @classmethod
    def create(
        cls: Type[T],
        supplier: Union[int, EntityHeadline],
        invoice_amount: Decimal,
        invitee_email: str,
        invoice_identifier: str,
        communication: CommunicationOption,
        session: Session
    ) -> T:

        def infer_supplier_id(x: Union[int, EntityHeadline]) -> int:
            if isinstance(x, int):
                return x
            if isinstance(x, EntityHeadline):
                return x.entity_id
            raise ProcuretTypeError(('int', 'EntityHeadline'), x, 'supplier')

        def infer_communication(y: CommunicationOption) -> bool:
            if not isinstance(communication, CommunicationOption):
                raise ProcuretTypeError(
                    'CommunicationOption',
                    y,
                    'communcation'
                )
            if communication == CommunicationOption.DO_NOT_CONTACT_CUSTOMER:
                return False
            if communication == CommunicationOption.EMAIL_CUSTOMER:
                return True
            raise NotImplementedError

        if not isinstance(invoice_amount, Decimal):
            raise ProcuretTypeError(
                'Decimal',
                invoice_amount,
                'invoice_amount'
            )

        if not isinstance(invitee_email, str):
            raise ProcuretTypeError('str', invitee_email, 'invitee_email')

        if not isinstance(invoice_identifier, str):
            raise ProcuretTypeError(
                'str',
                invoice_identifier,
                'invoice_identifier'
            )

        data = {
            'supplier_id': infer_supplier_id(supplier),
            'invoice_amount': str(invoice_amount),
            'invitee_email': invitee_email,
            'invoice_identifier': invoice_identifier,
            'communicate': infer_communication(communication)
        }

        result = ApiRequest.make(
            path=cls.PATH,
            method=HTTPMethod.POST,
            data=data,
            session=session,
            query_parameters=None
        )

        if result is None:
            raise InconsistentState

        return cls.decode(result)
