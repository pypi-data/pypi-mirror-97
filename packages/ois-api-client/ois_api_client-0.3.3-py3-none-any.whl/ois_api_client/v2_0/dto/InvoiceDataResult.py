from dataclasses import dataclass
from .AuditData import AuditData


@dataclass
class InvoiceDataResult:
    """Invoice number based query result

    :param invoice_data: Invoice data in BASE64 encoded form
    :param audit_data: Invoice audit data
    :param compressed_content_indicator: Indicates if the content of the invoice needs to be decompressed to be read following the BASE64 decoding
    """

    invoice_data: str
    audit_data: AuditData
    compressed_content_indicator: bool
