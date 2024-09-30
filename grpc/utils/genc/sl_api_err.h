/*
 *------------------------------------------------------------------
 * This file is AUTO-GENERATED. DO NOT EDIT.
 *
 * Copyright (c) 2016-2019 by cisco Systems, Inc.
 * All rights reserved.
 *------------------------------------------------------------------
 */

#ifndef __SL_API_ERR_H__
#define __SL_API_ERR_H__

#define SL_GENERATED_ERR_CODES \
    /* !!! Common error codes for all RPCs and objects */\
    /* Success, no errors detected. 0x0. */\
    SL_SUCCESS = 0x0,\
    /* Client not connected. 0x1 */\
    SL_NOT_CONNECTED = 0x1,\
    /* Operation must be retried. 0x2 */\
    SL_EAGAIN = 0x2,\
    /* One or more components does not have sufficient memory. 0x3 */\
    SL_ENOMEM = 0x3,\
    /* Too many outstanding requests. 0x4 */\
    SL_EBUSY = 0x4,\
    /* One or more arguments are invalid. 0x5 */\
    SL_EINVAL = 0x5,\
    /* Unsupported version. 0x6 */\
    SL_UNSUPPORTED_VER = 0x6,\
    /* Not Available. 0x7 */\
    SL_NOT_AVAILABLE = 0x7,\
    /* Stream mode not supported. 0x8 */\
    SL_STREAM_NOT_SUPPORTED = 0x8,\
    /* Operation not supported. 0x9 */\
    SL_ENOTSUP = 0x9,\
    /* One or more objects is errored: */\
    /* Each object must be individually examined. 0xa */\
    SL_SOME_ERR = 0xa,\
    /* Operation Timed out. */\
    /* The result of the operation is undeterministic (success or fail). 0xb */\
    SL_TIMEOUT = 0xb,\
    /* Due to some event, the client will no longer receive notification */\
    /* events on this channel. 0xc */\
    /* Such events include: */\
    /* - Notification Session was hijacked by another client. */\
    SL_NOTIF_TERM = 0xc,\
    /* Authentication failure. */\
    /* Incorrect credentials passed in by RPC. 0xd */\
    SL_AUTH_FAIL = 0xd,\
    /* Ack type not supported error. 0xe */\
    SL_ACK_TYPE_NOT_SUPPORTED = 0xe,\
    /* Ack cadence not supported when scope is not defined. 0xf */\
    SL_ACK_CADENCE_NOT_SUPPORTED = 0xf,\
    /* !!! Error codes for Client INIT operations. */\
    /* Offset for INIT errors. 0x500 */\
    SL_INIT_START_OFFSET = 0x500,\
    /* Success, no errors detected - clear state. */\
    /* This error is returned on the first-ever initialization, or, */\
    /* when a fatal event has occured and all previous state was lost. 0x501 */\
    SL_INIT_STATE_CLEAR = 0x501,\
    /* Success, no errors detected - previous state is recovered. */\
    /* This error is returned on a client re-initialization with */\
    /* successful recovery of state. Note that any unacknowledged */\
    /* data previously sent should be considered lost. 0x502 */\
    SL_INIT_STATE_READY = 0x502,\
    /* Server software incompatible with client software version. 0x503 */\
    SL_INIT_UNSUPPORTED_VER = 0x503,\
    /* Initialization request received while server is not ready. 0x504 */\
    SL_INIT_SERVER_NOT_INITIALIZED = 0x504,\
    /* Server operational mode change from stream to non-stream */\
    /* or vice-versa failed. 0x505 */\
    SL_INIT_SERVER_MODE_CHANGE_FAILED = 0x505,\
    /* !!! Error codes for VRF operations. */\
    /* Offset for VRF errors. 0x1000 */\
    SL_RPC_VRF_START_OFFSET = 0x1000,\
    /* Operation rejected for ALL VRFs due to too many VRF registration */\
    /* messages in the request. 0x1001 */\
    SL_RPC_VRF_TOO_MANY_VRF_REG_MSGS = 0x1001,\
    /* Operation rejected for all VRFs as server is not initialized. 0x1002 */\
    SL_RPC_VRF_SERVER_NOT_INITIALIZED = 0x1002,\
    /* Operation not supported in auto-register mode. 0x1003 */\
    SL_RPC_VRF_OP_NOTSUP_WITH_AUTOREG = 0x1003,\
    /* !!! Error codes for VRF objects. */\
    /* Offset for VRF errors. 0x2000 */\
    SL_VRF_START_OFFSET = 0x2000,\
    /* VRF name in the VRF registration message is too long. 0x2001 */\
    SL_VRF_NAME_TOOLONG = 0x2001,\
    /* VRF not found during a unregister or EOF. 0x2002 */\
    SL_VRF_NOT_FOUND = 0x2002,\
    /* On a VRF registration, Table ID for the VRF is not found. 0x2003 */\
    SL_VRF_NO_TABLE_ID = 0x2003,\
    /* VRF add registration message with invalid administrative distance. 0x2004 */\
    SL_VRF_REG_INVALID_ADMIN_DISTANCE = 0x2004,\
    /* On a VRF registration, Table cannot be added to persistent memory. 0x2005 */\
    SL_VRF_TABLE_ADD_ERR = 0x2005,\
    /* VRF table cannot be registered with RIB. 0x2006 */\
    SL_VRF_TABLE_REGISTRATION_ERR = 0x2006,\
    /* VRF table cannot be unregistered with RIB. 0x2007 */\
    SL_VRF_TABLE_UNREGISTRATION_ERR = 0x2007,\
    /* VRF table RIB EOF operation error. 0x2008 */\
    SL_VRF_TABLE_EOF_ERR = 0x2008,\
    /* VRF registration message does not have a VRF name. 0x2009 */\
    SL_VRF_REG_VRF_NAME_MISSING = 0x2009,\
    /* IPv4 routes in VRF cannot be played to Routing Information Base */\
    /* on a process restart or connection re-establishment. */\
    /* The Forwarding Information Base can */\
    /* can be inconsistent. Agent/Controller should initiate a */\
    /* recovery action by reloading the device. 0x2010 */\
    SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR = 0x2010,\
    /* IPv6 routes in VRF cannot be played to Routing Information Base */\
    /* on a process restart or connection re-establishment. */\
    /* The Forwarding Information Base can */\
    /* can be inconsistent. Agent/Controller should initiate a */\
    /* recovery action by reloading the device. 0x2011 */\
    SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR = 0x2011,\
    /* IPv4 routes in VRF were played to Routing Information Base */\
    /* on a process restart or connection re-establishment. 0x2012 */\
    SL_VRF_V4_ROUTE_REPLAY_OK = 0x2012,\
    /* IPv6 routes in VRF were played to Routing Information Base */\
    /* on a process restart or connection re-establishment. 0x2013 */\
    SL_VRF_V6_ROUTE_REPLAY_OK = 0x2013,\
    /* !!! Error codes for Route operations. */\
    /* Offset for Route operation errors. 0x3000 */\
    SL_RPC_ROUTE_START_OFFSET = 0x3000,\
    /* Operation rejected for ALL routes due to too many routes in the */\
    /* request. 0x3001 */\
    SL_RPC_ROUTE_TOO_MANY_ROUTES = 0x3001,\
    /* Operation rejected for ALL routes as the request's VRF name */\
    /* is too long. 0x3002 */\
    SL_RPC_ROUTE_VRF_NAME_TOOLONG = 0x3002,\
    /* Operation rejected for ALL routes as VRF for the given name */\
    /* is not found. 0x3003 */\
    SL_RPC_ROUTE_VRF_NOT_FOUND = 0x3003,\
    /* Operation rejected for ALL routes as VRF's Table ID is not found. */\
    /* 0x3004 */\
    SL_RPC_ROUTE_VRF_NO_TABLE = 0x3004,\
    /* Operation rejected for ALL routes as VRF is not registered with RIB. */\
    /* 0x3005 */\
    SL_RPC_ROUTE_VRF_TABLE_NOT_REGISTERED = 0x3005,\
    /* Route Operation rejected for ALL objects as VRF name is missing. */\
    /* 0x3006 */\
    SL_RPC_ROUTE_VRF_NAME_MISSING = 0x3006,\
    /* Operation rejected for all routes as the RPC request is */\
    /* not supported for the library's initialization mode. 0x3007 */\
    SL_RPC_ROUTE_INIT_MODE_INCOMPATIBLE = 0x3007,\
    /* Operation rejected for all routes as server is not initialized. */\
    /* 0x3008 */\
    SL_RPC_ROUTE_SERVER_NOT_INITIALIZED = 0x3008,\
    /* Operation rejected as the request's SrcProto is too long. 0x3009 */\
    SL_RPC_ROUTE_NOTIF_SRC_PROTO_TOOLONG = 0x3009,\
    /* Operation rejected as the request's SrcProtoTag is too long. 0x300a */\
    SL_RPC_ROUTE_NOTIF_SRC_PROTO_TAG_TOOLONG = 0x300a,\
    /* Operation rejected as the requested match value/values/criteria is invalid. 0x300b */\
    SL_RPC_ROUTE_GET_MATCH_INVALID = 0x300b,\
    /* Operation rejected as the requested match value/values/criteria is not supported. 0x300c */\
    SL_RPC_ROUTE_GET_MATCH_NOTSUP = 0x300c,\
    /* !!! Error codes for Route objects. */\
    /* Offset for route errors. 0x4000 */\
    SL_ROUTE_START_OFFSET = 0x4000,\
    /* Route add operation requested but no paths were provided. 0x4001 */\
    SL_ROUTE_ADD_NO_PATHS = 0x4001,\
    /* Route update operation requested but no paths were provided. 0x4002 */\
    SL_ROUTE_UPDATE_NO_PATHS = 0x4002,\
    /* Route's prefix length is invalid. 0x4003 */\
    SL_ROUTE_INVALID_PREFIX_LEN = 0x4003,\
    /* Route's admininstrative distance is invalid. 0x4004 */\
    SL_ROUTE_INVALID_ADMIN_DISTANCE = 0x4004,\
    /* Route's number of paths exceeds system capabilities. 0x4005 */\
    SL_ROUTE_INVALID_NUM_PATHS = 0x4005,\
    /* Size of IPv6 prefix is invalid. 0x4006 */\
    SL_ROUTE_INVALID_PREFIX_SZ = 0x4006,\
    /* Route's prefix is invalid. 0x4007 */\
    SL_ROUTE_INVALID_PREFIX = 0x4007,\
    /* Route programming failed in RIB as VRF table limit reached. 0x4008 */\
    SL_ROUTE_ERR_RIB_TABLE_LIMIT_REACHED = 0x4008,\
    /* RIB route programming failed in RIB due to invalid arguments. 0x4009 */\
    SL_ROUTE_ERR_RIB_INVALID_ARGS = 0x4009,\
    /* One or more paths could not be programmed in RIB as VRF */\
    /* table limit reached. 0x400a */\
    SL_ROUTE_ERR_RIB_PATH_TABLE_LIMIT = 0x400a,\
    /* One or more paths could not be programmed in RIB as number of paths */\
    /* reached system limit. 0x400b */\
    SL_ROUTE_ERR_RIB_TOOMANYPATHS = 0x400b,\
    /* This route already exists in the database. 0x400c   */\
    SL_ROUTE_EEXIST = 0x400c,\
    /* Route prefix has host bits set. 0x400d */\
    SL_ROUTE_HOST_BITS_SET = 0x400d,\
    /* IPv4 Route prefix is a multicast address. 0x400e */\
    SL_ROUTE_INVALID_PREFIX_MCAST = 0x400e,\
    /* Route and Path AFI does not match. 0x400f */\
    SL_ROUTE_PATH_AFI_MISMATCH = 0x400f,\
    /* Number of primary paths exceeds system capabilities. 0x4010 */\
    SL_ROUTE_TOOMANY_PRIMARY_PATHS = 0x4010,\
    /* Number of backup paths exceeds system capabilities. 0x4011 */\
    SL_ROUTE_TOOMANY_BACKUP_PATHS = 0x4011,\
    /* The route database is out of memory. 0x4012 */\
    SL_ROUTE_DB_NOMEM = 0x4012,\
    /* The route has an invalid local label. 0x4013 */\
    SL_ROUTE_INVALID_LOCAL_LABEL = 0x4013,\
    /* Invalid route flags. 0x4014 */\
    SL_ROUTE_INVALID_FLAGS = 0x4014,\
    /* !!! Error codes for route path objects. */\
    /* Offset for route path errors. 0x5000 */\
    SL_PATH_START_OFFSET = 0x5000,\
    /* VRF table for the path could not be determined. 0x5001 */\
    SL_PATH_NH_NO_TABLE = 0x5001,\
    /* Path next hop interface not found. 0x5002 */\
    SL_PATH_NH_INTF_NOT_FOUND = 0x5002,\
    /* Number of labels in the path exceeds system capabilities. 0x5003 */\
    SL_PATH_INVALID_LABEL_COUNT = 0x5003,\
    /* Path ID assigned to the path falls outside the supported range. 0x5004 */\
    SL_PATH_INVALID_ID = 0x5004,\
    /* Path VRF name exceeds supported length. 0x5005 */\
    SL_PATH_VRF_NAME_TOOLONG = 0x5005,\
    /* Path next hop interface name exceeds supported length. 0x5006 */\
    SL_PATH_NH_INTF_NAME_TOOLONG = 0x5006,\
    /* Size of next hop IPv6 address is invalid. 0x5007 */\
    SL_PATH_NH_INVALID_ADDR_SZ = 0x5007,\
    /* Next hop interface name is missing from path. 0x5008 */\
    SL_PATH_NH_INF_NAME_MISSING = 0x5008,\
    /* Path has an invalid next hop address. 0x5009 */\
    SL_PATH_INVALID_NEXT_HOP_ADDR = 0x5009,\
    /* Number of remote backup addresses in the path exceeds */\
    /* system capabilities. 0x500a */\
    SL_PATH_INVALID_REMOTE_ADDR_COUNT = 0x500a,\
    /* Size of IPv6 remote backup address is invalid. 0x500b */\
    SL_PATH_REMOTE_ADDR_INVALID_SZ = 0x500b,\
    /* Route and Path remote backup address AFI does not match. 0x500c */\
    SL_PATH_REMOTE_ADDR_AFI_MISMATCH = 0x500c,\
    /* Path has an invalid protection bitmap. 0x500d */\
    SL_PATH_INVALID_PROTECTED_BITMAP = 0x500d,\
    /* Protection bitmap of a backup path refers to a missing path. 0x500e */\
    SL_PATH_BACKUP_MISSING_PRIMARY_PATH = 0x500e,\
    /* Too many primary paths with same Path ID. 0x500f */\
    SL_PATH_PRIMARY_ID_REPEATED = 0x500f,\
    /* Too many pure backup paths with same Path ID. 0x5010 */\
    SL_PATH_BACKUP_ID_REPEATED = 0x5010,\
    /* A primary path has too many backup paths. 0x5011 */\
    SL_PATH_PRIMARY_TOOMANY_BACKUP_PATHS = 0x5011,\
    /* A primary path has too many labels. 0x5012 */\
    SL_PATH_PRIMARY_TOOMANY_LABELS = 0x5012,\
    /* A primary path has too many remote addresses. 0x5013 */\
    SL_PATH_PRIMARY_TOOMANY_REMOTE_ADDR = 0x5013,\
    /* A pure backup remote address is invalid. 0x5014 */\
    SL_PATH_REMOTE_ADDR_INVALID = 0x5014,\
    /* Path has an invalid label. 0x5015 */\
    SL_PATH_INVALID_LABEL = 0x5015,\
    /* Size of router mac address is invalid. 0x5016 */\
    SL_PATH_ROUTER_MAC_ADDR_INVALID_SZ = 0x5016,\
    /* A backup path has too many labels. 0x5017 */\
    SL_PATH_BACKUP_TOOMANY_LABELS = 0x5017,\
    /* Invalid VNI for VxLAN encap. 0x5018 */\
    SL_PATH_INVALID_VNI = 0x5018,\
    /* Path has an invalid  encap address. 0x5019 */\
    SL_PATH_INVALID_ENCAP_ADDR = 0x5019,\
    /* Path encapsulation source and destination AFI mismatch. 0x501a */\
    SL_PATH_ENCAP_SRC_DST_AFI_MISMATCH = 0x501a,\
    /* PATH router mac is not supported with VxLAN path attributes. 0x501b */\
    SL_PATH_RTR_MAC_NOSUP = 0x501b,\
    /* Path Encap type attribute does not match specified encapsulation. 0x501c */\
    SL_PATH_ENCAP_TYPE_MISMATCH = 0x501c,\
    /* !!! Error codes for BFD opertations. */\
    /* Offset for BFD operation errors. 0x6000 */\
    SL_RPC_BFD_START_OFFSET = 0x6000,\
    /* BFD Operation rejected for ALL Sessions as the BFD Session count */\
    /* is beyond supported limit. 0x6001 */\
    SL_RPC_BFD_TOO_MANY_BFD_SESSIONS = 0x6001,\
    /* BFD Operation rejected due to one or many invalid parameters. 0x6002 */\
    SL_RPC_BFD_API_BAD_PARAMETER = 0x6002,\
    /* BFD Operation failed as server is not registered with BFD. 0x6003 */\
    SL_RPC_BFD_API_CLIENT_NOT_REGISTERED = 0x6003,\
    /* BFD Operation failed with internal error. 0x6004 */\
    SL_RPC_BFD_API_INTERNAL_ERROR = 0x6004,\
    /* BFD Operation rejected as server is not initialized. 0x6005 */\
    SL_RPC_BFD_SERVER_NOT_INITIALIZED = 0x6005,\
    /* BFD IPv4 not registered. 0x6006 */\
    SL_RPC_BFD_V4_NOT_REGISTERED = 0x6006,\
    /* BFD IPv6 not registered. 0x6007 */\
    SL_RPC_BFD_V6_NOT_REGISTERED = 0x6007,\
    /* !!! Error codes for BFD Session objects. */\
    /* Offset for BFD errors. 0x7000 */\
    SL_BFD_START_OFFSET = 0x7000,\
    /* BFD Session's interface name exceeds supported length. 0x7001 */\
    SL_BFD_INTF_NAME_TOOLONG = 0x7001,\
    /* BFD Session's interface not found. 0x7002 */\
    SL_BFD_INTF_NOT_FOUND = 0x7002,\
    /* BFD Session's tx interval or multiplier are beyond the  */\
    /* supported range. 0x7003 */\
    SL_BFD_INVALID_ATTRIBUTE = 0x7003,\
    /* BFD Session's interface name is missing. 0x7004 */\
    SL_BFD_INTF_NAME_MISSING = 0x7004,\
    /* BFD Session's neighbor is mcast address. 0x7005 */\
    SL_BFD_INVALID_NBR_MCAST = 0x7005,\
    /* BFD Session's neighbor address is invalid. 0x7006 */\
    SL_BFD_INVALID_NBR = 0x7006,\
    /* BFD Session's VRF Name is too long. 0x7007 */\
    SL_BFD_VRF_NAME_TOOLONG = 0x7007,\
    /* BFD Session's one or more parameters are invalid.  */\
    /* For example, Multihop BFD can not have the interface name set. 0x7008 */\
    SL_BFD_BAD_PARAMETER = 0x7008,\
    /* BFD Session failed with internal error. 0x7009 */\
    SL_BFD_API_INTERNAL_ERROR = 0x7009,\
    /* BFD Session's VRF not found. 0x700a */\
    SL_BFD_VRF_NOT_FOUND = 0x700a,\
    /* BFD Session's neighbor IPv6 prefix size is invalid. 0x700b */\
    SL_BFD_INVALID_PREFIX_SIZE = 0x700b,\
    /* BFD Session type invalid. 0x700c */\
    SL_BFD_INVALID_SESSION_TYPE = 0x700c,\
    /* BFD Session's VRF is Invalid. 0x700d */\
    SL_BFD_INVALID_VRF = 0x700d,\
    /* BFD Session not found. 0x700e */\
    SL_BFD_SESSION_NOT_FOUND = 0x700e,\
    /* BFD Session exists. 0x700f */\
    SL_BFD_SESSION_EXISTS = 0x700f,\
    /* BFD Internal database error. 0x7010 */\
    SL_BFD_INTERNAL_DB_ERROR = 0x7010,\
    /* BFD Recovery error. 0x7011 */\
    SL_BFD_RECOVERY_ERROR = 0x7011,\
    /* !!! Error codes for MPLS opertations. */\
    /* Offset for MPLS operation errors. 0x8000 */\
    SL_RPC_MPLS_START_OFFSET = 0x8000,\
    /* Operation rejected for ALL ILMS due to too many ILMS in the */\
    /* request. 0x8001 */\
    SL_RPC_MPLS_ILM_TOO_MANY_ILMS = 0x8001,\
    /* Operation rejected for all ILMs as server is not initialized. */\
    /* 0x0x8002 */\
    SL_RPC_MPLS_SERVER_NOT_INITIALIZED = 0x8002,\
    /* Operation rejected for all ILMs as the RPC request is */\
    /* not supported for the library's initialization mode. 0x8003 */\
    SL_RPC_MPLS_INIT_MODE_INCOMPATIBLE = 0x8003,\
    /* Operation rejected for ALL label blocks due to too many */\
    /* label blocks in the request. 0x8004 */\
    SL_RPC_MPLS_LABEL_BLK_TOO_MANY_LABEL_BLKS = 0x8004,\
    /* Operation rejected for ALL ILMs as MPLS layer is not registered. */\
    /* 0x8005 */\
    SL_RPC_MPLS_NOT_REGISTERED = 0x8005,\
    /* !!!  MPLS ILM Error codes */\
    /* Offset for MPLS ILM errors. 0x9000 */\
    SL_ILM_ERR_OFFSET = 0x9000,\
    /* MPLS ILM add to service layer failed. 0x9001 */\
    SL_ILM_ADD_FAILED = 0x9001,\
    /* MPLS ILM add to Label Switching Database failed. 0x9002 */\
    SL_ILM_LSD_ADD_FAILED = 0x9002,\
    /* MPLS ILM NHLFE count exceeded max supported number. 0x9003 */\
    SL_ILM_INVALID_NUM_NHLFE = 0x9003,\
    /* MPLS ILM label value out of range. 0x9004 */\
    SL_ILM_INVALID_LABEL = 0x9004,\
    /* MPLS ILM delete from service layer failed. 0x9005 */\
    SL_ILM_DELETE_FAILED = 0x9005,\
    /* MPLS ILM delete from Label Switching Database failed. 0x9006 */\
    SL_ILM_LSD_DELETE_FAILED = 0x9006,\
    /* Number of primary NHLFEs exceeds system capabilities. 0x9007 */\
    SL_ILM_TOOMANY_PRIMARY_NHLFES = 0x9007,\
    /* Number of backup NHLFEs exceeds system capabilities. 0x9008 */\
    SL_ILM_TOOMANY_BACKUP_NHLFES = 0x9008,\
    /* MPLS ILM label alloc failed in Label switching database. 0x9009 */\
    SL_ILM_LSD_ADD_LABEL_ALLOC_FAILED = 0x9009,\
    /* MPLS ILM NHLFE attribute invalid. 0x900a */\
    SL_ILM_LSD_NHLFE_INVALID_ATTRIB = 0x900a,\
    /* MPLS ILM already exists in the database. 0x900b */\
    SL_ILM_EEXIST = 0x900b,\
    /* The ILM database is out of memory. 0x900c */\
    SL_ILM_DB_NOMEM = 0x900c,\
    /* EXP value is outside of the valid range of <0-7>. 0x900d */\
    SL_ILM_INVALID_ELSP_EXP = 0x900d,\
    /* EXP value or Default already set. 0x900e */\
    SL_ILM_ELSP_EXP_OR_DFLT_ALREADY_SET = 0x900e,\
    /* MPLS ILM add operation requested but no paths were provided. 0x900f */\
    SL_ILM_ADD_NO_PATHS = 0x900f,\
    /* MPLS ILM update operation requested but no paths were provided. 0x9010 */\
    SL_ILM_UPDATE_NO_PATHS = 0x9010,\
    /* LSP and ELSP on the same label not supported. 0x9011 */\
    SL_ILM_UNSUPPORTED_ELSP = 0x9011,\
    /* Number of EXP classes on the label exceed system capabilities. 0x9012 */\
    SL_ILM_LABEL_TOOMANY_EXP_CLASSES = 0x9012,\
    /* MPLS ILMs cannot be played to Label Switching Database */\
    /* on a process restart or connection re-establishment. */\
    /* The Forwarding Information Base can */\
    /* can be inconsistent. Agent/Controller should initiate a */\
    /* recovery action by reloading the device. 0x9013 */\
    SL_ILM_REPLAY_FATAL_ERROR = 0x9013,\
    /* MPLS ILMs were played to Label Switching Database */\
    /* on a process restart or connection re-establishment. 0x9014 */\
    SL_ILM_REPLAY_OK = 0x9014,\
    /* ILM's prefix length is invalid. 0x9015 */\
    SL_ILM_INVALID_PREFIX_LEN = 0x9015,\
    /* ILM prefix has host bits set. 0x9016 */\
    SL_ILM_HOST_BITS_SET = 0x9016,\
    /* Size of IPv6 prefix is invalid. 0x9017 */\
    SL_ILM_INVALID_PREFIX_SZ = 0x9017,\
    /* ILM's prefix is invalid. 0x9018 */\
    SL_ILM_INVALID_PREFIX = 0x9018,\
    /* ILM's IPv4 Route prefix is a multicast address. 0x9019 */\
    SL_ILM_INVALID_PREFIX_MCAST = 0x9019,\
    /* VRF name is too long. 0x9020 */\
    SL_ILM_VRF_NAME_TOOLONG = 0x9020,\
    /* VRF's table ID not found. 0x9021 */\
    SL_ILM_VRF_NO_TABLE_ID = 0x9021,\
    /* VRF name of the ILM route not specified. 0x9022 */\
    SL_ILM_VRF_NAME_MISSING = 0x9022,\
    /* !!!  MPLS NHLFE Error codes */\
    /* Offset for MPLS NHLFE errors. 0xa000 */\
    SL_NHLFE_ERR_OFFSET = 0xa000,\
    /* MPLS NHLFE vrf table could not be determined. 0xa001 */\
    SL_NHLFE_NH_NO_TABLE = 0xa001,\
    /* Size of next hop IPv6 address is invalid. 0xa002 */\
    SL_NHLFE_NH_INVALID_ADDR_SZ = 0xa002,\
    /* NHLFE has an invalid next hop address. 0xa003 */\
    SL_NHLFE_INVALID_NEXT_HOP_ADDR = 0xa003,\
    /* Path VRF name exceeds supported length. 0xa004 */\
    SL_NHLFE_VRF_NAME_TOOLONG = 0xa004,\
    /* Next hop interface name is missing from path. 0xa005 */\
    SL_NHLFE_NH_INF_NAME_MISSING = 0xa005,\
    /* Interface name exceeds supported length. 0xa006 */\
    SL_NHLFE_NH_INTF_NAME_TOOLONG = 0xa006,\
    /* Number of labels in the path incompatible with system capabilities  */\
    /* for the given label action. 0xa007 */\
    SL_NHLFE_INVALID_LABEL_COUNT = 0xa007,\
    /* Path id is invalid in NHLFE. 0xa008 */\
    SL_NHLFE_INVALID_PATH_ID = 0xa008,\
    /* MPLS NHLFE label value out of range. 0xa009 */\
    SL_NHLFE_INVALID_LABEL = 0xa009,\
    /* NHLFE has an invalid protection bitmap. 0xa00a */\
    SL_NHLFE_INVALID_PROTECTED_BITMAP = 0xa00a,\
    /* Number of remote backup addresses in the NHLFE exceeds */\
    /* system capabilities. 0xa00b */\
    SL_NHLFE_INVALID_REMOTE_ADDR_COUNT = 0xa00b,\
    /* Size of IPv6 remote backup address is invalid. 0xa00c */\
    SL_NHLFE_REMOTE_ADDR_INVALID_SZ = 0xa00c,\
    /* A primary NHLFE has too many labels. 0xa00d */\
    SL_NHLFE_PRIMARY_TOOMANY_LABELS = 0xa00d,\
    /* A primary NHLFE has too many remote addresses. 0xa00e */\
    SL_NHLFE_PRIMARY_TOOMANY_REMOTE_ADDR = 0xa00e,\
    /* Too many pure backup NHLFE with same Path ID. 0xa00f */\
    SL_NHLFE_BACKUP_ID_REPEATED = 0xa00f,\
    /* Too many primary NHLFE with same Path ID. 0xa010 */\
    SL_NHLFE_PRIMARY_ID_REPEATED = 0xa010,\
    /* Pure backup NHLFE has a empty protected bitmap. 0xa011 */\
    SL_NHLFE_BACKUP_PROTECTED_BITMAP_EMPTY = 0xa011,\
    /* A primary NHLFE has too many backup paths. 0xa012 */\
    SL_NHLFE_PRIMARY_TOOMANY_BACKUP_PATHS = 0xa012,\
    /* A pure backup remote address is invalid. 0xa013 */\
    SL_NHLFE_REMOTE_ADDR_INVALID = 0xa013,\
    /* Protection bitmap of a backup NHLFE refers to a missing path. 0xa014 */\
    SL_NHLFE_BACKUP_MISSING_PRIMARY_PATH = 0xa014,\
    /* NHLFE next-hop missing. 0xa015 */\
    SL_NHLFE_NEXT_HOP_MISSING = 0xa015,\
    /* Label action specified is invalid. 0xa016 */\
    SL_NHLFE_LABEL_ACTION_INVALID = 0xa016,\
    /* NHLFE next hop interface not found. 0xa017 */\
    SL_NHLFE_NH_INTF_NOT_FOUND = 0xa017,\
    /* MPLS NHLFE operation failed. 0xa018 */\
    SL_NHLFE_OPER_FAILED = 0xa018,\
    /* MPLS NHLFE label action missing. 0xa019 */\
    SL_NHLFE_LABEL_ACTION_MISSING = 0xa019,\
    /* Setting EXP value failed. 0xa01a */\
    SL_NHLFE_EXP_SET_FAILED = 0xa01a,\
    /* ELSP protection is unsupported. 0xa01b */\
    SL_NHLFE_ELSP_PROTECTION_UNSUPPORTED = 0xa01b,\
    /* EXP value is outside of the valid range of <0-7>. 0xa01c */\
    SL_NHLFE_INVALID_ELSP_EXP = 0xa01c,\
    /* Path Priority is invalid (valid: 0 or 1). 0xa01d */\
    SL_NHLFE_INVALID_PATH_PRIORITY = 0xa01d,\
    /* Load metric is not zero for a down path. 0xa01e */\
    SL_NHLFE_INVALID_LOAD_METRIC = 0xa01e,\
    /* Set ID value is outside of the valid range of <0-7>. 0xa01f */\
    SL_NHLFE_INVALID_SETID = 0xa01f,\
    /* Two paths with the same Set ID have different path priorities. 0xa020 */\
    SL_NHLFE_INVALID_SETID_PRIORITY = 0xa020,\
    /* Multiple Set IDs are set as the primary. 0xa021 */\
    SL_NHLFE_INVALID_MULTIPLE_PRIMARY_SETIDS = 0xa021,\
    /* Paths with the same SET ID are not contiguous. 0xa022 */\
    SL_NHLFE_NON_CONTIGUOUS_SETIDS = 0xa022,\
    /* Paths with same EXP classification are not contiguous. 0xa023 */\
    SL_NHLFE_NON_CONTIGUOUS_EXP = 0xa023,\
    /* On a ILM, mix of NHLFE with EXP class and others without any EXP class are not allowed. 0xa024 */\
    SL_NHLFE_INCONSISTENT_EXP_ON_PATH = 0xa024,\
    /* !!!  MPLS Label block Error codes */\
    /* Offset for label block errors. 0xb000 */\
    SL_LABEL_BLK_ERR_OFFSET = 0xb000,\
    /* MPLS label block add from Label Switching Database failed. 0xb001 */\
    SL_LABEL_BLK_LSD_ADD_FAILED = 0xb001,\
    /* MPLS label block delete from Label Switching Database failed. 0xb002 */\
    SL_LABEL_BLK_LSD_DELETE_FAILED = 0xb002,\
    /* MPLS label block not found. 0xb003 */\
    SL_LABEL_BLK_LSD_LABEL_BLK_NOT_FOUND = 0xb003,\
    /* MPLS label block in use. 0xb004 */\
    SL_LABEL_BLK_LSD_LABEL_BLK_IN_USE = 0xb004,\
    /* MPLS label block attribute invalid. 0xb005 */\
    SL_LABEL_BLK_LSD_INVALID_ATTRIB = 0xb005,\
    /* MPLS label block size > max size per block. 0xb006 */\
    SL_LABEL_BLK_INVALID_BLOCK_SIZE = 0xb006,\
    /* MPLS label start_label < min label for platform . 0xb007 */\
    SL_LABEL_BLK_INVALID_START_LABEL = 0xb007,\
    /* MPLS label block already exists in the database. 0xb008 */\
    SL_LABEL_BLK_EEXIST = 0xb008,\
    /* MPLS label database is out of memory. 0xb009 */\
    SL_LABEL_BLK_DB_NOMEM = 0xb009,\
    /* MPLS label block type invalid. 0xb00a */\
    SL_LABEL_BLK_TYPE_INVALID = 0xb00a,\
    /* MPLS label block client name exceeds max length. 0xb00b */\
    SL_LABEL_BLK_CLIENT_NAME_TOOLONG = 0xb00b,\
    /* !!!  MPLS Reg error codes */\
    /* Offset for MPLS registration errors. 0xc000 */\
    SL_MPLS_REG_ERR_OFFSET = 0xc000,\
    /* MPLS registration error. 0xc001 */\
    SL_MPLS_REG_ERR = 0xc001,\
    /* MPLS unregistration error. 0xc002 */\
    SL_MPLS_UNREG_ERR = 0xc002,\
    /* MPLS EOF error. 0xc003 */\
    SL_MPLS_EOF_ERR = 0xc003,\
    /* !!! Error codes for Interface operations. */\
    /* Offset for Interface operation errors. 0xd000 */\
    SL_RPC_INTF_START_OFFSET = 0xd000,\
    /* Interface Operation rejected for ALL Sessions as the Interface */\
    /* Session count is beyond supported limit. 0xd001 */\
    SL_RPC_INTF_TOO_MANY_INTERFACES = 0xd001,\
    /* Interface Operation rejected as server is not initialized. 0xd002 */\
    SL_RPC_INTF_SERVER_NOT_INITIALIZED = 0xd002,\
    /* Interface Operation failed as server is not registered with  */\
    /* interface manager. 0xd003 */\
    SL_RPC_INTF_API_CLIENT_NOT_REGISTERED = 0xd003,\
    /* !!! Error codes for Interface objects. */\
    /* Offset for Interface object errors. 0xe000 */\
    SL_INTF_START_OFFSET = 0xe000,\
    /* Interface object's interface name missing. 0xe001 */\
    SL_INTF_INTERFACE_NAME_MISSING = 0xe001,\
    /* Interface object's interface name exceeds supported length. 0xe002 */\
    SL_INTF_INTERFACE_NAME_TOOLONG = 0xe002,\
    /* Interface internal registration error. 0xe003  */\
    SL_INTF_INTERFACE_REG_ERR = 0xe003,\
    /* Internal database error. 0xe004 */\
    SL_INTF_INTERNAL_DB_ERROR = 0xe004,\
    /* Interface Recovery error. 0xe005 */\
    SL_INTF_RECOVERY_ERROR = 0xe005,\
    /* Interface exists. 0xe006 */\
    SL_INTF_INTERFACE_EXISTS = 0xe006,\
    /* Interface not found. 0xe007 */\
    SL_INTF_INTERFACE_NOT_FOUND = 0xe007,\
    /* Interface State not supported. 0xe008 */\
    SL_INTF_INTERFACE_STATE_NOT_SUPPORTED = 0xe008,\
    /* !!! Error codes for Global L2 operations. */\
    /* Offset for Global L2 operation errors. 0xf000 */\
    SL_L2_REG_START_OFFSET = 0xf000,\
    /* Client cannot be registered with Layer-2 RIB. 0xf001 */\
    SL_L2_REGISTRATION_ERR = 0xf001,\
    /* Client cannot be unregistered with Layer-2 RIB. 0xf002 */\
    SL_L2_UNREGISTRATION_ERR = 0xf002,\
    /* EOF Operation error. 0xf003 */\
    SL_L2_EOF_ERR = 0xf003,\
    /* L2 registration message with invalid admin distance. 0xf004 */\
    SL_L2_REG_INVALID_ADMIN_DISTANCE = 0xf004,\
    /* Duplicate L2 registration message. 0xf005 */\
    SL_L2_REG_IS_DUPLICATE = 0xf005,\
    /* L2 registration rejected as server is not initialized. 0xf006 */\
    SL_L2_REG_SERVER_NOT_INITIALIZED = 0xf006,\
    /* !!! Error codes for L2 Bridge-Domain (BD) Operations. */\
    /* Offset for L2 BD operation errors. 0x10000 */\
    SL_RPC_L2_BD_REG_START_OFFSET = 0x10000,\
    /* Operation is rejected for all BDs as name is missing. 0x10001 */\
    SL_RPC_L2_BD_REG_NAME_MISSING = 0x10001,\
    /* Operation rejected for all BDs due to too many BD registration */\
    /* messages in the request. 0x10002 */\
    SL_RPC_L2_BD_REG_TOO_MANY_MSGS = 0x10002,\
    /* Operation rejected for all BDs as server is not initialized. */\
    /* 0x10003 */\
    SL_RPC_L2_BD_REG_SERVER_NOT_INITIALIZED = 0x10003,\
    /* Operation rejected for all BDs as client is not registered. */\
    /* 0x10004 */\
    SL_RPC_L2_BD_REG_CLIENT_NOT_REGISTERED = 0x10004,\
    /* !!! Error codes for L2 Bridge-Domain (BD) Objects. */\
    /* Offset for L2 BD object errors. 0x11000 */\
    SL_L2_BD_REG_START_OFFSET = 0x11000,\
    /* BD cannot be registered with Layer-2 RIB. 0x11001 */\
    SL_L2_BD_REGISTRATION_ERR = 0x11001,\
    /* BD cannot be unregistered with Layer-2 RIB. 0x11002 */\
    SL_L2_BD_UNREGISTRATION_ERR = 0x11002,\
    /* BD EOF Operation error. 0x11003 */\
    SL_L2_BD_EOF_ERR = 0x11003,\
    /* Name is too long in BD registration message. 0x11004 */\
    SL_L2_BD_REG_NAME_TOO_LONG = 0x11004,\
    /* BD not found in BD registration message. 0x11005 */\
    SL_L2_BD_REG_BD_NOT_FOUND = 0x11005,\
    /* !!! Error codes for L2 Route operations. */\
    /* Offset for L2 Route Operation errors. 0x12000 */\
    SL_RPC_L2_ROUTE_START_OFFSET = 0x12000,\
    /* Operation rejected for all L2 routes due to too many messages */\
    /* in the request. 0x12001 */\
    SL_RPC_L2_ROUTE_TOO_MANY_MSGS = 0x12001,\
    /* Operation rejected for all L2 routes as server is not */\
    /* initialized. 0x12002 */\
    SL_RPC_L2_ROUTE_SERVER_NOT_INITIALIZED = 0x12002,\
    /* Operation rejected for all L2 routes as client is not */\
    /* registered. 0x12003 */\
    SL_RPC_L2_ROUTE_CLIENT_NOT_REGISTERED = 0x12003,\
    /* !!! Error codes for L2 Objects. */\
    /* Offset for L2 object errors. 0x13000 */\
    SL_L2_ROUTE_START_OFFSET = 0x13000,\
    /* L2 route operation rejected as BD name is missing. 0x13001 */\
    SL_L2_ROUTE_BD_NAME_MISSING = 0x13001,\
    /* L2 route operation rejected as BD name is too long. 0x13002 */\
    SL_L2_ROUTE_BD_NAME_TOOLONG = 0x13002,\
    /* L2 route operation rejected as BD not found. 0x13003 */\
    SL_L2_ROUTE_BD_NOT_FOUND = 0x13003,\
    /* L2 route operation rejected as BD is not registered. 0x13004 */\
    SL_L2_ROUTE_BD_NOT_REGISTERED = 0x13004,\
    /* L2 route operation rejected due to one or more invalid */\
    /* arguments. 0x13005 */\
    SL_L2_ROUTE_INVALID_ARGS = 0x13005,\
    /* !!! Error codes for L2 Get Notification operations. */\
    /* Offset for L2 Get Notification Operation errors. 0x14000 */\
    SL_RPC_L2_NOTIF_START_OFFSET = 0x14001,\
    /* L2 notification request rejected as server is not initialized. */\
    /* 0x14002 */\
    SL_RPC_L2_NOTIF_SERVER_NOT_INITIALIZED = 0x14002,\
    /* L2 notification request rejected as client is not registered. */\
    /* 0x14003 */\
    SL_RPC_L2_NOTIF_CLIENT_NOT_REGISTERED = 0x14003,\
    /* L2 notification enable error. 0x14004 */\
    SL_RPC_L2_NOTIF_ENABLE_ERR = 0x14004,\
    /* L2 notification disable error. 0x14005 */\
    SL_RPC_L2_NOTIF_DISABLE_ERR = 0x14005,\
    /* L2 notification EOF error. 0x14006 */\
    SL_RPC_L2_NOTIF_EOF_ERR = 0x14006,\
    /* L2 notification request rejected as BD name is missing. 0x14007 */\
    SL_RPC_L2_NOTIF_BD_NAME_MISSING = 0x14007,\
    /* L2 notification request rejected as BD name is too long. */\
    /* 0x14008 */\
    SL_RPC_L2_NOTIF_BD_NAME_TOOLONG = 0x14008,\
    /* L2 notification request rejected as BD not found. 0x14009 */\
    SL_RPC_L2_NOTIF_BD_NOT_FOUND = 0x14009,\
    /* !!! Error codes for path group objects. */\
    /* Container VRF for PathGroup could not be added. 0x15001 */\
    SL_PG_VRF_ADD_ERR = 0x15001,\
    /* PathGroup's VRF ID could not be determined. 0x15002 */\
    SL_PG_VRF_NO_VRFID = 0x15002,\
    /* PathGroup's string key is too long. 0x15003 */\
    SL_PG_STR_KEY_TOOLONG = 0x15003,\
    /* ID of a next hop VRF in a path in the PathGroup cannot be determined. 0x15004 */\
    SL_PG_TARGET_VRF_NO_VRFID = 0x15004,\
    /* PathGroup's string key contains invalid characters. 0x15005 */\
    SL_PG_STR_KEY_INVALID = 0x15005,\
    /* !!! Error codes for Nexthop request objects. */\
    /* Offset for Nexthop request errors. 0x16000 */\
    SL_NEXT_HOP_START_OFFSET = 0x16000,\
    /* Nexthop prefix length is invalid. 0x16001 */\
    SL_NEXT_HOP_INVALID_PREFIX_LEN = 0x16001,\
    /* Nexthop prefix has host bits set. 0x16002 */\
    SL_NEXT_HOP_HOST_BITS_SET = 0x16002,\
    /* IPv4 Route prefix is a multicast address. 0x16003 */\
    SL_NEXT_HOP_INVALID_PREFIX_MCAST = 0x16003,\
    /* Nexthop prefix is invalid. 0x16004 */\
    SL_NEXT_HOP_INVALID_PREFIX = 0x16004,\
    /* Invalid next hop address. 0x16005 */\
    SL_NEXT_HOP_INVALID_NEXT_HOP_ADDR = 0x16005,\
    /* Size of IPv6 prefix is invalid. 0x16006 */\
    SL_NEXT_HOP_INVALID_PREFIX_SZ = 0x16006,\
    /* Unable to program NH tracking registration to RIB. 0x16007 */\
    SL_NEXT_HOP_RIB_ADD_FAILED = 0x16007,\
    /* Unable to program route redist registration to RIB. 0x16008 */\
    SL_ROUTE_REDIST_RIB_ADD_FAILED = 0x16008,\
    /* Offset for Hardware Ack errors. 0x17000 */\
    SL_FIB_START_OFFSET = 0x17000,\
    /* The operation is successfully programmed in hardware. 0x17001 */\
    SL_FIB_SUCCESS = 0x17001,\
    /* FIB programming failure. 0x17002 */\
    SL_FIB_FAILED = 0x17002,\
    /* The operation is not viable to be programmed in hardware at this time. 0x17003 */\
    SL_FIB_INELIGIBLE = 0x17003,\
    /* !!! Error codes for operations on policy objects. */\
    /* Offset for policy object operations. 0x18000 */\
    SL_POLICY_START_OFFSET = 0x18000,\
    /* Policy object could not be created. 0x18001   */\
    SL_POLICY_ADD_ERR = 0x18001,\
    /* Policy object already exists. 0x18002 */\
    SL_POLICY_EXISTS_ERR = 0x18002,\
    /* Policy object delete failed. 0x18003 */\
    SL_POLICY_DELETE_ERR = 0x18003,\
    /* Rule could not be created. 0x18004 */\
    SL_POLICY_RULE_ADD_ERR = 0x18004,\
    /* Rule already exists. 0x18005 */\
    SL_POLICY_RULE_EXISTS_ERR = 0x18005,\
    /* Rule delete error. 0x18006 */\
    SL_POLICY_RULE_DELETE_ERR = 0x18006,\
    /* Policy object apply error. 0x18007 */\
    SL_POLICY_APPLY_ERR = 0x18007,\
    /* Policy object unapply error. 0x18008 */\
    SL_POLICY_UNAPPLY_ERR = 0x18008,\
    /* Operation rejected due to too many policies in the request. 0x18009 */\
    SL_POLICY_TOO_MANY_POLICIES = 0x18009,\
    /* Policy name is too long. 0x1800a */\
    SL_POLICY_NAME_TOO_LONG = 0x1800a,\
    /* Rule name is too long. 0x1800b */\
    SL_POLICY_RULE_NAME_TOO_LONG = 0x1800b,\
    /* Duplicate priority for the rule in the same policy. 0x1800c */\
    SL_POLICY_DUPLICATE_PRIORITY_IN_RULE = 0x1800c,\
    /* Rule modification not allowed. 0x1800d */\
    SL_POLICY_RULE_MOD_NOT_ALLOWED = 0x1800d,\
    /* Rule belongs to a different policy. 0x1800e */\
    SL_POLICY_INVALID_RULE = 0x1800e,\
    /* Rule add operation requested but no rules were provided. 0x1800f */\
    SL_POLICY_RULE_ADD_NO_RULES = 0x1800f, \
    /* Rule add operation requested but no matches were provided. 0x18010 */\
    SL_POLICY_INVALID_MATCH_COUNT_IN_RULE = 0x18010,\
    /* Rule add operation requested but no actions were provided. 0x18011 */\
    SL_POLICY_INVALID_ACTION_COUNT_IN_RULE = 0x18011,\
    /* Policy not found.0x18012 */\
    SL_POLICY_NOT_FOUND = 0x18012,\
    /* Policy invalid. 0x18013 */\
    SL_POLICY_INVALID = 0x18013,\
    /* Policy name missing. 0x18014 */\
    SL_POLICY_NAME_MISSING = 0x18014,\
    /* Rule name missing. 0x18015  */\
    SL_POLICY_RULE_NAME_MISSING = 0x18015,\
    /* Priority missing in rule. 0x18016 */\
    SL_POLICY_PRIORITY_MISSING_IN_RULE = 0x18016,\
    /* Invalid policy type. 0x18017  */\
    SL_POLICY_TYPE_INVALID = 0x18017,\
    /* Invalid policy direction. 0x18018 */\
    SL_POLICY_INVALID_DIRECTION = 0x18018,\
    /* Policy object's interface name exceeds supported length. 0x18019 */\
    SL_POLICY_INTF_NAME_TOOLONG = 0x18019,\
    /* Policy object's interface name is missing. 0x1801a  */\
    SL_POLICY_INTF_NAME_MISSING = 0x1801a,\
    /* Max rule limit within a policy is reached. 0x1801b */\
    SL_POLICY_MAX_RULE_LIMIT_REACHED = 0x1801b,\
    /* Vrf name in policy object is too long. 0x1801c */\
    SL_POLICY_VRF_NAME_TOO_LONG = 0x1801c,\
    /* Vrf name missing in policy object. 0x1801d */\
    SL_POLICY_VRF_NAME_MISSING = 0x1801d,\
    /* Path Group name in policy object too long. 0x1801e */\
    SL_POLICY_PATH_GRP_NAME_TOO_LONG = 0x1801e,\
    /* Path Group name missing in policy object. 0x1801f */\
    SL_POLICY_PATH_GRP_NAME_MISSING = 0x1801f,\
    /* Invalid Dscp Value. 0x18020 */\
    SL_POLICY_INVALID_DSCP_VALUE = 0x18020,\
    /* Priority string too long. 0x18021  */\
    SL_POLICY_PRIORITY_STR_TOO_LONG = 0x18021,\
    /* Max interfaces limit in policy reached. 0x18022 */\
    SL_POLICY_MAX_INTF_LIMIT_REACHED = 0x18022,\
    /* Rule delete operation requested but no rules were provided. 0x18023 */\
    SL_POLICY_RULE_DELETE_NO_RULES = 0x18023,\
    /* Policy apply requested but no interfaces were provided. 0x18024 */\
    SL_POLICY_APPLY_NO_INTFS = 0x18024,\
    /* Policy unapply requested but no interfaces were provided. 0x18025 */\
    SL_POLICY_UNAPPLY_NO_INTFS = 0x18025,\
    /* !!! Error codes Reserved for internal errors. */\
    /* Offset for Internal errors. 0x100000 */\
    SL_INTERNAL_START_OFFSET = 0x100000,\
    /*End of Generated error codes*/



