# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_common_types.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15sl_common_types.proto\x12\rservice_layer\"\xbc[\n\rSLErrorStatus\x12\x34\n\x06Status\x18\x01 \x01(\x0e\x32$.service_layer.SLErrorStatus.SLErrno\"\xf4Z\n\x07SLErrno\x12\x0e\n\nSL_SUCCESS\x10\x00\x12\x14\n\x10SL_NOT_CONNECTED\x10\x01\x12\r\n\tSL_EAGAIN\x10\x02\x12\r\n\tSL_ENOMEM\x10\x03\x12\x0c\n\x08SL_EBUSY\x10\x04\x12\r\n\tSL_EINVAL\x10\x05\x12\x16\n\x12SL_UNSUPPORTED_VER\x10\x06\x12\x14\n\x10SL_NOT_AVAILABLE\x10\x07\x12\x1b\n\x17SL_STREAM_NOT_SUPPORTED\x10\x08\x12\x0e\n\nSL_ENOTSUP\x10\t\x12\x0f\n\x0bSL_SOME_ERR\x10\n\x12\x0e\n\nSL_TIMEOUT\x10\x0b\x12\x11\n\rSL_NOTIF_TERM\x10\x0c\x12\x10\n\x0cSL_AUTH_FAIL\x10\r\x12\x1d\n\x19SL_ACK_TYPE_NOT_SUPPORTED\x10\x0e\x12\x19\n\x14SL_INIT_START_OFFSET\x10\x80\n\x12\x18\n\x13SL_INIT_STATE_CLEAR\x10\x81\n\x12\x18\n\x13SL_INIT_STATE_READY\x10\x82\n\x12\x1c\n\x17SL_INIT_UNSUPPORTED_VER\x10\x83\n\x12#\n\x1eSL_INIT_SERVER_NOT_INITIALIZED\x10\x84\n\x12&\n!SL_INIT_SERVER_MODE_CHANGE_FAILED\x10\x85\n\x12\x1c\n\x17SL_RPC_VRF_START_OFFSET\x10\x80 \x12%\n SL_RPC_VRF_TOO_MANY_VRF_REG_MSGS\x10\x81 \x12&\n!SL_RPC_VRF_SERVER_NOT_INITIALIZED\x10\x82 \x12&\n!SL_RPC_VRF_OP_NOTSUP_WITH_AUTOREG\x10\x83 \x12\x18\n\x13SL_VRF_START_OFFSET\x10\x80@\x12\x18\n\x13SL_VRF_NAME_TOOLONG\x10\x81@\x12\x15\n\x10SL_VRF_NOT_FOUND\x10\x82@\x12\x17\n\x12SL_VRF_NO_TABLE_ID\x10\x83@\x12&\n!SL_VRF_REG_INVALID_ADMIN_DISTANCE\x10\x84@\x12\x19\n\x14SL_VRF_TABLE_ADD_ERR\x10\x85@\x12\"\n\x1dSL_VRF_TABLE_REGISTRATION_ERR\x10\x86@\x12$\n\x1fSL_VRF_TABLE_UNREGISTRATION_ERR\x10\x87@\x12\x19\n\x14SL_VRF_TABLE_EOF_ERR\x10\x88@\x12 \n\x1bSL_VRF_REG_VRF_NAME_MISSING\x10\x89@\x12\'\n\"SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR\x10\x90@\x12\'\n\"SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR\x10\x91@\x12\x1e\n\x19SL_VRF_V4_ROUTE_REPLAY_OK\x10\x92@\x12\x1e\n\x19SL_VRF_V6_ROUTE_REPLAY_OK\x10\x93@\x12\x1e\n\x19SL_RPC_ROUTE_START_OFFSET\x10\x80`\x12!\n\x1cSL_RPC_ROUTE_TOO_MANY_ROUTES\x10\x81`\x12\"\n\x1dSL_RPC_ROUTE_VRF_NAME_TOOLONG\x10\x82`\x12\x1f\n\x1aSL_RPC_ROUTE_VRF_NOT_FOUND\x10\x83`\x12\x1e\n\x19SL_RPC_ROUTE_VRF_NO_TABLE\x10\x84`\x12*\n%SL_RPC_ROUTE_VRF_TABLE_NOT_REGISTERED\x10\x85`\x12\"\n\x1dSL_RPC_ROUTE_VRF_NAME_MISSING\x10\x86`\x12(\n#SL_RPC_ROUTE_INIT_MODE_INCOMPATIBLE\x10\x87`\x12(\n#SL_RPC_ROUTE_SERVER_NOT_INITIALIZED\x10\x88`\x12)\n$SL_RPC_ROUTE_NOTIF_SRC_PROTO_TOOLONG\x10\x89`\x12-\n(SL_RPC_ROUTE_NOTIF_SRC_PROTO_TAG_TOOLONG\x10\x8a`\x12#\n\x1eSL_RPC_ROUTE_GET_MATCH_INVALID\x10\x8b`\x12\"\n\x1dSL_RPC_ROUTE_GET_MATCH_NOTSUP\x10\x8c`\x12\x1b\n\x15SL_ROUTE_START_OFFSET\x10\x80\x80\x01\x12\x1b\n\x15SL_ROUTE_ADD_NO_PATHS\x10\x81\x80\x01\x12\x1e\n\x18SL_ROUTE_UPDATE_NO_PATHS\x10\x82\x80\x01\x12!\n\x1bSL_ROUTE_INVALID_PREFIX_LEN\x10\x83\x80\x01\x12%\n\x1fSL_ROUTE_INVALID_ADMIN_DISTANCE\x10\x84\x80\x01\x12 \n\x1aSL_ROUTE_INVALID_NUM_PATHS\x10\x85\x80\x01\x12 \n\x1aSL_ROUTE_INVALID_PREFIX_SZ\x10\x86\x80\x01\x12\x1d\n\x17SL_ROUTE_INVALID_PREFIX\x10\x87\x80\x01\x12*\n$SL_ROUTE_ERR_RIB_TABLE_LIMIT_REACHED\x10\x88\x80\x01\x12#\n\x1dSL_ROUTE_ERR_RIB_INVALID_ARGS\x10\x89\x80\x01\x12\'\n!SL_ROUTE_ERR_RIB_PATH_TABLE_LIMIT\x10\x8a\x80\x01\x12#\n\x1dSL_ROUTE_ERR_RIB_TOOMANYPATHS\x10\x8b\x80\x01\x12\x15\n\x0fSL_ROUTE_EEXIST\x10\x8c\x80\x01\x12\x1c\n\x16SL_ROUTE_HOST_BITS_SET\x10\x8d\x80\x01\x12#\n\x1dSL_ROUTE_INVALID_PREFIX_MCAST\x10\x8e\x80\x01\x12 \n\x1aSL_ROUTE_PATH_AFI_MISMATCH\x10\x8f\x80\x01\x12$\n\x1eSL_ROUTE_TOOMANY_PRIMARY_PATHS\x10\x90\x80\x01\x12#\n\x1dSL_ROUTE_TOOMANY_BACKUP_PATHS\x10\x91\x80\x01\x12\x17\n\x11SL_ROUTE_DB_NOMEM\x10\x92\x80\x01\x12\"\n\x1cSL_ROUTE_INVALID_LOCAL_LABEL\x10\x93\x80\x01\x12\x1c\n\x16SL_ROUTE_INVALID_FLAGS\x10\x94\x80\x01\x12\x1a\n\x14SL_PATH_START_OFFSET\x10\x80\xa0\x01\x12\x19\n\x13SL_PATH_NH_NO_TABLE\x10\x81\xa0\x01\x12\x1f\n\x19SL_PATH_NH_INTF_NOT_FOUND\x10\x82\xa0\x01\x12!\n\x1bSL_PATH_INVALID_LABEL_COUNT\x10\x83\xa0\x01\x12\x18\n\x12SL_PATH_INVALID_ID\x10\x84\xa0\x01\x12\x1e\n\x18SL_PATH_VRF_NAME_TOOLONG\x10\x85\xa0\x01\x12\"\n\x1cSL_PATH_NH_INTF_NAME_TOOLONG\x10\x86\xa0\x01\x12 \n\x1aSL_PATH_NH_INVALID_ADDR_SZ\x10\x87\xa0\x01\x12!\n\x1bSL_PATH_NH_INF_NAME_MISSING\x10\x88\xa0\x01\x12#\n\x1dSL_PATH_INVALID_NEXT_HOP_ADDR\x10\x89\xa0\x01\x12\'\n!SL_PATH_INVALID_REMOTE_ADDR_COUNT\x10\x8a\xa0\x01\x12$\n\x1eSL_PATH_REMOTE_ADDR_INVALID_SZ\x10\x8b\xa0\x01\x12&\n SL_PATH_REMOTE_ADDR_AFI_MISMATCH\x10\x8c\xa0\x01\x12&\n SL_PATH_INVALID_PROTECTED_BITMAP\x10\x8d\xa0\x01\x12)\n#SL_PATH_BACKUP_MISSING_PRIMARY_PATH\x10\x8e\xa0\x01\x12!\n\x1bSL_PATH_PRIMARY_ID_REPEATED\x10\x8f\xa0\x01\x12 \n\x1aSL_PATH_BACKUP_ID_REPEATED\x10\x90\xa0\x01\x12*\n$SL_PATH_PRIMARY_TOOMANY_BACKUP_PATHS\x10\x91\xa0\x01\x12$\n\x1eSL_PATH_PRIMARY_TOOMANY_LABELS\x10\x92\xa0\x01\x12)\n#SL_PATH_PRIMARY_TOOMANY_REMOTE_ADDR\x10\x93\xa0\x01\x12!\n\x1bSL_PATH_REMOTE_ADDR_INVALID\x10\x94\xa0\x01\x12\x1b\n\x15SL_PATH_INVALID_LABEL\x10\x95\xa0\x01\x12(\n\"SL_PATH_ROUTER_MAC_ADDR_INVALID_SZ\x10\x96\xa0\x01\x12#\n\x1dSL_PATH_BACKUP_TOOMANY_LABELS\x10\x97\xa0\x01\x12\x19\n\x13SL_PATH_INVALID_VNI\x10\x98\xa0\x01\x12 \n\x1aSL_PATH_INVALID_ENCAP_ADDR\x10\x99\xa0\x01\x12(\n\"SL_PATH_ENCAP_SRC_DST_AFI_MISMATCH\x10\x9a\xa0\x01\x12\x1b\n\x15SL_PATH_RTR_MAC_NOSUP\x10\x9b\xa0\x01\x12!\n\x1bSL_PATH_ENCAP_TYPE_MISMATCH\x10\x9c\xa0\x01\x12\x1d\n\x17SL_RPC_BFD_START_OFFSET\x10\x80\xc0\x01\x12&\n SL_RPC_BFD_TOO_MANY_BFD_SESSIONS\x10\x81\xc0\x01\x12\"\n\x1cSL_RPC_BFD_API_BAD_PARAMETER\x10\x82\xc0\x01\x12*\n$SL_RPC_BFD_API_CLIENT_NOT_REGISTERED\x10\x83\xc0\x01\x12#\n\x1dSL_RPC_BFD_API_INTERNAL_ERROR\x10\x84\xc0\x01\x12\'\n!SL_RPC_BFD_SERVER_NOT_INITIALIZED\x10\x85\xc0\x01\x12\"\n\x1cSL_RPC_BFD_V4_NOT_REGISTERED\x10\x86\xc0\x01\x12\"\n\x1cSL_RPC_BFD_V6_NOT_REGISTERED\x10\x87\xc0\x01\x12\x19\n\x13SL_BFD_START_OFFSET\x10\x80\xe0\x01\x12\x1e\n\x18SL_BFD_INTF_NAME_TOOLONG\x10\x81\xe0\x01\x12\x1b\n\x15SL_BFD_INTF_NOT_FOUND\x10\x82\xe0\x01\x12\x1e\n\x18SL_BFD_INVALID_ATTRIBUTE\x10\x83\xe0\x01\x12\x1e\n\x18SL_BFD_INTF_NAME_MISSING\x10\x84\xe0\x01\x12\x1e\n\x18SL_BFD_INVALID_NBR_MCAST\x10\x85\xe0\x01\x12\x18\n\x12SL_BFD_INVALID_NBR\x10\x86\xe0\x01\x12\x1d\n\x17SL_BFD_VRF_NAME_TOOLONG\x10\x87\xe0\x01\x12\x1a\n\x14SL_BFD_BAD_PARAMETER\x10\x88\xe0\x01\x12\x1f\n\x19SL_BFD_API_INTERNAL_ERROR\x10\x89\xe0\x01\x12\x1a\n\x14SL_BFD_VRF_NOT_FOUND\x10\x8a\xe0\x01\x12 \n\x1aSL_BFD_INVALID_PREFIX_SIZE\x10\x8b\xe0\x01\x12!\n\x1bSL_BFD_INVALID_SESSION_TYPE\x10\x8c\xe0\x01\x12\x18\n\x12SL_BFD_INVALID_VRF\x10\x8d\xe0\x01\x12\x1e\n\x18SL_BFD_SESSION_NOT_FOUND\x10\x8e\xe0\x01\x12\x1b\n\x15SL_BFD_SESSION_EXISTS\x10\x8f\xe0\x01\x12\x1e\n\x18SL_BFD_INTERNAL_DB_ERROR\x10\x90\xe0\x01\x12\x1b\n\x15SL_BFD_RECOVERY_ERROR\x10\x91\xe0\x01\x12\x1e\n\x18SL_RPC_MPLS_START_OFFSET\x10\x80\x80\x02\x12#\n\x1dSL_RPC_MPLS_ILM_TOO_MANY_ILMS\x10\x81\x80\x02\x12(\n\"SL_RPC_MPLS_SERVER_NOT_INITIALIZED\x10\x82\x80\x02\x12(\n\"SL_RPC_MPLS_INIT_MODE_INCOMPATIBLE\x10\x83\x80\x02\x12/\n)SL_RPC_MPLS_LABEL_BLK_TOO_MANY_LABEL_BLKS\x10\x84\x80\x02\x12 \n\x1aSL_RPC_MPLS_NOT_REGISTERED\x10\x85\x80\x02\x12\x17\n\x11SL_ILM_ERR_OFFSET\x10\x80\xa0\x02\x12\x17\n\x11SL_ILM_ADD_FAILED\x10\x81\xa0\x02\x12\x1b\n\x15SL_ILM_LSD_ADD_FAILED\x10\x82\xa0\x02\x12\x1e\n\x18SL_ILM_INVALID_NUM_NHLFE\x10\x83\xa0\x02\x12\x1a\n\x14SL_ILM_INVALID_LABEL\x10\x84\xa0\x02\x12\x1a\n\x14SL_ILM_DELETE_FAILED\x10\x85\xa0\x02\x12\x1e\n\x18SL_ILM_LSD_DELETE_FAILED\x10\x86\xa0\x02\x12#\n\x1dSL_ILM_TOOMANY_PRIMARY_NHLFES\x10\x87\xa0\x02\x12\"\n\x1cSL_ILM_TOOMANY_BACKUP_NHLFES\x10\x88\xa0\x02\x12\'\n!SL_ILM_LSD_ADD_LABEL_ALLOC_FAILED\x10\x89\xa0\x02\x12%\n\x1fSL_ILM_LSD_NHLFE_INVALID_ATTRIB\x10\x8a\xa0\x02\x12\x13\n\rSL_ILM_EEXIST\x10\x8b\xa0\x02\x12\x15\n\x0fSL_ILM_DB_NOMEM\x10\x8c\xa0\x02\x12\x1d\n\x17SL_ILM_INVALID_ELSP_EXP\x10\x8d\xa0\x02\x12)\n#SL_ILM_ELSP_EXP_OR_DFLT_ALREADY_SET\x10\x8e\xa0\x02\x12\x19\n\x13SL_ILM_ADD_NO_PATHS\x10\x8f\xa0\x02\x12\x1c\n\x16SL_ILM_UPDATE_NO_PATHS\x10\x90\xa0\x02\x12\x1d\n\x17SL_ILM_UNSUPPORTED_ELSP\x10\x91\xa0\x02\x12&\n SL_ILM_LABEL_TOOMANY_EXP_CLASSES\x10\x92\xa0\x02\x12\x1f\n\x19SL_ILM_REPLAY_FATAL_ERROR\x10\x93\xa0\x02\x12\x16\n\x10SL_ILM_REPLAY_OK\x10\x94\xa0\x02\x12\x1f\n\x19SL_ILM_INVALID_PREFIX_LEN\x10\x95\xa0\x02\x12\x1a\n\x14SL_ILM_HOST_BITS_SET\x10\x96\xa0\x02\x12\x1e\n\x18SL_ILM_INVALID_PREFIX_SZ\x10\x97\xa0\x02\x12\x1b\n\x15SL_ILM_INVALID_PREFIX\x10\x98\xa0\x02\x12!\n\x1bSL_ILM_INVALID_PREFIX_MCAST\x10\x99\xa0\x02\x12\x1d\n\x17SL_ILM_VRF_NAME_TOOLONG\x10\xa0\xa0\x02\x12\x1c\n\x16SL_ILM_VRF_NO_TABLE_ID\x10\xa1\xa0\x02\x12\x1d\n\x17SL_ILM_VRF_NAME_MISSING\x10\xa2\xa0\x02\x12\x19\n\x13SL_NHLFE_ERR_OFFSET\x10\x80\xc0\x02\x12\x1a\n\x14SL_NHLFE_NH_NO_TABLE\x10\x81\xc0\x02\x12!\n\x1bSL_NHLFE_NH_INVALID_ADDR_SZ\x10\x82\xc0\x02\x12$\n\x1eSL_NHLFE_INVALID_NEXT_HOP_ADDR\x10\x83\xc0\x02\x12\x1f\n\x19SL_NHLFE_VRF_NAME_TOOLONG\x10\x84\xc0\x02\x12\"\n\x1cSL_NHLFE_NH_INF_NAME_MISSING\x10\x85\xc0\x02\x12#\n\x1dSL_NHLFE_NH_INTF_NAME_TOOLONG\x10\x86\xc0\x02\x12\"\n\x1cSL_NHLFE_INVALID_LABEL_COUNT\x10\x87\xc0\x02\x12\x1e\n\x18SL_NHLFE_INVALID_PATH_ID\x10\x88\xc0\x02\x12\x1c\n\x16SL_NHLFE_INVALID_LABEL\x10\x89\xc0\x02\x12\'\n!SL_NHLFE_INVALID_PROTECTED_BITMAP\x10\x8a\xc0\x02\x12(\n\"SL_NHLFE_INVALID_REMOTE_ADDR_COUNT\x10\x8b\xc0\x02\x12%\n\x1fSL_NHLFE_REMOTE_ADDR_INVALID_SZ\x10\x8c\xc0\x02\x12%\n\x1fSL_NHLFE_PRIMARY_TOOMANY_LABELS\x10\x8d\xc0\x02\x12*\n$SL_NHLFE_PRIMARY_TOOMANY_REMOTE_ADDR\x10\x8e\xc0\x02\x12!\n\x1bSL_NHLFE_BACKUP_ID_REPEATED\x10\x8f\xc0\x02\x12\"\n\x1cSL_NHLFE_PRIMARY_ID_REPEATED\x10\x90\xc0\x02\x12,\n&SL_NHLFE_BACKUP_PROTECTED_BITMAP_EMPTY\x10\x91\xc0\x02\x12+\n%SL_NHLFE_PRIMARY_TOOMANY_BACKUP_PATHS\x10\x92\xc0\x02\x12\"\n\x1cSL_NHLFE_REMOTE_ADDR_INVALID\x10\x93\xc0\x02\x12*\n$SL_NHLFE_BACKUP_MISSING_PRIMARY_PATH\x10\x94\xc0\x02\x12\x1f\n\x19SL_NHLFE_NEXT_HOP_MISSING\x10\x95\xc0\x02\x12#\n\x1dSL_NHLFE_LABEL_ACTION_INVALID\x10\x96\xc0\x02\x12 \n\x1aSL_NHLFE_NH_INTF_NOT_FOUND\x10\x97\xc0\x02\x12\x1a\n\x14SL_NHLFE_OPER_FAILED\x10\x98\xc0\x02\x12#\n\x1dSL_NHLFE_LABEL_ACTION_MISSING\x10\x99\xc0\x02\x12\x1d\n\x17SL_NHLFE_EXP_SET_FAILED\x10\x9a\xc0\x02\x12*\n$SL_NHLFE_ELSP_PROTECTION_UNSUPPORTED\x10\x9b\xc0\x02\x12\x1f\n\x19SL_NHLFE_INVALID_ELSP_EXP\x10\x9c\xc0\x02\x12$\n\x1eSL_NHLFE_INVALID_PATH_PRIORITY\x10\x9d\xc0\x02\x12\"\n\x1cSL_NHLFE_INVALID_LOAD_METRIC\x10\x9e\xc0\x02\x12\x1c\n\x16SL_NHLFE_INVALID_SETID\x10\x9f\xc0\x02\x12%\n\x1fSL_NHLFE_INVALID_SETID_PRIORITY\x10\xa0\xc0\x02\x12.\n(SL_NHLFE_INVALID_MULTIPLE_PRIMARY_SETIDS\x10\xa1\xc0\x02\x12$\n\x1eSL_NHLFE_NON_CONTIGUOUS_SETIDS\x10\xa2\xc0\x02\x12!\n\x1bSL_NHLFE_NON_CONTIGUOUS_EXP\x10\xa3\xc0\x02\x12\'\n!SL_NHLFE_INCONSISTENT_EXP_ON_PATH\x10\xa4\xc0\x02\x12\x1d\n\x17SL_LABEL_BLK_ERR_OFFSET\x10\x80\xe0\x02\x12!\n\x1bSL_LABEL_BLK_LSD_ADD_FAILED\x10\x81\xe0\x02\x12$\n\x1eSL_LABEL_BLK_LSD_DELETE_FAILED\x10\x82\xe0\x02\x12*\n$SL_LABEL_BLK_LSD_LABEL_BLK_NOT_FOUND\x10\x83\xe0\x02\x12\'\n!SL_LABEL_BLK_LSD_LABEL_BLK_IN_USE\x10\x84\xe0\x02\x12%\n\x1fSL_LABEL_BLK_LSD_INVALID_ATTRIB\x10\x85\xe0\x02\x12%\n\x1fSL_LABEL_BLK_INVALID_BLOCK_SIZE\x10\x86\xe0\x02\x12&\n SL_LABEL_BLK_INVALID_START_LABEL\x10\x87\xe0\x02\x12\x19\n\x13SL_LABEL_BLK_EEXIST\x10\x88\xe0\x02\x12\x1b\n\x15SL_LABEL_BLK_DB_NOMEM\x10\x89\xe0\x02\x12\x1f\n\x19SL_LABEL_BLK_TYPE_INVALID\x10\x8a\xe0\x02\x12&\n SL_LABEL_BLK_CLIENT_NAME_TOOLONG\x10\x8b\xe0\x02\x12\x1c\n\x16SL_MPLS_REG_ERR_OFFSET\x10\x80\x80\x03\x12\x15\n\x0fSL_MPLS_REG_ERR\x10\x81\x80\x03\x12\x17\n\x11SL_MPLS_UNREG_ERR\x10\x82\x80\x03\x12\x15\n\x0fSL_MPLS_EOF_ERR\x10\x83\x80\x03\x12\x1e\n\x18SL_RPC_INTF_START_OFFSET\x10\x80\xa0\x03\x12%\n\x1fSL_RPC_INTF_TOO_MANY_INTERFACES\x10\x81\xa0\x03\x12(\n\"SL_RPC_INTF_SERVER_NOT_INITIALIZED\x10\x82\xa0\x03\x12+\n%SL_RPC_INTF_API_CLIENT_NOT_REGISTERED\x10\x83\xa0\x03\x12\x1a\n\x14SL_INTF_START_OFFSET\x10\x80\xc0\x03\x12$\n\x1eSL_INTF_INTERFACE_NAME_MISSING\x10\x81\xc0\x03\x12$\n\x1eSL_INTF_INTERFACE_NAME_TOOLONG\x10\x82\xc0\x03\x12\x1f\n\x19SL_INTF_INTERFACE_REG_ERR\x10\x83\xc0\x03\x12\x1f\n\x19SL_INTF_INTERNAL_DB_ERROR\x10\x84\xc0\x03\x12\x1c\n\x16SL_INTF_RECOVERY_ERROR\x10\x85\xc0\x03\x12\x1e\n\x18SL_INTF_INTERFACE_EXISTS\x10\x86\xc0\x03\x12!\n\x1bSL_INTF_INTERFACE_NOT_FOUND\x10\x87\xc0\x03\x12+\n%SL_INTF_INTERFACE_STATE_NOT_SUPPORTED\x10\x88\xc0\x03\x12\x1c\n\x16SL_L2_REG_START_OFFSET\x10\x80\xe0\x03\x12\x1c\n\x16SL_L2_REGISTRATION_ERR\x10\x81\xe0\x03\x12\x1e\n\x18SL_L2_UNREGISTRATION_ERR\x10\x82\xe0\x03\x12\x13\n\rSL_L2_EOF_ERR\x10\x83\xe0\x03\x12&\n SL_L2_REG_INVALID_ADMIN_DISTANCE\x10\x84\xe0\x03\x12\x1c\n\x16SL_L2_REG_IS_DUPLICATE\x10\x85\xe0\x03\x12&\n SL_L2_REG_SERVER_NOT_INITIALIZED\x10\x86\xe0\x03\x12#\n\x1dSL_RPC_L2_BD_REG_START_OFFSET\x10\x80\x80\x04\x12#\n\x1dSL_RPC_L2_BD_REG_NAME_MISSING\x10\x81\x80\x04\x12$\n\x1eSL_RPC_L2_BD_REG_TOO_MANY_MSGS\x10\x82\x80\x04\x12-\n\'SL_RPC_L2_BD_REG_SERVER_NOT_INITIALIZED\x10\x83\x80\x04\x12,\n&SL_RPC_L2_BD_REG_CLIENT_NOT_REGISTERED\x10\x84\x80\x04\x12\x1f\n\x19SL_L2_BD_REG_START_OFFSET\x10\x80\xa0\x04\x12\x1f\n\x19SL_L2_BD_REGISTRATION_ERR\x10\x81\xa0\x04\x12!\n\x1bSL_L2_BD_UNREGISTRATION_ERR\x10\x82\xa0\x04\x12\x16\n\x10SL_L2_BD_EOF_ERR\x10\x83\xa0\x04\x12 \n\x1aSL_L2_BD_REG_NAME_TOO_LONG\x10\x84\xa0\x04\x12\x1f\n\x19SL_L2_BD_REG_BD_NOT_FOUND\x10\x85\xa0\x04\x12\"\n\x1cSL_RPC_L2_ROUTE_START_OFFSET\x10\x80\xc0\x04\x12#\n\x1dSL_RPC_L2_ROUTE_TOO_MANY_MSGS\x10\x81\xc0\x04\x12,\n&SL_RPC_L2_ROUTE_SERVER_NOT_INITIALIZED\x10\x82\xc0\x04\x12+\n%SL_RPC_L2_ROUTE_CLIENT_NOT_REGISTERED\x10\x83\xc0\x04\x12\x1e\n\x18SL_L2_ROUTE_START_OFFSET\x10\x80\xe0\x04\x12!\n\x1bSL_L2_ROUTE_BD_NAME_MISSING\x10\x81\xe0\x04\x12!\n\x1bSL_L2_ROUTE_BD_NAME_TOOLONG\x10\x82\xe0\x04\x12\x1e\n\x18SL_L2_ROUTE_BD_NOT_FOUND\x10\x83\xe0\x04\x12#\n\x1dSL_L2_ROUTE_BD_NOT_REGISTERED\x10\x84\xe0\x04\x12\x1e\n\x18SL_L2_ROUTE_INVALID_ARGS\x10\x85\xe0\x04\x12\"\n\x1cSL_RPC_L2_NOTIF_START_OFFSET\x10\x81\x80\x05\x12,\n&SL_RPC_L2_NOTIF_SERVER_NOT_INITIALIZED\x10\x82\x80\x05\x12+\n%SL_RPC_L2_NOTIF_CLIENT_NOT_REGISTERED\x10\x83\x80\x05\x12 \n\x1aSL_RPC_L2_NOTIF_ENABLE_ERR\x10\x84\x80\x05\x12!\n\x1bSL_RPC_L2_NOTIF_DISABLE_ERR\x10\x85\x80\x05\x12\x1d\n\x17SL_RPC_L2_NOTIF_EOF_ERR\x10\x86\x80\x05\x12%\n\x1fSL_RPC_L2_NOTIF_BD_NAME_MISSING\x10\x87\x80\x05\x12%\n\x1fSL_RPC_L2_NOTIF_BD_NAME_TOOLONG\x10\x88\x80\x05\x12\"\n\x1cSL_RPC_L2_NOTIF_BD_NOT_FOUND\x10\x89\x80\x05\x12\x17\n\x11SL_PG_VRF_ADD_ERR\x10\x81\xa0\x05\x12\x18\n\x12SL_PG_VRF_NO_VRFID\x10\x82\xa0\x05\x12\x1b\n\x15SL_PG_STR_KEY_TOOLONG\x10\x83\xa0\x05\x12\x1f\n\x19SL_PG_TARGET_VRF_NO_VRFID\x10\x84\xa0\x05\x12\x1b\n\x15SL_PG_STR_KEY_INVALID\x10\x85\xa0\x05\x12\x1e\n\x18SL_NEXT_HOP_START_OFFSET\x10\x80\xc0\x05\x12$\n\x1eSL_NEXT_HOP_INVALID_PREFIX_LEN\x10\x81\xc0\x05\x12\x1f\n\x19SL_NEXT_HOP_HOST_BITS_SET\x10\x82\xc0\x05\x12&\n SL_NEXT_HOP_INVALID_PREFIX_MCAST\x10\x83\xc0\x05\x12 \n\x1aSL_NEXT_HOP_INVALID_PREFIX\x10\x84\xc0\x05\x12\'\n!SL_NEXT_HOP_INVALID_NEXT_HOP_ADDR\x10\x85\xc0\x05\x12#\n\x1dSL_NEXT_HOP_INVALID_PREFIX_SZ\x10\x86\xc0\x05\x12 \n\x1aSL_NEXT_HOP_RIB_ADD_FAILED\x10\x87\xc0\x05\x12$\n\x1eSL_ROUTE_REDIST_RIB_ADD_FAILED\x10\x88\xc0\x05\x12\x19\n\x13SL_FIB_START_OFFSET\x10\x80\xe0\x05\x12\x14\n\x0eSL_FIB_SUCCESS\x10\x81\xe0\x05\x12\x13\n\rSL_FIB_FAILED\x10\x82\xe0\x05\x12\x17\n\x11SL_FIB_INELIGIBLE\x10\x83\xe0\x05\x12!\n\x1bSL_ACK_PERMIT_NOT_SUPPORTED\x10\x84\xe0\x05\x12\"\n\x1cSL_ACK_CADENCE_NOT_SUPPORTED\x10\x85\xe0\x05\x12\x1c\n\x16SL_POLICY_START_OFFSET\x10\x80\x80\x06\x12\x17\n\x11SL_POLICY_ADD_ERR\x10\x81\x80\x06\x12\x1a\n\x14SL_POLICY_EXISTS_ERR\x10\x82\x80\x06\x12\x1a\n\x14SL_POLICY_DELETE_ERR\x10\x83\x80\x06\x12\x1c\n\x16SL_POLICY_RULE_ADD_ERR\x10\x84\x80\x06\x12\x1f\n\x19SL_POLICY_RULE_EXISTS_ERR\x10\x85\x80\x06\x12\x1f\n\x19SL_POLICY_RULE_DELETE_ERR\x10\x86\x80\x06\x12\x19\n\x13SL_POLICY_APPLY_ERR\x10\x87\x80\x06\x12\x1b\n\x15SL_POLICY_UNAPPLY_ERR\x10\x88\x80\x06\x12!\n\x1bSL_POLICY_TOO_MANY_POLICIES\x10\x89\x80\x06\x12\x1d\n\x17SL_POLICY_NAME_TOO_LONG\x10\x8a\x80\x06\x12\"\n\x1cSL_POLICY_RULE_NAME_TOO_LONG\x10\x8b\x80\x06\x12*\n$SL_POLICY_DUPLICATE_PRIORITY_IN_RULE\x10\x8c\x80\x06\x12$\n\x1eSL_POLICY_RULE_MOD_NOT_ALLOWED\x10\x8d\x80\x06\x12\x1c\n\x16SL_POLICY_INVALID_RULE\x10\x8e\x80\x06\x12!\n\x1bSL_POLICY_RULE_ADD_NO_RULES\x10\x8f\x80\x06\x12+\n%SL_POLICY_INVALID_MATCH_COUNT_IN_RULE\x10\x90\x80\x06\x12,\n&SL_POLICY_INVALID_ACTION_COUNT_IN_RULE\x10\x91\x80\x06\x12\x19\n\x13SL_POLICY_NOT_FOUND\x10\x92\x80\x06\x12\x17\n\x11SL_POLICY_INVALID\x10\x93\x80\x06\x12\x1c\n\x16SL_POLICY_NAME_MISSING\x10\x94\x80\x06\x12!\n\x1bSL_POLICY_RULE_NAME_MISSING\x10\x95\x80\x06\x12(\n\"SL_POLICY_PRIORITY_MISSING_IN_RULE\x10\x96\x80\x06\x12\x1c\n\x16SL_POLICY_TYPE_INVALID\x10\x97\x80\x06\x12!\n\x1bSL_POLICY_INVALID_DIRECTION\x10\x98\x80\x06\x12!\n\x1bSL_POLICY_INTF_NAME_TOOLONG\x10\x99\x80\x06\x12!\n\x1bSL_POLICY_INTF_NAME_MISSING\x10\x9a\x80\x06\x12&\n SL_POLICY_MAX_RULE_LIMIT_REACHED\x10\x9b\x80\x06\x12!\n\x1bSL_POLICY_VRF_NAME_TOO_LONG\x10\x9c\x80\x06\x12 \n\x1aSL_POLICY_VRF_NAME_MISSING\x10\x9d\x80\x06\x12&\n SL_POLICY_PATH_GRP_NAME_TOO_LONG\x10\x9e\x80\x06\x12%\n\x1fSL_POLICY_PATH_GRP_NAME_MISSING\x10\x9f\x80\x06\x12\"\n\x1cSL_POLICY_INVALID_DSCP_VALUE\x10\xa0\x80\x06\x12%\n\x1fSL_POLICY_PRIORITY_STR_TOO_LONG\x10\xa1\x80\x06\x12&\n SL_POLICY_MAX_INTF_LIMIT_REACHED\x10\xa2\x80\x06\x12$\n\x1eSL_POLICY_RULE_DELETE_NO_RULES\x10\xa3\x80\x06\x12\x1e\n\x18SL_POLICY_APPLY_NO_INTFS\x10\xa4\x80\x06\x12 \n\x1aSL_POLICY_UNAPPLY_NO_INTFS\x10\xa5\x80\x06\x12 \n\x1aSL_BGPLS_TOPO_START_OFFSET\x10\x80\xa0\x06\x12#\n\x1dSL_BGPLS_SERVER_NOT_AVAILABLE\x10\x81\xa0\x06\x12(\n\"SL_BGPLS_MAX_MATCH_FILTER_EXCEEDED\x10\x82\xa0\x06\x12#\n\x1dSL_BGPLS_MAX_STREAMS_EXCEEDED\x10\x83\xa0\x06\x12!\n\x1bSL_SRTE_POLICY_START_OFFSET\x10\x80\xc0\x06\x12$\n\x1eSL_SRTE_POLICY_INVALID_REQUEST\x10\x81\xc0\x06\x12&\n SL_SRTE_POLICY_POLICYKEY_MISSING\x10\x82\xc0\x06\x12,\n&SL_SRTE_POLICY_POLICYKEY_COLOR_MISSING\x10\x83\xc0\x06\x12)\n#SL_SRTE_POLICY_POLICYKEY_EP_MISSING\x10\x84\xc0\x06\x12*\n$SL_SRTE_POLICY_POLICYKEY_SRC_MISSING\x10\x85\xc0\x06\x12$\n\x1eSL_SRTE_POLICY_CP_PREF_MISSING\x10\x86\xc0\x06\x12\"\n\x1cSL_SRTE_POLICY_CPKEY_MISSING\x10\x87\xc0\x06\x12-\n\'SL_SRTE_POLICY_CPKEY_ORIGINATOR_MISSING\x10\x88\xc0\x06\x12#\n\x1dSL_SRTE_POLICY_SERVICE_NOT_UP\x10\x89\xc0\x06\x12$\n\x1eSL_SRTE_POLICY_EXCEED_MSG_SIZE\x10\x8a\xc0\x06\x12#\n\x1dSL_SRTE_PCALC_INVALID_REQUEST\x10\x81\xc2\x06\x12!\n\x1bSL_SRTE_PCALC_NO_PATH_FOUND\x10\x82\xc2\x06\x12\x1e\n\x18SL_INTERNAL_START_OFFSET\x10\x80\x80@\"<\n\x0bSLInterface\x12\x0e\n\x04Name\x18\x01 \x01(\tH\x00\x12\x10\n\x06Handle\x18\x02 \x01(\rH\x00\x42\x0b\n\tInterface\"B\n\x0bSLIpAddress\x12\x13\n\tV4Address\x18\x01 \x01(\rH\x00\x12\x13\n\tV6Address\x18\x02 \x01(\x0cH\x00\x42\t\n\x07\x41\x64\x64ress\"%\n\nSLObjectId\x12\x0e\n\x04Name\x18\x01 \x01(\tH\x00\x42\x07\n\x05\x65ntry\"T\n\x11SLPathGroupRefKey\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12.\n\x0bPathGroupId\x18\x02 \x01(\x0b\x32\x19.service_layer.SLObjectId*b\n\x07SLRegOp\x12\x15\n\x11SL_REGOP_RESERVED\x10\x00\x12\x15\n\x11SL_REGOP_REGISTER\x10\x01\x12\x17\n\x13SL_REGOP_UNREGISTER\x10\x02\x12\x10\n\x0cSL_REGOP_EOF\x10\x03*_\n\nSLObjectOp\x12\x15\n\x11SL_OBJOP_RESERVED\x10\x00\x12\x10\n\x0cSL_OBJOP_ADD\x10\x01\x12\x13\n\x0fSL_OBJOP_UPDATE\x10\x02\x12\x13\n\x0fSL_OBJOP_DELETE\x10\x03*S\n\tSLNotifOp\x12\x17\n\x13SL_NOTIFOP_RESERVED\x10\x00\x12\x15\n\x11SL_NOTIFOP_ENABLE\x10\x01\x12\x16\n\x12SL_NOTIFOP_DISABLE\x10\x02*\x89\x01\n\x10SLUpdatePriority\x12\x18\n\x14SL_PRIORITY_RESERVED\x10\x00\x12\x18\n\x14SL_PRIORITY_CRITICAL\x10\x04\x12\x14\n\x10SL_PRIORITY_HIGH\x10\x08\x12\x16\n\x12SL_PRIORITY_MEDIUM\x10\x0c\x12\x13\n\x0fSL_PRIORITY_LOW\x10\x10*K\n\x0bSLEncapType\x12\x15\n\x11SL_ENCAP_RESERVED\x10\x00\x12\x12\n\x0eSL_ENCAP_VXLAN\x10\x01\x12\x11\n\rSL_ENCAP_MPLS\x10\x02*\x8d\x01\n\x0bSLTableType\x12\x1a\n\x16SL_TABLE_TYPE_RESERVED\x10\x00\x12\x17\n\x13SL_IPv4_ROUTE_TABLE\x10\x01\x12\x17\n\x13SL_IPv6_ROUTE_TABLE\x10\x02\x12\x17\n\x13SL_MPLS_LABEL_TABLE\x10\x03\x12\x17\n\x13SL_PATH_GROUP_TABLE\x10\x04*0\n\x0cSLRspACKType\x12\x0b\n\x07RIB_ACK\x10\x00\x12\x13\n\x0fRIB_AND_FIB_ACK\x10\x01*\x99\x01\n\x0eSLRspACKPermit\x12\x11\n\rSL_PERMIT_ALL\x10\x00\x12\x18\n\x14SL_PERMIT_SL_SUCCESS\x10\x01\x12\x1c\n\x18SL_PERMIT_SL_FIB_SUCCESS\x10\x02\x12\x1b\n\x17SL_PERMIT_SL_FIB_FAILED\x10\x04\x12\x1f\n\x1bSL_PERMIT_SL_FIB_INELIGIBLE\x10\x08*T\n\x0fSLRspAckCadence\x12\x15\n\x11SL_RSP_CONTINUOUS\x10\x00\x12\x14\n\x10SL_RSP_JUST_ONCE\x10\x01\x12\x14\n\x10SL_RSP_ONCE_EACH\x10\x02\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_common_types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLREGOP']._serialized_start=12006
  _globals['_SLREGOP']._serialized_end=12104
  _globals['_SLOBJECTOP']._serialized_start=12106
  _globals['_SLOBJECTOP']._serialized_end=12201
  _globals['_SLNOTIFOP']._serialized_start=12203
  _globals['_SLNOTIFOP']._serialized_end=12286
  _globals['_SLUPDATEPRIORITY']._serialized_start=12289
  _globals['_SLUPDATEPRIORITY']._serialized_end=12426
  _globals['_SLENCAPTYPE']._serialized_start=12428
  _globals['_SLENCAPTYPE']._serialized_end=12503
  _globals['_SLTABLETYPE']._serialized_start=12506
  _globals['_SLTABLETYPE']._serialized_end=12647
  _globals['_SLRSPACKTYPE']._serialized_start=12649
  _globals['_SLRSPACKTYPE']._serialized_end=12697
  _globals['_SLRSPACKPERMIT']._serialized_start=12700
  _globals['_SLRSPACKPERMIT']._serialized_end=12853
  _globals['_SLRSPACKCADENCE']._serialized_start=12855
  _globals['_SLRSPACKCADENCE']._serialized_end=12939
  _globals['_SLERRORSTATUS']._serialized_start=41
  _globals['_SLERRORSTATUS']._serialized_end=11749
  _globals['_SLERRORSTATUS_SLERRNO']._serialized_start=113
  _globals['_SLERRORSTATUS_SLERRNO']._serialized_end=11749
  _globals['_SLINTERFACE']._serialized_start=11751
  _globals['_SLINTERFACE']._serialized_end=11811
  _globals['_SLIPADDRESS']._serialized_start=11813
  _globals['_SLIPADDRESS']._serialized_end=11879
  _globals['_SLOBJECTID']._serialized_start=11881
  _globals['_SLOBJECTID']._serialized_end=11918
  _globals['_SLPATHGROUPREFKEY']._serialized_start=11920
  _globals['_SLPATHGROUPREFKEY']._serialized_end=12004
# @@protoc_insertion_point(module_scope)
