# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: payment/grpc/payment.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'payment/grpc/payment.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1apayment/grpc/payment.proto\x12\x0c\x63ore.payment\x1a\x1bgoogle/protobuf/empty.proto\"#\n\x15PaymentDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x14\n\x12PaymentListRequest\"E\n\x13PaymentListResponse\x12.\n\x07results\x18\x01 \x03(\x0b\x32\x1d.core.payment.PaymentResponse\"\xd1\x01\n\x1bPaymentPartialUpdateRequest\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x0f\n\x07request\x18\x02 \x01(\x03\x12\x0f\n\x07user_id\x18\x03 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x01\x12\x16\n\x0etransaction_id\x18\x05 \x01(\t\x12\x1c\n\x0f\x61mount_in_paisa\x18\x06 \x01(\x01H\x01\x88\x01\x01\x12\x1e\n\x16_partial_update_fields\x18\x07 \x03(\tB\x05\n\x03_idB\x12\n\x10_amount_in_paisa\"\xd2\x02\n\x0ePaymentRequest\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x14\n\x07user_id\x18\x03 \x01(\x05H\x01\x88\x01\x01\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x01\x12\x1c\n\x0f\x61mount_in_paisa\x18\x05 \x01(\x01H\x02\x88\x01\x01\x12\x1b\n\x0etransaction_id\x18\x06 \x01(\tH\x03\x88\x01\x01\x12\x1c\n\x0fpayment_partner\x18\x07 \x01(\tH\x04\x88\x01\x01\x12\x14\n\x07purpose\x18\x08 \x01(\tH\x05\x88\x01\x01\x12\x14\n\x07remarks\x18\t \x01(\tH\x06\x88\x01\x01\x12\x13\n\x06status\x18\n \x01(\tH\x07\x88\x01\x01\x42\x05\n\x03_idB\n\n\x08_user_idB\x12\n\x10_amount_in_paisaB\x11\n\x0f_transaction_idB\x12\n\x10_payment_partnerB\n\n\x08_purposeB\n\n\x08_remarksB\t\n\x07_status\"*\n\x1cPaymentRequestDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x1b\n\x19PaymentRequestListRequest\"S\n\x1aPaymentRequestListResponse\x12\x35\n\x07results\x18\x01 \x03(\x0b\x32$.core.payment.PaymentRequestResponse\"\x86\x03\n\"PaymentRequestPartialUpdateRequest\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x1c\n\x0fpayment_partner\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07user_id\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x14\n\x07purpose\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x14\n\x07remarks\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x0e\n\x06\x61mount\x18\x06 \x01(\x01\x12\x1c\n\x0f\x61mount_in_paisa\x18\x07 \x01(\x01H\x05\x88\x01\x01\x12\x1b\n\x0etransaction_id\x18\x08 \x01(\tH\x06\x88\x01\x01\x12\x1e\n\x16_partial_update_fields\x18\t \x03(\t\x12\x13\n\x06status\x18\n \x01(\tH\x07\x88\x01\x01\x42\x05\n\x03_idB\x12\n\x10_payment_partnerB\n\n\x08_user_idB\n\n\x08_purposeB\n\n\x08_remarksB\x12\n\x10_amount_in_paisaB\x11\n\x0f_transaction_idB\t\n\x07_status\"\xda\x02\n\x16PaymentRequestResponse\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x1c\n\x0fpayment_partner\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07user_id\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x14\n\x07purpose\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x14\n\x07remarks\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x0e\n\x06\x61mount\x18\x06 \x01(\x01\x12\x1c\n\x0f\x61mount_in_paisa\x18\x07 \x01(\x01H\x05\x88\x01\x01\x12\x1b\n\x0etransaction_id\x18\x08 \x01(\tH\x06\x88\x01\x01\x12\x13\n\x06status\x18\t \x01(\tH\x07\x88\x01\x01\x42\x05\n\x03_idB\x12\n\x10_payment_partnerB\n\n\x08_user_idB\n\n\x08_purposeB\n\n\x08_remarksB\x12\n\x10_amount_in_paisaB\x11\n\x0f_transaction_idB\t\n\x07_status\"+\n\x1dPaymentRequestRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\xa5\x01\n\x0fPaymentResponse\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x0f\n\x07request\x18\x02 \x01(\x03\x12\x0f\n\x07user_id\x18\x03 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x01\x12\x16\n\x0etransaction_id\x18\x05 \x01(\t\x12\x1c\n\x0f\x61mount_in_paisa\x18\x06 \x01(\x01H\x01\x88\x01\x01\x42\x05\n\x03_idB\x12\n\x10_amount_in_paisa\"$\n\x16PaymentRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x32\xee\x03\n\x11PaymentController\x12G\n\x06\x43reate\x12\x1c.core.payment.PaymentRequest\x1a\x1d.core.payment.PaymentResponse\"\x00\x12H\n\x07\x44\x65stroy\x12#.core.payment.PaymentDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12M\n\x04List\x12 .core.payment.PaymentListRequest\x1a!.core.payment.PaymentListResponse\"\x00\x12[\n\rPartialUpdate\x12).core.payment.PaymentPartialUpdateRequest\x1a\x1d.core.payment.PaymentResponse\"\x00\x12Q\n\x08Retrieve\x12$.core.payment.PaymentRetrieveRequest\x1a\x1d.core.payment.PaymentResponse\"\x00\x12G\n\x06Update\x12\x1c.core.payment.PaymentRequest\x1a\x1d.core.payment.PaymentResponse\"\x00\x32\xb4\x04\n\x18PaymentRequestController\x12N\n\x06\x43reate\x12\x1c.core.payment.PaymentRequest\x1a$.core.payment.PaymentRequestResponse\"\x00\x12O\n\x07\x44\x65stroy\x12*.core.payment.PaymentRequestDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12[\n\x04List\x12\'.core.payment.PaymentRequestListRequest\x1a(.core.payment.PaymentRequestListResponse\"\x00\x12i\n\rPartialUpdate\x12\x30.core.payment.PaymentRequestPartialUpdateRequest\x1a$.core.payment.PaymentRequestResponse\"\x00\x12_\n\x08Retrieve\x12+.core.payment.PaymentRequestRetrieveRequest\x1a$.core.payment.PaymentRequestResponse\"\x00\x12N\n\x06Update\x12\x1c.core.payment.PaymentRequest\x1a$.core.payment.PaymentRequestResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'payment.grpc.payment_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PAYMENTDESTROYREQUEST']._serialized_start=73
  _globals['_PAYMENTDESTROYREQUEST']._serialized_end=108
  _globals['_PAYMENTLISTREQUEST']._serialized_start=110
  _globals['_PAYMENTLISTREQUEST']._serialized_end=130
  _globals['_PAYMENTLISTRESPONSE']._serialized_start=132
  _globals['_PAYMENTLISTRESPONSE']._serialized_end=201
  _globals['_PAYMENTPARTIALUPDATEREQUEST']._serialized_start=204
  _globals['_PAYMENTPARTIALUPDATEREQUEST']._serialized_end=413
  _globals['_PAYMENTREQUEST']._serialized_start=416
  _globals['_PAYMENTREQUEST']._serialized_end=754
  _globals['_PAYMENTREQUESTDESTROYREQUEST']._serialized_start=756
  _globals['_PAYMENTREQUESTDESTROYREQUEST']._serialized_end=798
  _globals['_PAYMENTREQUESTLISTREQUEST']._serialized_start=800
  _globals['_PAYMENTREQUESTLISTREQUEST']._serialized_end=827
  _globals['_PAYMENTREQUESTLISTRESPONSE']._serialized_start=829
  _globals['_PAYMENTREQUESTLISTRESPONSE']._serialized_end=912
  _globals['_PAYMENTREQUESTPARTIALUPDATEREQUEST']._serialized_start=915
  _globals['_PAYMENTREQUESTPARTIALUPDATEREQUEST']._serialized_end=1305
  _globals['_PAYMENTREQUESTRESPONSE']._serialized_start=1308
  _globals['_PAYMENTREQUESTRESPONSE']._serialized_end=1654
  _globals['_PAYMENTREQUESTRETRIEVEREQUEST']._serialized_start=1656
  _globals['_PAYMENTREQUESTRETRIEVEREQUEST']._serialized_end=1699
  _globals['_PAYMENTRESPONSE']._serialized_start=1702
  _globals['_PAYMENTRESPONSE']._serialized_end=1867
  _globals['_PAYMENTRETRIEVEREQUEST']._serialized_start=1869
  _globals['_PAYMENTRETRIEVEREQUEST']._serialized_end=1905
  _globals['_PAYMENTCONTROLLER']._serialized_start=1908
  _globals['_PAYMENTCONTROLLER']._serialized_end=2402
  _globals['_PAYMENTREQUESTCONTROLLER']._serialized_start=2405
  _globals['_PAYMENTREQUESTCONTROLLER']._serialized_end=2969
# @@protoc_insertion_point(module_scope)