#define SL_GENERATED_ERR_STRINGS \
    {SL_SUCCESS ,        " Success, no errors detected.  "\
        },\
    {SL_NOT_CONNECTED ,\
        " Client not connected.  "\
        },\
    {SL_EAGAIN ,\
        " Operation must be retried.  "\
        },\
    {SL_ENOMEM ,\
        " One or more components does not have sufficient memory.  "\
        },\
    {SL_EBUSY ,\
        " Too many outstanding requests.  "\
        },\
    {SL_EINVAL ,\
        " One or more arguments are invalid.  "\
        },\
    {SL_UNSUPPORTED_VER ,\
        " Unsupported version.  "\
        },\
    {SL_NOT_AVAILABLE ,\
        " Not Available.  "\
        },\
    {SL_STREAM_NOT_SUPPORTED ,\
        " Stream mode not supported.  "\
        },\
    {SL_ENOTSUP ,\
        " Operation not supported.  "\
        },\
    {SL_SOME_ERR ,\
        " One or more objects is errored: "\
        " Each object must be individually examined.  "\
        },\
    {SL_TIMEOUT ,\
        " Operation Timed out. "\
        " The result of the operation is undeterministic (success or fail).  "\
        },\
    {SL_NOTIF_TERM ,\
        " Due to some event, the client will no longer receive notification "\
        " events on this channel.  "\
        " Such events include: "\
        " - Notification Session was hijacked by another client. "\
        },\
    {SL_AUTH_FAIL ,\
        " Authentication failure. "\
        " Incorrect credentials passed in by RPC.  "\
        },\
    {SL_ACK_TYPE_NOT_SUPPORTED ,\
        " Ack type not supported error.  "\
        },\
    {SL_ACK_CADENCE_NOT_SUPPORTED ,\
        " Ack cadence not supported when scope is not defined.  "\
        },\
    {SL_INIT_START_OFFSET ,\
        " Offset for INIT errors.  "\
        },\
    {SL_INIT_STATE_CLEAR ,\
        " Success, no errors detected - clear state. "\
        " This error is returned on the first-ever initialization, or, "\
        " when a fatal event has occured and all previous state was lost.  "\
        },\
    {SL_INIT_STATE_READY ,\
        " Success, no errors detected - previous state is recovered. "\
        " This error is returned on a client re-initialization with "\
        " successful recovery of state. Note that any unacknowledged "\
        " data previously sent should be considered lost.  "\
        },\
    {SL_INIT_UNSUPPORTED_VER ,\
        " Server software incompatible with client software version.  "\
        },\
    {SL_INIT_SERVER_NOT_INITIALIZED ,\
        " Initialization request received while server is not ready.  "\
        },\
    {SL_INIT_SERVER_MODE_CHANGE_FAILED ,\
        " Server operational mode change from stream to non-stream "\
        " or vice-versa failed.  "\
        },\
    {SL_RPC_VRF_START_OFFSET ,\
        " Offset for VRF errors.  "\
        },\
    {SL_RPC_VRF_TOO_MANY_VRF_REG_MSGS ,\
        " Operation rejected for ALL VRFs due to too many VRF registration "\
        " messages in the request.  "\
        },\
    {SL_RPC_VRF_SERVER_NOT_INITIALIZED ,\
        " Operation rejected for all VRFs as server is not initialized.  "\
        },\
    {SL_RPC_VRF_OP_NOTSUP_WITH_AUTOREG ,\
        " Operation not supported in auto-register mode.  "\
        },\
    {SL_VRF_START_OFFSET ,\
        " Offset for VRF errors.  "\
        },\
    {SL_VRF_NAME_TOOLONG ,\
        " VRF name in the VRF registration message is too long.  "\
        },\
    {SL_VRF_NOT_FOUND ,\
        " VRF not found during a unregister or EOF.  "\
        },\
    {SL_VRF_NO_TABLE_ID ,\
        " On a VRF registration, Table ID for the VRF is not found.  "\
        },\
    {SL_VRF_REG_INVALID_ADMIN_DISTANCE ,\
        " VRF add registration message with invalid administrative distance.  "\
        },\
    {SL_VRF_TABLE_ADD_ERR ,\
        " On a VRF registration, Table cannot be added to persistent memory.  "\
        },\
    {SL_VRF_TABLE_REGISTRATION_ERR ,\
        " VRF table cannot be registered with RIB.  "\
        },\
    {SL_VRF_TABLE_UNREGISTRATION_ERR ,\
        " VRF table cannot be unregistered with RIB.  "\
        },\
    {SL_VRF_TABLE_EOF_ERR ,\
        " VRF table RIB EOF operation error.  "\
        },\
    {SL_VRF_REG_VRF_NAME_MISSING ,\
        " VRF registration message does not have a VRF name.  "\
        },\
    {SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR ,\
        " IPv4 routes in VRF cannot be played to Routing Information Base "\
        " on a process restart or connection re-establishment. "\
        " The Forwarding Information Base can "\
        " can be inconsistent. Agent/Controller should initiate a "\
        " recovery action by reloading the device.  "\
        },\
    {SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR ,\
        " IPv6 routes in VRF cannot be played to Routing Information Base "\
        " on a process restart or connection re-establishment. "\
        " The Forwarding Information Base can "\
        " can be inconsistent. Agent/Controller should initiate a "\
        " recovery action by reloading the device.  "\
        },\
    {SL_VRF_V4_ROUTE_REPLAY_OK ,\
        " IPv4 routes in VRF were played to Routing Information Base "\
        " on a process restart or connection re-establishment.  "\
        },\
    {SL_VRF_V6_ROUTE_REPLAY_OK ,\
        " IPv6 routes in VRF were played to Routing Information Base "\
        " on a process restart or connection re-establishment.  "\
        },\
    {SL_RPC_ROUTE_START_OFFSET ,\
        " Offset for Route operation errors.  "\
        },\
    {SL_RPC_ROUTE_TOO_MANY_ROUTES ,\
        " Operation rejected for ALL routes due to too many routes in the "\
        " request.  "\
        },\
    {SL_RPC_ROUTE_VRF_NAME_TOOLONG ,\
        " Operation rejected for ALL routes as the request's VRF name "\
        " is too long.  "\
        },\
    {SL_RPC_ROUTE_VRF_NOT_FOUND ,\
        " Operation rejected for ALL routes as VRF for the given name "\
        " is not found.  "\
        },\
    {SL_RPC_ROUTE_VRF_NO_TABLE ,\
        " Operation rejected for ALL routes as VRF's Table ID is not found. "\
        "  "\
        },\
    {SL_RPC_ROUTE_VRF_TABLE_NOT_REGISTERED ,\
        " Operation rejected for ALL routes as VRF is not registered with RIB. "\
        "  "\
        },\
    {SL_RPC_ROUTE_VRF_NAME_MISSING ,\
        " Route Operation rejected for ALL objects as VRF name is missing. "\
        "  "\
        },\
    {SL_RPC_ROUTE_INIT_MODE_INCOMPATIBLE ,\
        " Operation rejected for all routes as the RPC request is "\
        " not supported for the library's initialization mode.  "\
        },\
    {SL_RPC_ROUTE_SERVER_NOT_INITIALIZED ,\
        " Operation rejected for all routes as server is not initialized. "\
        "  "\
        },\
    {SL_RPC_ROUTE_NOTIF_SRC_PROTO_TOOLONG ,\
        " Operation rejected as the request's SrcProto is too long.  "\
        },\
    {SL_RPC_ROUTE_NOTIF_SRC_PROTO_TAG_TOOLONG ,\
        " Operation rejected as the request's SrcProtoTag is too long.  "\
        },\
    {SL_RPC_ROUTE_GET_MATCH_INVALID ,\
        " Operation rejected as the requested match value/values/criteria is invalid.  "\
        },\
    {SL_RPC_ROUTE_GET_MATCH_NOTSUP ,\
        " Operation rejected as the requested match value/values/criteria is not supported.  "\
        },\
    {SL_ROUTE_START_OFFSET ,\
        " Offset for route errors.  "\
        },\
    {SL_ROUTE_ADD_NO_PATHS ,\
        " Route add operation requested but no paths were provided.  "\
        },\
    {SL_ROUTE_UPDATE_NO_PATHS ,\
        " Route update operation requested but no paths were provided.  "\
        },\
    {SL_ROUTE_INVALID_PREFIX_LEN ,\
        " Route's prefix length is invalid.  "\
        },\
    {SL_ROUTE_INVALID_ADMIN_DISTANCE ,\
        " Route's admininstrative distance is invalid.  "\
        },\
    {SL_ROUTE_INVALID_NUM_PATHS ,\
        " Route's number of paths exceeds system capabilities.  "\
        },\
    {SL_ROUTE_INVALID_PREFIX_SZ ,\
        " Size of IPv6 prefix is invalid.  "\
        },\
    {SL_ROUTE_INVALID_PREFIX ,\
        " Route's prefix is invalid.  "\
        },\
    {SL_ROUTE_ERR_RIB_TABLE_LIMIT_REACHED ,\
        " Route programming failed in RIB as VRF table limit reached.  "\
        },\
    {SL_ROUTE_ERR_RIB_INVALID_ARGS ,\
        " RIB route programming failed in RIB due to invalid arguments.  "\
        },\
    {SL_ROUTE_ERR_RIB_PATH_TABLE_LIMIT ,\
        " One or more paths could not be programmed in RIB as VRF "\
        " table limit reached.  "\
        },\
    {SL_ROUTE_ERR_RIB_TOOMANYPATHS ,\
        " One or more paths could not be programmed in RIB as number of paths "\
        " reached system limit.  "\
        },\
    {SL_ROUTE_EEXIST ,\
        " This route already exists in the database.  "\
        },\
    {SL_ROUTE_HOST_BITS_SET ,\
        " Route prefix has host bits set.  "\
        },\
    {SL_ROUTE_INVALID_PREFIX_MCAST ,\
        " IPv4 Route prefix is a multicast address.  "\
        },\
    {SL_ROUTE_PATH_AFI_MISMATCH ,\
        " Route and Path AFI does not match.  "\
        },\
    {SL_ROUTE_TOOMANY_PRIMARY_PATHS ,\
        " Number of primary paths exceeds system capabilities.  "\
        },\
    {SL_ROUTE_TOOMANY_BACKUP_PATHS ,\
        " Number of backup paths exceeds system capabilities.  "\
        },\
    {SL_ROUTE_DB_NOMEM ,\
        " The route database is out of memory.  "\
        },\
    {SL_ROUTE_INVALID_LOCAL_LABEL ,\
        " The route has an invalid local label.  "\
        },\
    {SL_ROUTE_INVALID_FLAGS ,\
        " Invalid route flags.  "\
        },\
    {SL_PATH_START_OFFSET ,\
        " Offset for route path errors.  "\
        },\
    {SL_PATH_NH_NO_TABLE ,\
        " VRF table for the path could not be determined.  "\
        },\
    {SL_PATH_NH_INTF_NOT_FOUND ,\
        " Path next hop interface not found.  "\
        },\
    {SL_PATH_INVALID_LABEL_COUNT ,\
        " Number of labels in the path exceeds system capabilities.  "\
        },\
    {SL_PATH_INVALID_ID ,\
        " Path ID assigned to the path falls outside the supported range.  "\
        },\
    {SL_PATH_VRF_NAME_TOOLONG ,\
        " Path VRF name exceeds supported length.  "\
        },\
    {SL_PATH_NH_INTF_NAME_TOOLONG ,\
        " Path next hop interface name exceeds supported length.  "\
        },\
    {SL_PATH_NH_INVALID_ADDR_SZ ,\
        " Size of next hop IPv6 address is invalid.  "\
        },\
    {SL_PATH_NH_INF_NAME_MISSING ,\
        " Next hop interface name is missing from path.  "\
        },\
    {SL_PATH_INVALID_NEXT_HOP_ADDR ,\
        " Path has an invalid next hop address.  "\
        },\
    {SL_PATH_INVALID_REMOTE_ADDR_COUNT ,\
        " Number of remote backup addresses in the path exceeds "\
        " system capabilities.  "\
        },\
    {SL_PATH_REMOTE_ADDR_INVALID_SZ ,\
        " Size of IPv6 remote backup address is invalid.  "\
        },\
    {SL_PATH_REMOTE_ADDR_AFI_MISMATCH ,\
        " Route and Path remote backup address AFI does not match.  "\
        },\
    {SL_PATH_INVALID_PROTECTED_BITMAP ,\
        " Path has an invalid protection bitmap.  "\
        },\
    {SL_PATH_BACKUP_MISSING_PRIMARY_PATH ,\
        " Protection bitmap of a backup path refers to a missing path.  "\
        },\
    {SL_PATH_PRIMARY_ID_REPEATED ,\
        " Too many primary paths with same Path ID.  "\
        },\
    {SL_PATH_BACKUP_ID_REPEATED ,\
        " Too many pure backup paths with same Path ID.  "\
        },\
    {SL_PATH_PRIMARY_TOOMANY_BACKUP_PATHS ,\
        " A primary path has too many backup paths.  "\
        },\
    {SL_PATH_PRIMARY_TOOMANY_LABELS ,\
        " A primary path has too many labels.  "\
        },\
    {SL_PATH_PRIMARY_TOOMANY_REMOTE_ADDR ,\
        " A primary path has too many remote addresses.  "\
        },\
    {SL_PATH_REMOTE_ADDR_INVALID ,\
        " A pure backup remote address is invalid.  "\
        },\
    {SL_PATH_INVALID_LABEL ,\
        " Path has an invalid label.  "\
        },\
    {SL_PATH_ROUTER_MAC_ADDR_INVALID_SZ ,\
        " Size of router mac address is invalid.  "\
        },\
    {SL_PATH_BACKUP_TOOMANY_LABELS ,\
        " A backup path has too many labels.  "\
        },\
    {SL_PATH_INVALID_VNI ,\
        " Invalid VNI for VxLAN encap.  "\
        },\
    {SL_PATH_INVALID_ENCAP_ADDR ,\
        " Path has an invalid  encap address.  "\
        },\
    {SL_PATH_ENCAP_SRC_DST_AFI_MISMATCH ,\
        " Path encapsulation source and destination AFI mismatch.  "\
        },\
    {SL_PATH_RTR_MAC_NOSUP ,\
        " PATH router mac is not supported with VxLAN path attributes.  "\
        },\
    {SL_PATH_ENCAP_TYPE_MISMATCH ,\
        " Path Encap type attribute does not match specified encapsulation.  "\
        },\
    {SL_RPC_BFD_START_OFFSET ,\
        " Offset for BFD operation errors.  "\
        },\
    {SL_RPC_BFD_TOO_MANY_BFD_SESSIONS ,\
        " BFD Operation rejected for ALL Sessions as the BFD Session count "\
        " is beyond supported limit.  "\
        },\
    {SL_RPC_BFD_API_BAD_PARAMETER ,\
        " BFD Operation rejected due to one or many invalid parameters.  "\
        },\
    {SL_RPC_BFD_API_CLIENT_NOT_REGISTERED ,\
        " BFD Operation failed as server is not registered with BFD.  "\
        },\
    {SL_RPC_BFD_API_INTERNAL_ERROR ,\
        " BFD Operation failed with internal error.  "\
        },\
    {SL_RPC_BFD_SERVER_NOT_INITIALIZED ,\
        " BFD Operation rejected as server is not initialized.  "\
        },\
    {SL_RPC_BFD_V4_NOT_REGISTERED ,\
        " BFD IPv4 not registered.  "\
        },\
    {SL_RPC_BFD_V6_NOT_REGISTERED ,\
        " BFD IPv6 not registered.  "\
        },\
    {SL_BFD_START_OFFSET ,\
        " Offset for BFD errors.  "\
        },\
    {SL_BFD_INTF_NAME_TOOLONG ,\
        " BFD Session's interface name exceeds supported length.  "\
        },\
    {SL_BFD_INTF_NOT_FOUND ,\
        " BFD Session's interface not found.  "\
        },\
    {SL_BFD_INVALID_ATTRIBUTE ,\
        " BFD Session's tx interval or multiplier are beyond the  "\
        " supported range.  "\
        },\
    {SL_BFD_INTF_NAME_MISSING ,\
        " BFD Session's interface name is missing.  "\
        },\
    {SL_BFD_INVALID_NBR_MCAST ,\
        " BFD Session's neighbor is mcast address.  "\
        },\
    {SL_BFD_INVALID_NBR ,\
        " BFD Session's neighbor address is invalid.  "\
        },\
    {SL_BFD_VRF_NAME_TOOLONG ,\
        " BFD Session's VRF Name is too long.  "\
        },\
    {SL_BFD_BAD_PARAMETER ,\
        " BFD Session's one or more parameters are invalid.  "\
        " For example, Multihop BFD can not have the interface name set.  "\
        },\
    {SL_BFD_API_INTERNAL_ERROR ,\
        " BFD Session failed with internal error.  "\
        },\
    {SL_BFD_VRF_NOT_FOUND ,\
        " BFD Session's VRF not found.  "\
        },\
    {SL_BFD_INVALID_PREFIX_SIZE ,\
        " BFD Session's neighbor IPv6 prefix size is invalid.  "\
        },\
    {SL_BFD_INVALID_SESSION_TYPE ,\
        " BFD Session type invalid.  "\
        },\
    {SL_BFD_INVALID_VRF ,\
        " BFD Session's VRF is Invalid.  "\
        },\
    {SL_BFD_SESSION_NOT_FOUND ,\
        " BFD Session not found.  "\
        },\
    {SL_BFD_SESSION_EXISTS ,\
        " BFD Session exists.  "\
        },\
    {SL_BFD_INTERNAL_DB_ERROR ,\
        " BFD Internal database error.  "\
        },\
    {SL_BFD_RECOVERY_ERROR ,\
        " BFD Recovery error.  "\
        },\
    {SL_RPC_MPLS_START_OFFSET ,\
        " Offset for MPLS operation errors.  "\
        },\
    {SL_RPC_MPLS_ILM_TOO_MANY_ILMS ,\
        " Operation rejected for ALL ILMS due to too many ILMS in the "\
        " request.  "\
        },\
    {SL_RPC_MPLS_SERVER_NOT_INITIALIZED ,\
        " Operation rejected for all ILMs as server is not initialized. "\
        "  "\
        },\
    {SL_RPC_MPLS_INIT_MODE_INCOMPATIBLE ,\
        " Operation rejected for all ILMs as the RPC request is "\
        " not supported for the library's initialization mode.  "\
        },\
    {SL_RPC_MPLS_LABEL_BLK_TOO_MANY_LABEL_BLKS ,\
        " Operation rejected for ALL label blocks due to too many "\
        " label blocks in the request.  "\
        },\
    {SL_RPC_MPLS_NOT_REGISTERED ,\
        " Operation rejected for ALL ILMs as MPLS layer is not registered. "\
        "  "\
        },\
    {SL_ILM_ERR_OFFSET ,\
        " Offset for MPLS ILM errors.  "\
        },\
    {SL_ILM_ADD_FAILED ,\
        " MPLS ILM add to service layer failed.  "\
        },\
    {SL_ILM_LSD_ADD_FAILED ,\
        " MPLS ILM add to Label Switching Database failed.  "\
        },\
    {SL_ILM_INVALID_NUM_NHLFE ,\
        " MPLS ILM NHLFE count exceeded max supported number.  "\
        },\
    {SL_ILM_INVALID_LABEL ,\
        " MPLS ILM label value out of range.  "\
        },\
    {SL_ILM_DELETE_FAILED ,\
        " MPLS ILM delete from service layer failed.  "\
        },\
    {SL_ILM_LSD_DELETE_FAILED ,\
        " MPLS ILM delete from Label Switching Database failed.  "\
        },\
    {SL_ILM_TOOMANY_PRIMARY_NHLFES ,\
        " Number of primary NHLFEs exceeds system capabilities.  "\
        },\
    {SL_ILM_TOOMANY_BACKUP_NHLFES ,\
        " Number of backup NHLFEs exceeds system capabilities.  "\
        },\
    {SL_ILM_LSD_ADD_LABEL_ALLOC_FAILED ,\
        " MPLS ILM label alloc failed in Label switching database.  "\
        },\
    {SL_ILM_LSD_NHLFE_INVALID_ATTRIB ,\
        " MPLS ILM NHLFE attribute invalid.  "\
        },\
    {SL_ILM_EEXIST ,\
        " MPLS ILM already exists in the database.  "\
        },\
    {SL_ILM_DB_NOMEM ,\
        " The ILM database is out of memory.  "\
        },\
    {SL_ILM_INVALID_ELSP_EXP ,\
        " EXP value is outside of the valid range of <0-7>.  "\
        },\
    {SL_ILM_ELSP_EXP_OR_DFLT_ALREADY_SET ,\
        " EXP value or Default already set.  "\
        },\
    {SL_ILM_ADD_NO_PATHS ,\
        " MPLS ILM add operation requested but no paths were provided.  "\
        },\
    {SL_ILM_UPDATE_NO_PATHS ,\
        " MPLS ILM update operation requested but no paths were provided.  "\
        },\
    {SL_ILM_UNSUPPORTED_ELSP ,\
        " LSP and ELSP on the same label not supported.  "\
        },\
    {SL_ILM_LABEL_TOOMANY_EXP_CLASSES ,\
        " Number of EXP classes on the label exceed system capabilities.  "\
        },\
    {SL_ILM_REPLAY_FATAL_ERROR ,\
        " MPLS ILMs cannot be played to Label Switching Database "\
        " on a process restart or connection re-establishment. "\
        " The Forwarding Information Base can "\
        " can be inconsistent. Agent/Controller should initiate a "\
        " recovery action by reloading the device.  "\
        },\
    {SL_ILM_REPLAY_OK ,\
        " MPLS ILMs were played to Label Switching Database "\
        " on a process restart or connection re-establishment.  "\
        },\
    {SL_ILM_INVALID_PREFIX_LEN ,\
        " ILM's prefix length is invalid.  "\
        },\
    {SL_ILM_HOST_BITS_SET ,\
        " ILM prefix has host bits set.  "\
        },\
    {SL_ILM_INVALID_PREFIX_SZ ,\
        " Size of IPv6 prefix is invalid.  "\
        },\
    {SL_ILM_INVALID_PREFIX ,\
        " ILM's prefix is invalid.  "\
        },\
    {SL_ILM_INVALID_PREFIX_MCAST ,\
        " ILM's IPv4 Route prefix is a multicast address.  "\
        },\
    {SL_ILM_VRF_NAME_TOOLONG ,\
        " VRF name is too long.  "\
        },\
    {SL_ILM_VRF_NO_TABLE_ID ,\
        " VRF's table ID not found.  "\
        },\
    {SL_ILM_VRF_NAME_MISSING ,\
        " VRF name of the ILM route not specified.  "\
        },\
    {SL_NHLFE_ERR_OFFSET ,\
        " Offset for MPLS NHLFE errors.  "\
        },\
    {SL_NHLFE_NH_NO_TABLE ,\
        " MPLS NHLFE vrf table could not be determined.  "\
        },\
    {SL_NHLFE_NH_INVALID_ADDR_SZ ,\
        " Size of next hop IPv6 address is invalid.  "\
        },\
    {SL_NHLFE_INVALID_NEXT_HOP_ADDR ,\
        " NHLFE has an invalid next hop address.  "\
        },\
    {SL_NHLFE_VRF_NAME_TOOLONG ,\
        " Path VRF name exceeds supported length.  "\
        },\
    {SL_NHLFE_NH_INF_NAME_MISSING ,\
        " Next hop interface name is missing from path.  "\
        },\
    {SL_NHLFE_NH_INTF_NAME_TOOLONG ,\
        " Interface name exceeds supported length.  "\
        },\
    {SL_NHLFE_INVALID_LABEL_COUNT ,\
        " Number of labels in the path incompatible with system capabilities  "\
        " for the given label action.  "\
        },\
    {SL_NHLFE_INVALID_PATH_ID ,\
        " Path id is invalid in NHLFE.  "\
        },\
    {SL_NHLFE_INVALID_LABEL ,\
        " MPLS NHLFE label value out of range.  "\
        },\
    {SL_NHLFE_INVALID_PROTECTED_BITMAP ,\
        " NHLFE has an invalid protection bitmap.  "\
        },\
    {SL_NHLFE_INVALID_REMOTE_ADDR_COUNT ,\
        " Number of remote backup addresses in the NHLFE exceeds "\
        " system capabilities.  "\
        },\
    {SL_NHLFE_REMOTE_ADDR_INVALID_SZ ,\
        " Size of IPv6 remote backup address is invalid.  "\
        },\
    {SL_NHLFE_PRIMARY_TOOMANY_LABELS ,\
        " A primary NHLFE has too many labels.  "\
        },\
    {SL_NHLFE_PRIMARY_TOOMANY_REMOTE_ADDR ,\
        " A primary NHLFE has too many remote addresses.  "\
        },\
    {SL_NHLFE_BACKUP_ID_REPEATED ,\
        " Too many pure backup NHLFE with same Path ID.  "\
        },\
    {SL_NHLFE_PRIMARY_ID_REPEATED ,\
        " Too many primary NHLFE with same Path ID.  "\
        },\
    {SL_NHLFE_BACKUP_PROTECTED_BITMAP_EMPTY ,\
        " Pure backup NHLFE has a empty protected bitmap.  "\
        },\
    {SL_NHLFE_PRIMARY_TOOMANY_BACKUP_PATHS ,\
        " A primary NHLFE has too many backup paths.  "\
        },\
    {SL_NHLFE_REMOTE_ADDR_INVALID ,\
        " A pure backup remote address is invalid.  "\
        },\
    {SL_NHLFE_BACKUP_MISSING_PRIMARY_PATH ,\
        " Protection bitmap of a backup NHLFE refers to a missing path.  "\
        },\
    {SL_NHLFE_NEXT_HOP_MISSING ,\
        " NHLFE next-hop missing.  "\
        },\
    {SL_NHLFE_LABEL_ACTION_INVALID ,\
        " Label action specified is invalid.  "\
        },\
    {SL_NHLFE_NH_INTF_NOT_FOUND ,\
        " NHLFE next hop interface not found.  "\
        },\
    {SL_NHLFE_OPER_FAILED ,\
        " MPLS NHLFE operation failed.  "\
        },\
    {SL_NHLFE_LABEL_ACTION_MISSING ,\
        " MPLS NHLFE label action missing.  "\
        },\
    {SL_NHLFE_EXP_SET_FAILED ,\
        " Setting EXP value failed.  "\
        },\
    {SL_NHLFE_ELSP_PROTECTION_UNSUPPORTED ,\
        " ELSP protection is unsupported.  "\
        },\
    {SL_NHLFE_INVALID_ELSP_EXP ,\
        " EXP value is outside of the valid range of <0-7>.  "\
        },\
    {SL_NHLFE_INVALID_PATH_PRIORITY ,\
        " Path Priority is invalid (valid: 0 or 1).  "\
        },\
    {SL_NHLFE_INVALID_LOAD_METRIC ,\
        " Load metric is not zero for a down path.  "\
        },\
    {SL_NHLFE_INVALID_SETID ,\
        " Set ID value is outside of the valid range of <0-7>.  "\
        },\
    {SL_NHLFE_INVALID_SETID_PRIORITY ,\
        " Two paths with the same Set ID have different path priorities.  "\
        },\
    {SL_NHLFE_INVALID_MULTIPLE_PRIMARY_SETIDS ,\
        " Multiple Set IDs are set as the primary.  "\
        },\
    {SL_NHLFE_NON_CONTIGUOUS_SETIDS ,\
        " Paths with the same SET ID are not contiguous.  "\
        },\
    {SL_NHLFE_NON_CONTIGUOUS_EXP ,\
        " Paths with same EXP classification are not contiguous.  "\
        },\
    {SL_NHLFE_INCONSISTENT_EXP_ON_PATH ,\
        " On a ILM, mix of NHLFE with EXP class and others without any EXP class are not allowed.  "\
        },\
    {SL_LABEL_BLK_ERR_OFFSET ,\
        " Offset for label block errors.  "\
        },\
    {SL_LABEL_BLK_LSD_ADD_FAILED ,\
        " MPLS label block add from Label Switching Database failed.  "\
        },\
    {SL_LABEL_BLK_LSD_DELETE_FAILED ,\
        " MPLS label block delete from Label Switching Database failed.  "\
        },\
    {SL_LABEL_BLK_LSD_LABEL_BLK_NOT_FOUND ,\
        " MPLS label block not found.  "\
        },\
    {SL_LABEL_BLK_LSD_LABEL_BLK_IN_USE ,\
        " MPLS label block in use.  "\
        },\
    {SL_LABEL_BLK_LSD_INVALID_ATTRIB ,\
        " MPLS label block attribute invalid.  "\
        },\
    {SL_LABEL_BLK_INVALID_BLOCK_SIZE ,\
        " MPLS label block size > max size per block.  "\
        },\
    {SL_LABEL_BLK_INVALID_START_LABEL ,\
        " MPLS label start_label < min label for platform .  "\
        },\
    {SL_LABEL_BLK_EEXIST ,\
        " MPLS label block already exists in the database.  "\
        },\
    {SL_LABEL_BLK_DB_NOMEM ,\
        " MPLS label database is out of memory.  "\
        },\
    {SL_LABEL_BLK_TYPE_INVALID ,\
        " MPLS label block type invalid.  "\
        },\
    {SL_LABEL_BLK_CLIENT_NAME_TOOLONG ,\
        " MPLS label block client name exceeds max length.  "\
        },\
    {SL_MPLS_REG_ERR_OFFSET ,\
        " Offset for MPLS registration errors.  "\
        },\
    {SL_MPLS_REG_ERR ,\
        " MPLS registration error.  "\
        },\
    {SL_MPLS_UNREG_ERR ,\
        " MPLS unregistration error.  "\
        },\
    {SL_MPLS_EOF_ERR ,\
        " MPLS EOF error.  "\
        },\
    {SL_RPC_INTF_START_OFFSET ,\
        " Offset for Interface operation errors.  "\
        },\
    {SL_RPC_INTF_TOO_MANY_INTERFACES ,\
        " Interface Operation rejected for ALL Sessions as the Interface "\
        " Session count is beyond supported limit.  "\
        },\
    {SL_RPC_INTF_SERVER_NOT_INITIALIZED ,\
        " Interface Operation rejected as server is not initialized.  "\
        },\
    {SL_RPC_INTF_API_CLIENT_NOT_REGISTERED ,\
        " Interface Operation failed as server is not registered with  "\
        " interface manager.  "\
        },\
    {SL_INTF_START_OFFSET ,\
        " Offset for Interface object errors.  "\
        },\
    {SL_INTF_INTERFACE_NAME_MISSING ,\
        " Interface object's interface name missing.  "\
        },\
    {SL_INTF_INTERFACE_NAME_TOOLONG ,\
        " Interface object's interface name exceeds supported length.  "\
        },\
    {SL_INTF_INTERFACE_REG_ERR ,\
        " Interface internal registration error.  "\
        },\
    {SL_INTF_INTERNAL_DB_ERROR ,\
        " Internal database error.  "\
        },\
    {SL_INTF_RECOVERY_ERROR ,\
        " Interface Recovery error.  "\
        },\
    {SL_INTF_INTERFACE_EXISTS ,\
        " Interface exists.  "\
        },\
    {SL_INTF_INTERFACE_NOT_FOUND ,\
        " Interface not found.  "\
        },\
    {SL_INTF_INTERFACE_STATE_NOT_SUPPORTED ,\
        " Interface State not supported.  "\
        },\
    {SL_L2_REG_START_OFFSET ,\
        " Offset for Global L2 operation errors.  "\
        },\
    {SL_L2_REGISTRATION_ERR ,\
        " Client cannot be registered with Layer-2 RIB.  "\
        },\
    {SL_L2_UNREGISTRATION_ERR ,\
        " Client cannot be unregistered with Layer-2 RIB.  "\
        },\
    {SL_L2_EOF_ERR ,\
        " EOF Operation error.  "\
        },\
    {SL_L2_REG_INVALID_ADMIN_DISTANCE ,\
        " L2 registration message with invalid admin distance.  "\
        },\
    {SL_L2_REG_IS_DUPLICATE ,\
        " Duplicate L2 registration message.  "\
        },\
    {SL_L2_REG_SERVER_NOT_INITIALIZED ,\
        " L2 registration rejected as server is not initialized.  "\
        },\
    {SL_RPC_L2_BD_REG_START_OFFSET ,\
        " Offset for L2 BD operation errors.  "\
        },\
    {SL_RPC_L2_BD_REG_NAME_MISSING ,\
        " Operation is rejected for all BDs as name is missing.  "\
        },\
    {SL_RPC_L2_BD_REG_TOO_MANY_MSGS ,\
        " Operation rejected for all BDs due to too many BD registration "\
        " messages in the request.  "\
        },\
    {SL_RPC_L2_BD_REG_SERVER_NOT_INITIALIZED ,\
        " Operation rejected for all BDs as server is not initialized. "\
        "  "\
        },\
    {SL_RPC_L2_BD_REG_CLIENT_NOT_REGISTERED ,\
        " Operation rejected for all BDs as client is not registered. "\
        "  "\
        },\
    {SL_L2_BD_REG_START_OFFSET ,\
        " Offset for L2 BD object errors.  "\
        },\
    {SL_L2_BD_REGISTRATION_ERR ,\
        " BD cannot be registered with Layer-2 RIB.  "\
        },\
    {SL_L2_BD_UNREGISTRATION_ERR ,\
        " BD cannot be unregistered with Layer-2 RIB.  "\
        },\
    {SL_L2_BD_EOF_ERR ,\
        " BD EOF Operation error.  "\
        },\
    {SL_L2_BD_REG_NAME_TOO_LONG ,\
        " Name is too long in BD registration message.  "\
        },\
    {SL_L2_BD_REG_BD_NOT_FOUND ,\
        " BD not found in BD registration message.  "\
        },\
    {SL_RPC_L2_ROUTE_START_OFFSET ,\
        " Offset for L2 Route Operation errors.  "\
        },\
    {SL_RPC_L2_ROUTE_TOO_MANY_MSGS ,\
        " Operation rejected for all L2 routes due to too many messages "\
        " in the request.  "\
        },\
    {SL_RPC_L2_ROUTE_SERVER_NOT_INITIALIZED ,\
        " Operation rejected for all L2 routes as server is not "\
        " initialized.  "\
        },\
    {SL_RPC_L2_ROUTE_CLIENT_NOT_REGISTERED ,\
        " Operation rejected for all L2 routes as client is not "\
        " registered.  "\
        },\
    {SL_L2_ROUTE_START_OFFSET ,\
        " Offset for L2 object errors.  "\
        },\
    {SL_L2_ROUTE_BD_NAME_MISSING ,\
        " L2 route operation rejected as BD name is missing.  "\
        },\
    {SL_L2_ROUTE_BD_NAME_TOOLONG ,\
        " L2 route operation rejected as BD name is too long.  "\
        },\
    {SL_L2_ROUTE_BD_NOT_FOUND ,\
        " L2 route operation rejected as BD not found.  "\
        },\
    {SL_L2_ROUTE_BD_NOT_REGISTERED ,\
        " L2 route operation rejected as BD is not registered.  "\
        },\
    {SL_L2_ROUTE_INVALID_ARGS ,\
        " L2 route operation rejected due to one or more invalid "\
        " arguments.  "\
        },\
    {SL_RPC_L2_NOTIF_START_OFFSET ,\
        " Offset for L2 Get Notification Operation errors.  "\
        },\
    {SL_RPC_L2_NOTIF_SERVER_NOT_INITIALIZED ,\
        " L2 notification request rejected as server is not initialized. "\
        "  "\
        },\
    {SL_RPC_L2_NOTIF_CLIENT_NOT_REGISTERED ,\
        " L2 notification request rejected as client is not registered. "\
        "  "\
        },\
    {SL_RPC_L2_NOTIF_ENABLE_ERR ,\
        " L2 notification enable error.  "\
        },\
    {SL_RPC_L2_NOTIF_DISABLE_ERR ,\
        " L2 notification disable error.  "\
        },\
    {SL_RPC_L2_NOTIF_EOF_ERR ,\
        " L2 notification EOF error.  "\
        },\
    {SL_RPC_L2_NOTIF_BD_NAME_MISSING ,\
        " L2 notification request rejected as BD name is missing.  "\
        },\
    {SL_RPC_L2_NOTIF_BD_NAME_TOOLONG ,\
        " L2 notification request rejected as BD name is too long. "\
        "  "\
        },\
    {SL_RPC_L2_NOTIF_BD_NOT_FOUND ,\
        " L2 notification request rejected as BD not found.  "\
        },\
    {SL_PG_VRF_ADD_ERR ,\
        " Container VRF for PathGroup could not be added.  "\
        },\
    {SL_PG_VRF_NO_VRFID ,\
        " PathGroup's VRF ID could not be determined.  "\
        },\
    {SL_PG_STR_KEY_TOOLONG ,\
        " PathGroup's string key is too long.  "\
        },\
    {SL_PG_TARGET_VRF_NO_VRFID ,\
        " ID of a next hop VRF in a path in the PathGroup cannot be determined.  "\
        },\
    {SL_PG_STR_KEY_INVALID ,\
        " PathGroup's string key contains invalid characters.  "\
        },\
    {SL_NEXT_HOP_START_OFFSET ,\
        " Offset for Nexthop request errors.  "\
        },\
    {SL_NEXT_HOP_INVALID_PREFIX_LEN ,\
        " Nexthop prefix length is invalid.  "\
        },\
    {SL_NEXT_HOP_HOST_BITS_SET ,\
        " Nexthop prefix has host bits set.  "\
        },\
    {SL_NEXT_HOP_INVALID_PREFIX_MCAST ,\
        " IPv4 Route prefix is a multicast address.  "\
        },\
    {SL_NEXT_HOP_INVALID_PREFIX ,\
        " Nexthop prefix is invalid.  "\
        },\
    {SL_NEXT_HOP_INVALID_NEXT_HOP_ADDR ,\
        " Invalid next hop address.  "\
        },\
    {SL_NEXT_HOP_INVALID_PREFIX_SZ ,\
        " Size of IPv6 prefix is invalid.  "\
        },\
    {SL_NEXT_HOP_RIB_ADD_FAILED ,\
        " Unable to program NH tracking registration to RIB.  "\
        },\
    {SL_ROUTE_REDIST_RIB_ADD_FAILED ,\
        " Unable to program route redist registration to RIB.  "\
        },\
    {SL_FIB_START_OFFSET ,\
        " Offset for Hardware Ack errors.  "\
        },\
    {SL_FIB_SUCCESS ,\
        " The operation is successfully programmed in hardware.  "\
        },\
    {SL_FIB_FAILED ,\
        " FIB programming failure.  "\
        },\
    {SL_FIB_INELIGIBLE ,\
        " The operation is not viable to be programmed in hardware at this time.  "\
        },\
    {SL_POLICY_START_OFFSET ,\
        " Offset for policy object operations.  "\
        },\
    {SL_POLICY_ADD_ERR ,\
        " Policy object could not be created.  "\
        },\
    {SL_POLICY_EXISTS_ERR ,\
        " Policy object already exists.  "\
        },\
    {SL_POLICY_DELETE_ERR ,\
        " Policy object delete failed.  "\
        },\
    {SL_POLICY_RULE_ADD_ERR ,\
        " Rule could not be created.  "\
        },\
    {SL_POLICY_RULE_EXISTS_ERR ,\
        " Rule already exists.  "\
        },\
    {SL_POLICY_RULE_DELETE_ERR ,\
        " Rule delete error.  "\
        },\
    {SL_POLICY_APPLY_ERR ,\
        " Policy object apply error.  "\
        },\
    {SL_POLICY_UNAPPLY_ERR ,\
        " Policy object unapply error.  "\
        },\
    {SL_POLICY_TOO_MANY_POLICIES ,\
        " Operation rejected due to too many policies in the request.  "\
        },\
    {SL_POLICY_NAME_TOO_LONG ,\
        " Policy name is too long.  "\
        },\
    {SL_POLICY_RULE_NAME_TOO_LONG ,\
        " Rule name is too long.  "\
        },\
    {SL_POLICY_DUPLICATE_PRIORITY_IN_RULE ,\
        " Duplicate priority for the rule in the same policy.  "\
        },\
    {SL_POLICY_RULE_MOD_NOT_ALLOWED ,\
        " Rule modification not allowed.  "\
        },\
    {SL_POLICY_INVALID_RULE ,\
        " Rule belongs to a different policy.  "\
        },\
    {SL_POLICY_RULE_ADD_NO_RULES ,\
        " Rule add operation requested but no rules were provided.  "\
        },\
    {SL_POLICY_INVALID_MATCH_COUNT_IN_RULE ,\
        " Rule add operation requested but no matches were provided.  "\
        },\
    {SL_POLICY_INVALID_ACTION_COUNT_IN_RULE ,\
        " Rule add operation requested but no actions were provided.  "\
        },\
    {SL_POLICY_NOT_FOUND ,\
        " Policy not found. "\
        },\
    {SL_POLICY_INVALID ,\
        " Policy invalid.  "\
        },\
    {SL_POLICY_NAME_MISSING ,\
        " Policy name missing.  "\
        },\
    {SL_POLICY_RULE_NAME_MISSING ,\
        " Rule name missing.  "\
        },\
    {SL_POLICY_PRIORITY_MISSING_IN_RULE ,\
        " Priority missing in rule.  "\
        },\
    {SL_POLICY_TYPE_INVALID ,\
        " Invalid policy type.  "\
        },\
    {SL_POLICY_INVALID_DIRECTION ,\
        " Invalid policy direction.  "\
        },\
    {SL_POLICY_INTF_NAME_TOOLONG ,\
        " Policy object's interface name exceeds supported length.  "\
        },\
    {SL_POLICY_INTF_NAME_MISSING ,\
        " Policy object's interface name is missing.  "\
        },\
    {SL_POLICY_MAX_RULE_LIMIT_REACHED ,\
        " Max rule limit within a policy is reached.  "\
        },\
    {SL_POLICY_VRF_NAME_TOO_LONG ,\
        " Vrf name in policy object is too long.  "\
        },\
    {SL_POLICY_VRF_NAME_MISSING ,\
        " Vrf name missing in policy object.  "\
        },\
    {SL_POLICY_PATH_GRP_NAME_TOO_LONG ,\
        " Path Group name in policy object too long.  "\
        },\
    {SL_POLICY_PATH_GRP_NAME_MISSING ,\
        " Path Group name missing in policy object.  "\
        },\
    {SL_POLICY_INVALID_DSCP_VALUE ,\
        " Invalid Dscp Value.  "\
        },\
    {SL_POLICY_PRIORITY_STR_TOO_LONG ,\
        " Priority string too long.  "\
        },\
    {SL_POLICY_MAX_INTF_LIMIT_REACHED ,\
        " Max interfaces limit in policy reached.  "\
        },\
    {SL_POLICY_RULE_DELETE_NO_RULES ,\
        " Rule delete operation requested but no rules were provided.  "\
        },\
    {SL_POLICY_APPLY_NO_INTFS ,\
        " Policy apply requested but no interfaces were provided.  "\
        },\
    {SL_POLICY_UNAPPLY_NO_INTFS ,\
        " Policy unapply requested but no interfaces were provided.  "\
        },\
    {SL_INTERNAL_START_OFFSET ,\
        " Offset for Internal errors.  "\
        },\
 \
    /*End of Generated Error strings*/

#endif

