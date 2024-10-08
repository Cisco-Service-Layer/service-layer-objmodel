# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_bgpls_topology.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17sl_bgpls_topology.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\"L\n\x16SLBgplsTopoNotifReqMsg\x12\x32\n\x05Match\x18\x01 \x03(\x0b\x32#.service_layer.SLBgplsTopoNlriMatch\"\xbc\x01\n\x14SLBgplsTopoNlriMatch\x12\x38\n\nInstanceId\x18\x01 \x01(\x0b\x32$.service_layer.SLBgplsTopoInstanceId\x12\x34\n\x08Protocol\x18\x02 \x01(\x0e\x32\".service_layer.SLBgplsTopoProtocol\x12\x34\n\x08NlriType\x18\x03 \x01(\x0e\x32\".service_layer.SLBgplsTopoNlriType\"\xee\x01\n\x13SLBgplsTopoNotifMsg\x12\x31\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatusH\x00\x12/\n\x04\x44\x61ta\x18\x02 \x01(\x0b\x32\x1f.service_layer.SLBgplsTopoNotifH\x00\x12\x36\n\x05Start\x18\x03 \x01(\x0b\x32%.service_layer.SLBgplsTopoStartMarkerH\x00\x12\x32\n\x03\x45nd\x18\x04 \x01(\x0b\x32#.service_layer.SLBgplsTopoEndMarkerH\x00\x42\x07\n\x05\x45vent\"\x18\n\x16SLBgplsTopoStartMarker\"\x16\n\x14SLBgplsTopoEndMarker\"D\n\x10SLBgplsTopoNotif\x12\x30\n\x07\x45ntries\x18\x01 \x03(\x0b\x32\x1f.service_layer.SLBgplsTopoEntry\"x\n\x10SLBgplsTopoEntry\x12\x36\n\tOperation\x18\x01 \x01(\x0e\x32#.service_layer.SLBgplsTopoOperation\x12,\n\x04\x44\x61ta\x18\x02 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoData\"\xa9\x02\n\x0fSLBgplsTopoData\x12\x38\n\nInstanceId\x18\x01 \x01(\x0b\x32$.service_layer.SLBgplsTopoInstanceId\x12\x34\n\x08Protocol\x18\x02 \x01(\x0e\x32\".service_layer.SLBgplsTopoProtocol\x12\x32\n\x04Node\x18\x03 \x01(\x0b\x32\".service_layer.SLBgplsTopoNodeDataH\x00\x12\x32\n\x04Link\x18\x04 \x01(\x0b\x32\".service_layer.SLBgplsTopoLinkDataH\x00\x12\x36\n\x06Prefix\x18\x05 \x01(\x0b\x32$.service_layer.SLBgplsTopoPrefixDataH\x00\x42\x06\n\x04\x44\x61ta\"+\n\x15SLBgplsTopoInstanceId\x12\x12\n\nIdentifier\x18\x01 \x01(\x04\"y\n\x13SLBgplsTopoNodeData\x12,\n\x04Node\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoNode\x12\x34\n\x08NodeAttr\x18\x02 \x01(\x0b\x32\".service_layer.SLBgplsTopoNodeAttr\"y\n\x13SLBgplsTopoLinkData\x12,\n\x04Link\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoLink\x12\x34\n\x08LinkAttr\x18\x02 \x01(\x0b\x32\".service_layer.SLBgplsTopoLinkAttr\"\x83\x01\n\x15SLBgplsTopoPrefixData\x12\x30\n\x06Prefix\x18\x01 \x01(\x0b\x32 .service_layer.SLBgplsTopoPrefix\x12\x38\n\nPrefixAttr\x18\x02 \x01(\x0b\x32$.service_layer.SLBgplsTopoPrefixAttr\"\x9a\x02\n\x0fSLBgplsTopoNode\x12\x0b\n\x03\x41sn\x18\x01 \x01(\r\x12:\n\nOspfNodeId\x18\x02 \x01(\x0b\x32$.service_layer.SLBgplsTopoOspfNodeIdH\x00\x12>\n\x0cOspfv3NodeId\x18\x03 \x01(\x0b\x32&.service_layer.SLBgplsTopoOspfv3NodeIdH\x00\x12:\n\nIsisNodeId\x18\x04 \x01(\x0b\x32$.service_layer.SLBgplsTopoIsisNodeIdH\x00\x12\x38\n\tBgpNodeId\x18\x05 \x01(\x0b\x32#.service_layer.SLBgplsTopoBgpNodeIdH\x00\x42\x08\n\x06NodeId\"\xba\x01\n\x0fSLBgplsTopoLink\x12\x36\n\x0eLocalNodeDescr\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoNode\x12\x37\n\x0fRemoteNodeDescr\x18\x02 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoNode\x12\x36\n\tLinkDescr\x18\x03 \x01(\x0b\x32#.service_layer.SLBgplsTopoLinkDescr\"\x82\x01\n\x11SLBgplsTopoPrefix\x12\x31\n\tNodeDescr\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoNode\x12:\n\x0bPrefixDescr\x18\x02 \x01(\x0b\x32%.service_layer.SLBgplsTopoPrefixDescr\"\xb5\x01\n\x14SLBgplsTopoLinkDescr\x12\x0f\n\x07LocalId\x18\x01 \x01(\r\x12\x10\n\x08RemoteId\x18\x02 \x01(\r\x12\x11\n\tLocalIpv4\x18\x03 \x01(\x0c\x12\x12\n\nRemoteIpv4\x18\x04 \x01(\x0c\x12\x11\n\tLocalIpv6\x18\x05 \x01(\x0c\x12\x12\n\nRemoteIpv6\x18\x06 \x01(\x0c\x12,\n\x04MtId\x18\x07 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoMtId\"\xac\x01\n\x16SLBgplsTopoPrefixDescr\x12,\n\x04MtId\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLBgplsTopoMtId\x12>\n\rOspfRouteType\x18\x02 \x01(\x0e\x32\'.service_layer.SLBgplsTopoOspfRouteType\x12\x14\n\x0cPrefixLength\x18\x03 \x01(\r\x12\x0e\n\x06Prefix\x18\x04 \x01(\x0c\"c\n\x15SLBgplsTopoOspfNodeId\x12\x0e\n\x06\x41reaId\x18\x01 \x01(\r\x12\x12\n\nIsAsScoped\x18\x02 \x01(\r\x12\x10\n\x08RouterId\x18\x03 \x01(\x0c\x12\x14\n\x0c\x44rIdentifier\x18\x04 \x01(\x0c\"c\n\x17SLBgplsTopoOspfv3NodeId\x12\x0e\n\x06\x41reaId\x18\x01 \x01(\r\x12\x10\n\x08\x41sScoped\x18\x02 \x01(\r\x12\x10\n\x08RouterId\x18\x03 \x01(\x0c\x12\x14\n\x0c\x44rIdentifier\x18\x04 \x01(\r\"8\n\x15SLBgplsTopoIsisNodeId\x12\x10\n\x08SystemId\x18\x01 \x01(\x0c\x12\r\n\x05PsnId\x18\x02 \x01(\x0c\";\n\x14SLBgplsTopoBgpNodeId\x12\x10\n\x08RouterId\x18\x01 \x01(\x0c\x12\x11\n\tMemberAsn\x18\x02 \x01(\r\"\xa3\x06\n\x13SLBgplsTopoNodeAttr\x12,\n\x04MtId\x18\x01 \x03(\x0b\x32\x1e.service_layer.SLBgplsTopoMtId\x12\x32\n\x07NodeMsd\x18\x02 \x03(\x0b\x32!.service_layer.SLBgplsTopoNodeMsd\x12<\n\x0cNodeFlagBits\x18\x03 \x01(\x0b\x32&.service_layer.SLBgplsTopoNodeFlagBits\x12@\n\x0eOpaqueNodeAttr\x18\x04 \x01(\x0b\x32(.service_layer.SLBgplsTopoNodeOpaqueAttr\x12\x30\n\x08NodeName\x18\x05 \x01(\x0b\x32\x1e.service_layer.SLBgplsNodeName\x12\x38\n\nIsisAreaId\x18\x06 \x03(\x0b\x32$.service_layer.SLBgplsTopoIsisAreaId\x12>\n\tLocalIpv4\x18\x07 \x03(\x0b\x32+.service_layer.SLBgplsTopoLocalIpv4RouterId\x12>\n\tLocalIpv6\x18\x08 \x03(\x0b\x32+.service_layer.SLBgplsTopoLocalIpv6RouterId\x12>\n\rSrgbIsisFlags\x18\t \x01(\x0b\x32\'.service_layer.SLBgplsTopoSrgbIsisFlags\x12,\n\x04Srgb\x18\n \x03(\x0b\x32\x1e.service_layer.SLBgplsTopoSrgb\x12:\n\x0bSrAlgorithm\x18\x0b \x01(\x0b\x32%.service_layer.SLBgplsTopoSrAlgorithm\x12,\n\x04Srlb\x18\x0c \x03(\x0b\x32\x1e.service_layer.SLBgplsTopoSrlb\x12*\n\x03\x46\x61\x64\x18\r \x03(\x0b\x32\x1d.service_layer.SLBgplsTopoFad\x12:\n\x0bUnknownAttr\x18\x0e \x03(\x0b\x32%.service_layer.SLBgplsTopoUnknownAttr\"\xa4\x10\n\x13SLBgplsTopoLinkAttr\x12;\n\x0cLinkLocRemId\x18\x01 \x01(\x0b\x32%.service_layer.SLBplsTopoLinkLocRemId\x12\x32\n\x07LinkMsd\x18\x02 \x03(\x0b\x32!.service_layer.SLBgplsTopoLinkMsd\x12\x46\n\x11LocalIpv4RouterId\x18\x03 \x03(\x0b\x32+.service_layer.SLBgplsTopoLocalIpv4RouterId\x12\x46\n\x11LocalIpv6RouterId\x18\x04 \x03(\x0b\x32+.service_layer.SLBgplsTopoLocalIpv6RouterId\x12H\n\x12RemoteIpv4RouterId\x18\x05 \x03(\x0b\x32,.service_layer.SLBgplsTopoRemoteIpv4RouterId\x12H\n\x12RemoteIpv6RouterId\x18\x06 \x03(\x0b\x32,.service_layer.SLBgplsTopoRemoteIpv6RouterId\x12@\n\x0cMaxBandwidth\x18\x08 \x01(\x0b\x32*.service_layer.SLBgplsTopoLinkMaxBandwidth\x12H\n\x10MaxResvBandwidth\x18\t \x01(\x0b\x32..service_layer.SLBgplsTopoLinkMaxResvBandwidth\x12\x46\n\x0fUnresvBandwidth\x18\n \x03(\x0b\x32-.service_layer.SLBgplsTopoLinkUnresvBandwidth\x12\x42\n\x0bTeDefMetric\x18\x0b \x01(\x0b\x32-.service_layer.SLBgplsTopoLinkTeDefaultMetric\x12\x44\n\x0eProtectionType\x18\x0c \x01(\x0b\x32,.service_layer.SLBgplsTopoLinkProtectionType\x12\x42\n\rMplsProtoMask\x18\r \x01(\x0b\x32+.service_layer.SLBgplsTopoLinkMplsProtoMask\x12:\n\tIgpMetric\x18\x0e \x01(\x0b\x32\'.service_layer.SLBgplsTopoLinkIgpMetric\x12\x30\n\x04Srlg\x18\x0f \x01(\x0b\x32\".service_layer.SLBgplsTopoLinkSrlg\x12<\n\nOpaqueAttr\x18\x10 \x01(\x0b\x32(.service_layer.SLBgplsTopoLinkOpaqueAttr\x12\x34\n\x08LinkName\x18\x11 \x01(\x0b\x32\".service_layer.SLBgplsTopoLinkName\x12\x30\n\x06\x41\x64jSid\x18\x12 \x03(\x0b\x32 .service_layer.SLBgplsTopoAdjSid\x12\x36\n\tLanAdjSid\x18\x13 \x03(\x0b\x32#.service_layer.SLBgplsTopoLanAdjSid\x12@\n\x0e\x42gpPeerNodeSid\x18\x14 \x03(\x0b\x32(.service_layer.SLBgplsTopoBgpPeerNodeSid\x12>\n\rBgpPeerAdjSid\x18\x15 \x03(\x0b\x32\'.service_layer.SLBgplsTopoBgpPeerAdjSid\x12>\n\rBgpPeerSetSid\x18\x16 \x03(\x0b\x32\'.service_layer.SLBgplsTopoBgpPeerSetSid\x12<\n\x0cUniLinkDelay\x18\x17 \x01(\x0b\x32&.service_layer.SLBgplsTopoUniLinkDelay\x12H\n\x12MinMaxUniLinkDelay\x18\x18 \x01(\x0b\x32,.service_layer.SLBgplsTopoMinMaxUniLinkDelay\x12:\n\x0bUniDelayVar\x18\x19 \x01(\x0b\x32%.service_layer.SLBgplsTopoUniDelayVar\x12:\n\x0bUniLinkLoss\x18\x1a \x01(\x0b\x32%.service_layer.SLBgplsTopoUniLinkLoss\x12\x42\n\x0fUniResBandwidth\x18\x1b \x01(\x0b\x32).service_layer.SLBgplsTopoUniResBandwidth\x12\x46\n\x11UniAvailBandwidth\x18\x1c \x01(\x0b\x32+.service_layer.SLBgplsTopoUniAvailBandwidth\x12\x44\n\x10UniUtilBandwidth\x18\x1d \x01(\x0b\x32*.service_layer.SLBgplsTopoUniUtilBandwidth\x12\x30\n\x04\x41sla\x18\x1e \x03(\x0b\x32\".service_layer.SLBgplsTopoAslaAttr\x12H\n\x12L2BundleMemberAttr\x18\x1f \x03(\x0b\x32,.service_layer.SLBgplsTopoL2BundleMemberAttr\x12>\n\rExtAdminGroup\x18  \x01(\x0b\x32\'.service_layer.SLBgplsTopoExtAdminGroup\x12:\n\x0bUnknownAttr\x18! \x03(\x0b\x32%.service_layer.SLBgplsTopoUnknownAttr\"\xef\x05\n\x15SLBgplsTopoPrefixAttr\x12\x32\n\x04\x46\x61pm\x18\x01 \x03(\x0b\x32$.service_layer.SLBgplsTopoPrefixFAPM\x12:\n\x08IgpFlags\x18\x02 \x01(\x0b\x32(.service_layer.SLBgplsTopoPrefixIgpFlags\x12@\n\x0bIgpRouteTag\x18\x03 \x03(\x0b\x32+.service_layer.SLBgplsTopoPrefixIgpRouteTag\x12\x46\n\x0eIgpExtRouteTag\x18\x04 \x03(\x0b\x32..service_layer.SLBgplsTopoPrefixIgpExtRouteTag\x12\x36\n\x06Metric\x18\x05 \x01(\x0b\x32&.service_layer.SLBgplsTopoPrefixMetric\x12@\n\x0bOspfFwdAddr\x18\x06 \x01(\x0b\x32+.service_layer.SLBgplsTopoPrefixOspfFwdAddr\x12>\n\nOpaqueAttr\x18\x07 \x01(\x0b\x32*.service_layer.SLBgplsTopoPrefixOpaqueAttr\x12\x30\n\x03Sid\x18\x08 \x03(\x0b\x32#.service_layer.SLBgplsTopoPrefixSid\x12\x34\n\x05Range\x18\t \x01(\x0b\x32%.service_layer.SLBgplsTopoPrefixRange\x12<\n\tAttrFlags\x18\n \x01(\x0b\x32).service_layer.SLBgplsTopoPrefixAttrFlags\x12@\n\x0bSrcRouterId\x18\x0b \x01(\x0b\x32+.service_layer.SLBgplsTopoPrefixSrcRouterId\x12:\n\x0bUnknownAttr\x18\x0c \x03(\x0b\x32%.service_layer.SLBgplsTopoUnknownAttr\";\n\x16SLBplsTopoLinkLocRemId\x12\x0f\n\x07LocalId\x18\x01 \x01(\r\x12\x10\n\x08RemoteId\x18\x02 \x01(\r\"\x1f\n\x0fSLBgplsTopoMtId\x12\x0c\n\x04MtId\x18\x01 \x01(\r\"1\n\x12SLBgplsTopoNodeMsd\x12\x0c\n\x04Type\x18\x01 \x01(\r\x12\r\n\x05Value\x18\x02 \x01(\r\"1\n\x12SLBgplsTopoLinkMsd\x12\x0c\n\x04Type\x18\x01 \x01(\r\x12\r\n\x05Value\x18\x02 \x01(\r\"(\n\x17SLBgplsTopoNodeFlagBits\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\"/\n\x19SLBgplsTopoNodeOpaqueAttr\x12\x12\n\nOpaqueAttr\x18\x01 \x01(\x0c\"\x1f\n\x0fSLBgplsNodeName\x12\x0c\n\x04Name\x18\x01 \x01(\t\"\'\n\x15SLBgplsTopoIsisAreaId\x12\x0e\n\x06\x41reaId\x18\x01 \x01(\x0c\"0\n\x1cSLBgplsTopoLocalIpv4RouterId\x12\x10\n\x08RouterId\x18\x01 \x01(\x0c\"0\n\x1cSLBgplsTopoLocalIpv6RouterId\x12\x10\n\x08RouterId\x18\x01 \x01(\x0c\"1\n\x1dSLBgplsTopoRemoteIpv4RouterId\x12\x10\n\x08RouterId\x18\x01 \x01(\x0c\"1\n\x1dSLBgplsTopoRemoteIpv6RouterId\x12\x10\n\x08RouterId\x18\x01 \x01(\x0c\"8\n\x0fSLBgplsTopoSrgb\x12\x12\n\nStartLabel\x18\x01 \x01(\r\x12\x11\n\tRangeSize\x18\x02 \x01(\r\")\n\x18SLBgplsTopoSrgbIsisFlags\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\",\n\x16SLBgplsTopoSrAlgorithm\x12\x12\n\nAlgorithms\x18\x01 \x01(\x0c\"8\n\x0fSLBgplsTopoSrlb\x12\x12\n\nStartLabel\x18\x01 \x01(\r\x12\x11\n\tRangeSize\x18\x02 \x01(\r\"\x82\x03\n\x0eSLBgplsTopoFad\x12\x11\n\tAlgorithm\x18\x01 \x01(\x0c\x12\x12\n\nMetricType\x18\x02 \x01(\x0c\x12\x10\n\x08\x43\x61lcType\x18\x03 \x01(\x0c\x12\x10\n\x08Priority\x18\x04 \x01(\x0c\x12\x11\n\tExcAnyAff\x18\x05 \x03(\r\x12\x11\n\tIncAnyAff\x18\x06 \x03(\r\x12\x11\n\tIncAllAff\x18\x07 \x03(\r\x12\r\n\x05\x46lags\x18\x08 \x01(\x0c\x12\x0f\n\x07\x45xcSrlg\x18\t \x03(\r\x12\x39\n\tUnsuppTlv\x18\x0f \x01(\x0b\x32&.service_layer.SLBgplsTopoFadUnsuppTlv\x12\x10\n\x08\x45xcMinBw\x18\x0e \x01(\x0c\x12=\n\x0b\x45xcMaxDelay\x18\r \x01(\x0b\x32(.service_layer.SLBgplsTopoFadExcMaxDelay\x12\x14\n\x0c\x45xcAnyRevAff\x18\n \x03(\r\x12\x14\n\x0cIncAnyRevAff\x18\x0b \x03(\r\x12\x14\n\x0cIncAllRevAff\x18\x0c \x03(\r\"H\n\x15SLBgplsTopoPrefixFAPM\x12\x10\n\x08\x46lexAlgo\x18\x01 \x01(\r\x12\r\n\x05\x46lags\x18\x02 \x01(\x0c\x12\x0e\n\x06Metric\x18\x03 \x01(\r\"^\n\x17SLBgplsTopoFadUnsuppTlv\x12\x34\n\x08Protocol\x18\x01 \x01(\x0e\x32\".service_layer.SLBgplsTopoProtocol\x12\r\n\x05Types\x18\x02 \x01(\x0c\"*\n\x19SLBgplsTopoFadExcMaxDelay\x12\r\n\x05\x44\x65lay\x18\x01 \x01(\r\"0\n\x1bSLBgplsTopoLinkMaxBandwidth\x12\x11\n\tBandwidth\x18\x01 \x01(\x0c\"4\n\x1fSLBgplsTopoLinkMaxResvBandwidth\x12\x11\n\tBandwidth\x18\x01 \x01(\x0c\"E\n\x1eSLBgplsTopoLinkUnresvBandwidth\x12\x10\n\x08Priority\x18\x01 \x01(\r\x12\x11\n\tBandwidth\x18\x02 \x01(\x0c\"0\n\x1eSLBgplsTopoLinkTeDefaultMetric\x12\x0e\n\x06Metric\x18\x01 \x01(\r\"-\n\x1dSLBgplsTopoLinkProtectionType\x12\x0c\n\x04Mask\x18\x01 \x01(\r\",\n\x1cSLBgplsTopoLinkMplsProtoMask\x12\x0c\n\x04Mask\x18\x01 \x01(\x0c\"*\n\x18SLBgplsTopoLinkIgpMetric\x12\x0e\n\x06Metric\x18\x01 \x01(\x0c\"&\n\x13SLBgplsTopoLinkSrlg\x12\x0f\n\x07SrlgVal\x18\x01 \x03(\r\"/\n\x19SLBgplsTopoLinkOpaqueAttr\x12\x12\n\nOpaqueAttr\x18\x01 \x01(\x0c\"#\n\x13SLBgplsTopoLinkName\x12\x0c\n\x04Name\x18\x01 \x01(\t\"\x81\x01\n\x11SLBgplsTopoAdjSid\x12\x12\n\nLabelIndex\x18\x01 \x01(\r\x12\x39\n\x0c\x41\x64jSidFormat\x18\x02 \x01(\x0e\x32#.service_layer.SLBgplsTopoSidFormat\x12\r\n\x05\x46lags\x18\x03 \x01(\x0c\x12\x0e\n\x06Weight\x18\x04 \x01(\r\"\xbc\x01\n\x14SLBgplsTopoLanAdjSid\x12\x36\n\x08Neighbor\x18\x01 \x01(\x0b\x32$.service_layer.SLBgpLsTopoNeighborId\x12\x12\n\nLabelIndex\x18\x02 \x01(\r\x12\x39\n\x0c\x41\x64jSidFormat\x18\x03 \x01(\x0e\x32#.service_layer.SLBgplsTopoSidFormat\x12\r\n\x05\x46lags\x18\x04 \x01(\x0c\x12\x0e\n\x06Weight\x18\x05 \x01(\r\"\x82\x01\n\x19SLBgplsTopoBgpPeerNodeSid\x12\x0b\n\x03Sid\x18\x01 \x01(\x0c\x12\x39\n\x0c\x42gpSidFormat\x18\x02 \x01(\x0e\x32#.service_layer.SLBgplsTopoSidFormat\x12\r\n\x05\x46lags\x18\x03 \x01(\x0c\x12\x0e\n\x06Weight\x18\x04 \x01(\r\"\x81\x01\n\x18SLBgplsTopoBgpPeerAdjSid\x12\x0b\n\x03Sid\x18\x01 \x01(\x0c\x12\x39\n\x0c\x42gpSidFormat\x18\x02 \x01(\x0e\x32#.service_layer.SLBgplsTopoSidFormat\x12\r\n\x05\x46lags\x18\x03 \x01(\x0c\x12\x0e\n\x06Weight\x18\x04 \x01(\r\"\x81\x01\n\x18SLBgplsTopoBgpPeerSetSid\x12\x0b\n\x03Sid\x18\x01 \x01(\x0c\x12\x39\n\x0c\x42gpSidFormat\x18\x02 \x01(\x0e\x32#.service_layer.SLBgplsTopoSidFormat\x12\r\n\x05\x46lags\x18\x03 \x01(\x0c\x12\x0e\n\x06Weight\x18\x04 \x01(\r\"M\n\x15SLBgpLsTopoNeighborId\x12\x12\n\x08Ipv4Addr\x18\x01 \x01(\x0cH\x00\x12\x12\n\x08SystemId\x18\x02 \x01(\x0cH\x00\x42\x0c\n\nNeighborId\"7\n\x17SLBgplsTopoUniLinkDelay\x12\r\n\x05\x44\x65lay\x18\x01 \x01(\r\x12\r\n\x05\x46lags\x18\x02 \x01(\x0c\"H\n\x1dSLBgplsTopoMinMaxUniLinkDelay\x12\x0b\n\x03Min\x18\x01 \x01(\r\x12\x0b\n\x03Max\x18\x02 \x01(\r\x12\r\n\x05\x46lags\x18\x03 \x01(\x0c\":\n\x16SLBgplsTopoUniDelayVar\x12\x11\n\tVariation\x18\x01 \x01(\r\x12\r\n\x05\x46lags\x18\x02 \x01(\x0c\"5\n\x16SLBgplsTopoUniLinkLoss\x12\x0c\n\x04Loss\x18\x01 \x01(\r\x12\r\n\x05\x46lags\x18\x02 \x01(\x0c\"/\n\x1aSLBgplsTopoUniResBandwidth\x12\x11\n\tBandwidth\x18\x01 \x01(\x0c\"1\n\x1cSLBgplsTopoUniAvailBandwidth\x12\x11\n\tBandwidth\x18\x01 \x01(\x0c\"0\n\x1bSLBgplsTopoUniUtilBandwidth\x12\x11\n\tBandwidth\x18\x01 \x01(\x0c\"\xf9\x05\n\x13SLBgplsTopoAslaAttr\x12\x0c\n\x04Sabm\x18\x01 \x01(\x0c\x12\r\n\x05Udabm\x18\x02 \x01(\x0c\x12\x42\n\x0bTeDefMetric\x18\x04 \x01(\x0b\x32-.service_layer.SLBgplsTopoLinkTeDefaultMetric\x12\x30\n\x04Srlg\x18\x05 \x01(\x0b\x32\".service_layer.SLBgplsTopoLinkSrlg\x12<\n\x0cUniLinkDelay\x18\x06 \x01(\x0b\x32&.service_layer.SLBgplsTopoUniLinkDelay\x12\x45\n\x0fMinMaxLinkDelay\x18\x07 \x01(\x0b\x32,.service_layer.SLBgplsTopoMinMaxUniLinkDelay\x12@\n\x11UniDelayVariation\x18\x08 \x01(\x0b\x32%.service_layer.SLBgplsTopoUniDelayVar\x12:\n\x0bUniLinkLoss\x18\t \x01(\x0b\x32%.service_layer.SLBgplsTopoUniLinkLoss\x12\x42\n\x0fUniResBandwidth\x18\n \x01(\x0b\x32).service_layer.SLBgplsTopoUniResBandwidth\x12\x46\n\x11UniAvailBandwidth\x18\x0b \x01(\x0b\x32+.service_layer.SLBgplsTopoUniAvailBandwidth\x12\x44\n\x10UniUtilBandwidth\x18\x0c \x01(\x0b\x32*.service_layer.SLBgplsTopoUniUtilBandwidth\x12>\n\rExtAdminGroup\x18\r \x01(\x0b\x32\'.service_layer.SLBgplsTopoExtAdminGroup\x12:\n\x0bUnknownAttr\x18\x0e \x03(\x0b\x32%.service_layer.SLBgplsTopoUnknownAttr\"*\n\x19SLBgplsTopoPrefixIgpFlags\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\"+\n\x1cSLBgplsTopoPrefixIgpRouteTag\x12\x0b\n\x03Tag\x18\x01 \x01(\r\".\n\x1fSLBgplsTopoPrefixIgpExtRouteTag\x12\x0b\n\x03Tag\x18\x01 \x01(\x04\")\n\x17SLBgplsTopoPrefixMetric\x12\x0e\n\x06Metric\x18\x01 \x01(\r\"U\n\x1cSLBgplsTopoPrefixOspfFwdAddr\x12\x12\n\x08Ipv4Addr\x18\x01 \x01(\x0cH\x00\x12\x12\n\x08Ipv6Addr\x18\x02 \x01(\x0cH\x00\x42\r\n\x0bOspfFwdAddr\"1\n\x1bSLBgplsTopoPrefixOpaqueAttr\x12\x12\n\nOpaqueAttr\x18\x01 \x01(\x0c\"\x90\x01\n\x14SLBgplsTopoPrefixSid\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\x12\x11\n\tAlgorithm\x18\x02 \x01(\r\x12\x12\n\nLabelIndex\x18\x03 \x01(\r\x12\x42\n\x0fPrefixSidFormat\x18\x04 \x01(\x0e\x32).service_layer.SLBgplsTopoPrefixSidFormat\"n\n\x16SLBgplsTopoPrefixRange\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\x12\x11\n\tRangeSize\x18\x02 \x01(\r\x12\x11\n\tAlgorithm\x18\x03 \x01(\r\x12\r\n\x05Index\x18\x04 \x01(\r\x12\x10\n\x08SidFlags\x18\x05 \x01(\x0c\"+\n\x1aSLBgplsTopoPrefixAttrFlags\x12\r\n\x05\x46lags\x18\x01 \x01(\x0c\"U\n\x1cSLBgplsTopoPrefixSrcRouterId\x12\x12\n\x08Ipv4Addr\x18\x01 \x01(\x0cH\x00\x12\x12\n\x08Ipv6Addr\x18\x02 \x01(\x0cH\x00\x42\r\n\x0bSrcRouterId\"\xfe\x08\n\x1dSLBgplsTopoL2BundleMemberAttr\x12\x12\n\nMemberDesc\x18\x01 \x01(\r\x12@\n\x0cMaxBandwidth\x18\x03 \x01(\x0b\x32*.service_layer.SLBgplsTopoLinkMaxBandwidth\x12H\n\x10MaxResvBandwidth\x18\x04 \x01(\x0b\x32..service_layer.SLBgplsTopoLinkMaxResvBandwidth\x12\x46\n\x0fUnresvBandwidth\x18\x05 \x03(\x0b\x32-.service_layer.SLBgplsTopoLinkUnresvBandwidth\x12\x42\n\x0bTeDefMetric\x18\x06 \x01(\x0b\x32-.service_layer.SLBgplsTopoLinkTeDefaultMetric\x12\x44\n\x0eProtectionType\x18\x07 \x01(\x0b\x32,.service_layer.SLBgplsTopoLinkProtectionType\x12\x30\n\x06\x41\x64jSid\x18\x08 \x03(\x0b\x32 .service_layer.SLBgplsTopoAdjSid\x12\x36\n\tLanAdjSid\x18\t \x03(\x0b\x32#.service_layer.SLBgplsTopoLanAdjSid\x12<\n\x0cUniLinkDelay\x18\n \x01(\x0b\x32&.service_layer.SLBgplsTopoUniLinkDelay\x12\x45\n\x0fMinMaxLinkDelay\x18\x0b \x01(\x0b\x32,.service_layer.SLBgplsTopoMinMaxUniLinkDelay\x12@\n\x11UniDelayVariation\x18\x0c \x01(\x0b\x32%.service_layer.SLBgplsTopoUniDelayVar\x12:\n\x0bUniLinkLoss\x18\r \x01(\x0b\x32%.service_layer.SLBgplsTopoUniLinkLoss\x12\x42\n\x0fUniResBandwidth\x18\x0e \x01(\x0b\x32).service_layer.SLBgplsTopoUniResBandwidth\x12\x46\n\x11UniAvailBandwidth\x18\x0f \x01(\x0b\x32+.service_layer.SLBgplsTopoUniAvailBandwidth\x12\x44\n\x10UniUtilBandwidth\x18\x10 \x01(\x0b\x32*.service_layer.SLBgplsTopoUniUtilBandwidth\x12\x30\n\x04\x41sla\x18\x11 \x03(\x0b\x32\".service_layer.SLBgplsTopoAslaAttr\x12>\n\rExtAdminGroup\x18\x12 \x01(\x0b\x32\'.service_layer.SLBgplsTopoExtAdminGroup\x12:\n\x0bUnknownAttr\x18\x13 \x03(\x0b\x32%.service_layer.SLBgplsTopoUnknownAttr\")\n\x18SLBgplsTopoExtAdminGroup\x12\r\n\x05Group\x18\x01 \x03(\r\"I\n\x16SLBgplsTopoUnknownAttr\x12\x0f\n\x07TlvType\x18\x01 \x01(\r\x12\x0e\n\x06TlvLen\x18\x02 \x01(\r\x12\x0e\n\x06RawTlv\x18\x03 \x01(\x0c*\x84\x01\n\x14SLBgplsTopoOperation\x12$\n SL_BGPLS_TOPO_OPERATION_RESERVED\x10\x00\x12\"\n\x1eSL_BGPLS_TOPO_OPERATION_UPDATE\x10\x01\x12\"\n\x1eSL_BGPLS_TOPO_OPERATION_DELETE\x10\x02*\xd1\x01\n\x13SLBgplsTopoNlriType\x12$\n SL_BGPLS_TOPO_NLRI_TYPE_RESERVED\x10\x00\x12 \n\x1cSL_BGPLS_TOPO_NLRI_TYPE_NODE\x10\x01\x12 \n\x1cSL_BGPLS_TOPO_NLRI_TYPE_LINK\x10\x02\x12\'\n#SL_BGPLS_TOPO_NLRI_TYPE_IPV4_PREFIX\x10\x03\x12\'\n#SL_BGPLS_TOPO_NLRI_TYPE_IPV6_PREFIX\x10\x04*\xf1\x02\n\x13SLBgplsTopoProtocol\x12#\n\x1fSL_BGPLS_TOPO_PROTOCOL_RESERVED\x10\x00\x12\"\n\x1eSL_BGPLS_TOPO_PROTOCOL_ISIS_L1\x10\x01\x12\"\n\x1eSL_BGPLS_TOPO_PROTOCOL_ISIS_L2\x10\x02\x12!\n\x1dSL_BGPLS_TOPO_PROTOCOL_OSPFv2\x10\x03\x12!\n\x1dSL_BGPLS_TOPO_PROTOCOL_DIRECT\x10\x04\x12!\n\x1dSL_BGPLS_TOPO_PROTOCOL_STATIC\x10\x05\x12!\n\x1dSL_BGPLS_TOPO_PROTOCOL_OSPFv3\x10\x06\x12\x1e\n\x1aSL_BGPLS_TOPO_PROTOCOL_BGP\x10\x07\x12\"\n\x1eSL_BGPLS_TOPO_PROTOCOL_RSVP_TE\x10\x08\x12\x1d\n\x19SL_BGPLS_TOPO_PROTOCOL_SR\x10\t*\xce\x02\n\x18SLBgplsTopoOspfRouteType\x12*\n&SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_RESERVED\x10\x00\x12,\n(SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_INTRA_AREA\x10\x01\x12,\n(SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_INTER_AREA\x10\x02\x12*\n&SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_EXTERN_1\x10\x03\x12*\n&SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_EXTERN_2\x10\x04\x12(\n$SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_NSSA_1\x10\x05\x12(\n$SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_NSSA_2\x10\x06*\xab\x01\n\x14SLBgplsTopoSidFormat\x12%\n!SL_BGPLS_TOPO_SID_FORMAT_RESERVED\x10\x00\x12\"\n\x1eSL_BGPLS_TOPO_SID_FORMAT_LABEL\x10\x01\x12\"\n\x1eSL_BGPLS_TOPO_SID_FORMAT_INDEX\x10\x02\x12$\n SL_BGPLS_TOPO_SID_FORMAT_V6_ADDR\x10\x03*\xa0\x01\n\x1aSLBgplsTopoPrefixSidFormat\x12,\n(SL_BGPLS_TOPO_PREFIX_SID_FORMAT_RESERVED\x10\x00\x12)\n%SL_BGPLS_TOPO_PREFIX_SID_FORMAT_LABEL\x10\x01\x12)\n%SL_BGPLS_TOPO_PREFIX_SID_FORMAT_INDEX\x10\x02\x32t\n\x0bSLBgplsTopo\x12\x65\n\x16SLBgplsTopoNotifStream\x12%.service_layer.SLBgplsTopoNotifReqMsg\x1a\".service_layer.SLBgplsTopoNotifMsg0\x01\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_bgpls_topology_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLBGPLSTOPOOPERATION']._serialized_start=12275
  _globals['_SLBGPLSTOPOOPERATION']._serialized_end=12407
  _globals['_SLBGPLSTOPONLRITYPE']._serialized_start=12410
  _globals['_SLBGPLSTOPONLRITYPE']._serialized_end=12619
  _globals['_SLBGPLSTOPOPROTOCOL']._serialized_start=12622
  _globals['_SLBGPLSTOPOPROTOCOL']._serialized_end=12991
  _globals['_SLBGPLSTOPOOSPFROUTETYPE']._serialized_start=12994
  _globals['_SLBGPLSTOPOOSPFROUTETYPE']._serialized_end=13328
  _globals['_SLBGPLSTOPOSIDFORMAT']._serialized_start=13331
  _globals['_SLBGPLSTOPOSIDFORMAT']._serialized_end=13502
  _globals['_SLBGPLSTOPOPREFIXSIDFORMAT']._serialized_start=13505
  _globals['_SLBGPLSTOPOPREFIXSIDFORMAT']._serialized_end=13665
  _globals['_SLBGPLSTOPONOTIFREQMSG']._serialized_start=65
  _globals['_SLBGPLSTOPONOTIFREQMSG']._serialized_end=141
  _globals['_SLBGPLSTOPONLRIMATCH']._serialized_start=144
  _globals['_SLBGPLSTOPONLRIMATCH']._serialized_end=332
  _globals['_SLBGPLSTOPONOTIFMSG']._serialized_start=335
  _globals['_SLBGPLSTOPONOTIFMSG']._serialized_end=573
  _globals['_SLBGPLSTOPOSTARTMARKER']._serialized_start=575
  _globals['_SLBGPLSTOPOSTARTMARKER']._serialized_end=599
  _globals['_SLBGPLSTOPOENDMARKER']._serialized_start=601
  _globals['_SLBGPLSTOPOENDMARKER']._serialized_end=623
  _globals['_SLBGPLSTOPONOTIF']._serialized_start=625
  _globals['_SLBGPLSTOPONOTIF']._serialized_end=693
  _globals['_SLBGPLSTOPOENTRY']._serialized_start=695
  _globals['_SLBGPLSTOPOENTRY']._serialized_end=815
  _globals['_SLBGPLSTOPODATA']._serialized_start=818
  _globals['_SLBGPLSTOPODATA']._serialized_end=1115
  _globals['_SLBGPLSTOPOINSTANCEID']._serialized_start=1117
  _globals['_SLBGPLSTOPOINSTANCEID']._serialized_end=1160
  _globals['_SLBGPLSTOPONODEDATA']._serialized_start=1162
  _globals['_SLBGPLSTOPONODEDATA']._serialized_end=1283
  _globals['_SLBGPLSTOPOLINKDATA']._serialized_start=1285
  _globals['_SLBGPLSTOPOLINKDATA']._serialized_end=1406
  _globals['_SLBGPLSTOPOPREFIXDATA']._serialized_start=1409
  _globals['_SLBGPLSTOPOPREFIXDATA']._serialized_end=1540
  _globals['_SLBGPLSTOPONODE']._serialized_start=1543
  _globals['_SLBGPLSTOPONODE']._serialized_end=1825
  _globals['_SLBGPLSTOPOLINK']._serialized_start=1828
  _globals['_SLBGPLSTOPOLINK']._serialized_end=2014
  _globals['_SLBGPLSTOPOPREFIX']._serialized_start=2017
  _globals['_SLBGPLSTOPOPREFIX']._serialized_end=2147
  _globals['_SLBGPLSTOPOLINKDESCR']._serialized_start=2150
  _globals['_SLBGPLSTOPOLINKDESCR']._serialized_end=2331
  _globals['_SLBGPLSTOPOPREFIXDESCR']._serialized_start=2334
  _globals['_SLBGPLSTOPOPREFIXDESCR']._serialized_end=2506
  _globals['_SLBGPLSTOPOOSPFNODEID']._serialized_start=2508
  _globals['_SLBGPLSTOPOOSPFNODEID']._serialized_end=2607
  _globals['_SLBGPLSTOPOOSPFV3NODEID']._serialized_start=2609
  _globals['_SLBGPLSTOPOOSPFV3NODEID']._serialized_end=2708
  _globals['_SLBGPLSTOPOISISNODEID']._serialized_start=2710
  _globals['_SLBGPLSTOPOISISNODEID']._serialized_end=2766
  _globals['_SLBGPLSTOPOBGPNODEID']._serialized_start=2768
  _globals['_SLBGPLSTOPOBGPNODEID']._serialized_end=2827
  _globals['_SLBGPLSTOPONODEATTR']._serialized_start=2830
  _globals['_SLBGPLSTOPONODEATTR']._serialized_end=3633
  _globals['_SLBGPLSTOPOLINKATTR']._serialized_start=3636
  _globals['_SLBGPLSTOPOLINKATTR']._serialized_end=5720
  _globals['_SLBGPLSTOPOPREFIXATTR']._serialized_start=5723
  _globals['_SLBGPLSTOPOPREFIXATTR']._serialized_end=6474
  _globals['_SLBPLSTOPOLINKLOCREMID']._serialized_start=6476
  _globals['_SLBPLSTOPOLINKLOCREMID']._serialized_end=6535
  _globals['_SLBGPLSTOPOMTID']._serialized_start=6537
  _globals['_SLBGPLSTOPOMTID']._serialized_end=6568
  _globals['_SLBGPLSTOPONODEMSD']._serialized_start=6570
  _globals['_SLBGPLSTOPONODEMSD']._serialized_end=6619
  _globals['_SLBGPLSTOPOLINKMSD']._serialized_start=6621
  _globals['_SLBGPLSTOPOLINKMSD']._serialized_end=6670
  _globals['_SLBGPLSTOPONODEFLAGBITS']._serialized_start=6672
  _globals['_SLBGPLSTOPONODEFLAGBITS']._serialized_end=6712
  _globals['_SLBGPLSTOPONODEOPAQUEATTR']._serialized_start=6714
  _globals['_SLBGPLSTOPONODEOPAQUEATTR']._serialized_end=6761
  _globals['_SLBGPLSNODENAME']._serialized_start=6763
  _globals['_SLBGPLSNODENAME']._serialized_end=6794
  _globals['_SLBGPLSTOPOISISAREAID']._serialized_start=6796
  _globals['_SLBGPLSTOPOISISAREAID']._serialized_end=6835
  _globals['_SLBGPLSTOPOLOCALIPV4ROUTERID']._serialized_start=6837
  _globals['_SLBGPLSTOPOLOCALIPV4ROUTERID']._serialized_end=6885
  _globals['_SLBGPLSTOPOLOCALIPV6ROUTERID']._serialized_start=6887
  _globals['_SLBGPLSTOPOLOCALIPV6ROUTERID']._serialized_end=6935
  _globals['_SLBGPLSTOPOREMOTEIPV4ROUTERID']._serialized_start=6937
  _globals['_SLBGPLSTOPOREMOTEIPV4ROUTERID']._serialized_end=6986
  _globals['_SLBGPLSTOPOREMOTEIPV6ROUTERID']._serialized_start=6988
  _globals['_SLBGPLSTOPOREMOTEIPV6ROUTERID']._serialized_end=7037
  _globals['_SLBGPLSTOPOSRGB']._serialized_start=7039
  _globals['_SLBGPLSTOPOSRGB']._serialized_end=7095
  _globals['_SLBGPLSTOPOSRGBISISFLAGS']._serialized_start=7097
  _globals['_SLBGPLSTOPOSRGBISISFLAGS']._serialized_end=7138
  _globals['_SLBGPLSTOPOSRALGORITHM']._serialized_start=7140
  _globals['_SLBGPLSTOPOSRALGORITHM']._serialized_end=7184
  _globals['_SLBGPLSTOPOSRLB']._serialized_start=7186
  _globals['_SLBGPLSTOPOSRLB']._serialized_end=7242
  _globals['_SLBGPLSTOPOFAD']._serialized_start=7245
  _globals['_SLBGPLSTOPOFAD']._serialized_end=7631
  _globals['_SLBGPLSTOPOPREFIXFAPM']._serialized_start=7633
  _globals['_SLBGPLSTOPOPREFIXFAPM']._serialized_end=7705
  _globals['_SLBGPLSTOPOFADUNSUPPTLV']._serialized_start=7707
  _globals['_SLBGPLSTOPOFADUNSUPPTLV']._serialized_end=7801
  _globals['_SLBGPLSTOPOFADEXCMAXDELAY']._serialized_start=7803
  _globals['_SLBGPLSTOPOFADEXCMAXDELAY']._serialized_end=7845
  _globals['_SLBGPLSTOPOLINKMAXBANDWIDTH']._serialized_start=7847
  _globals['_SLBGPLSTOPOLINKMAXBANDWIDTH']._serialized_end=7895
  _globals['_SLBGPLSTOPOLINKMAXRESVBANDWIDTH']._serialized_start=7897
  _globals['_SLBGPLSTOPOLINKMAXRESVBANDWIDTH']._serialized_end=7949
  _globals['_SLBGPLSTOPOLINKUNRESVBANDWIDTH']._serialized_start=7951
  _globals['_SLBGPLSTOPOLINKUNRESVBANDWIDTH']._serialized_end=8020
  _globals['_SLBGPLSTOPOLINKTEDEFAULTMETRIC']._serialized_start=8022
  _globals['_SLBGPLSTOPOLINKTEDEFAULTMETRIC']._serialized_end=8070
  _globals['_SLBGPLSTOPOLINKPROTECTIONTYPE']._serialized_start=8072
  _globals['_SLBGPLSTOPOLINKPROTECTIONTYPE']._serialized_end=8117
  _globals['_SLBGPLSTOPOLINKMPLSPROTOMASK']._serialized_start=8119
  _globals['_SLBGPLSTOPOLINKMPLSPROTOMASK']._serialized_end=8163
  _globals['_SLBGPLSTOPOLINKIGPMETRIC']._serialized_start=8165
  _globals['_SLBGPLSTOPOLINKIGPMETRIC']._serialized_end=8207
  _globals['_SLBGPLSTOPOLINKSRLG']._serialized_start=8209
  _globals['_SLBGPLSTOPOLINKSRLG']._serialized_end=8247
  _globals['_SLBGPLSTOPOLINKOPAQUEATTR']._serialized_start=8249
  _globals['_SLBGPLSTOPOLINKOPAQUEATTR']._serialized_end=8296
  _globals['_SLBGPLSTOPOLINKNAME']._serialized_start=8298
  _globals['_SLBGPLSTOPOLINKNAME']._serialized_end=8333
  _globals['_SLBGPLSTOPOADJSID']._serialized_start=8336
  _globals['_SLBGPLSTOPOADJSID']._serialized_end=8465
  _globals['_SLBGPLSTOPOLANADJSID']._serialized_start=8468
  _globals['_SLBGPLSTOPOLANADJSID']._serialized_end=8656
  _globals['_SLBGPLSTOPOBGPPEERNODESID']._serialized_start=8659
  _globals['_SLBGPLSTOPOBGPPEERNODESID']._serialized_end=8789
  _globals['_SLBGPLSTOPOBGPPEERADJSID']._serialized_start=8792
  _globals['_SLBGPLSTOPOBGPPEERADJSID']._serialized_end=8921
  _globals['_SLBGPLSTOPOBGPPEERSETSID']._serialized_start=8924
  _globals['_SLBGPLSTOPOBGPPEERSETSID']._serialized_end=9053
  _globals['_SLBGPLSTOPONEIGHBORID']._serialized_start=9055
  _globals['_SLBGPLSTOPONEIGHBORID']._serialized_end=9132
  _globals['_SLBGPLSTOPOUNILINKDELAY']._serialized_start=9134
  _globals['_SLBGPLSTOPOUNILINKDELAY']._serialized_end=9189
  _globals['_SLBGPLSTOPOMINMAXUNILINKDELAY']._serialized_start=9191
  _globals['_SLBGPLSTOPOMINMAXUNILINKDELAY']._serialized_end=9263
  _globals['_SLBGPLSTOPOUNIDELAYVAR']._serialized_start=9265
  _globals['_SLBGPLSTOPOUNIDELAYVAR']._serialized_end=9323
  _globals['_SLBGPLSTOPOUNILINKLOSS']._serialized_start=9325
  _globals['_SLBGPLSTOPOUNILINKLOSS']._serialized_end=9378
  _globals['_SLBGPLSTOPOUNIRESBANDWIDTH']._serialized_start=9380
  _globals['_SLBGPLSTOPOUNIRESBANDWIDTH']._serialized_end=9427
  _globals['_SLBGPLSTOPOUNIAVAILBANDWIDTH']._serialized_start=9429
  _globals['_SLBGPLSTOPOUNIAVAILBANDWIDTH']._serialized_end=9478
  _globals['_SLBGPLSTOPOUNIUTILBANDWIDTH']._serialized_start=9480
  _globals['_SLBGPLSTOPOUNIUTILBANDWIDTH']._serialized_end=9528
  _globals['_SLBGPLSTOPOASLAATTR']._serialized_start=9531
  _globals['_SLBGPLSTOPOASLAATTR']._serialized_end=10292
  _globals['_SLBGPLSTOPOPREFIXIGPFLAGS']._serialized_start=10294
  _globals['_SLBGPLSTOPOPREFIXIGPFLAGS']._serialized_end=10336
  _globals['_SLBGPLSTOPOPREFIXIGPROUTETAG']._serialized_start=10338
  _globals['_SLBGPLSTOPOPREFIXIGPROUTETAG']._serialized_end=10381
  _globals['_SLBGPLSTOPOPREFIXIGPEXTROUTETAG']._serialized_start=10383
  _globals['_SLBGPLSTOPOPREFIXIGPEXTROUTETAG']._serialized_end=10429
  _globals['_SLBGPLSTOPOPREFIXMETRIC']._serialized_start=10431
  _globals['_SLBGPLSTOPOPREFIXMETRIC']._serialized_end=10472
  _globals['_SLBGPLSTOPOPREFIXOSPFFWDADDR']._serialized_start=10474
  _globals['_SLBGPLSTOPOPREFIXOSPFFWDADDR']._serialized_end=10559
  _globals['_SLBGPLSTOPOPREFIXOPAQUEATTR']._serialized_start=10561
  _globals['_SLBGPLSTOPOPREFIXOPAQUEATTR']._serialized_end=10610
  _globals['_SLBGPLSTOPOPREFIXSID']._serialized_start=10613
  _globals['_SLBGPLSTOPOPREFIXSID']._serialized_end=10757
  _globals['_SLBGPLSTOPOPREFIXRANGE']._serialized_start=10759
  _globals['_SLBGPLSTOPOPREFIXRANGE']._serialized_end=10869
  _globals['_SLBGPLSTOPOPREFIXATTRFLAGS']._serialized_start=10871
  _globals['_SLBGPLSTOPOPREFIXATTRFLAGS']._serialized_end=10914
  _globals['_SLBGPLSTOPOPREFIXSRCROUTERID']._serialized_start=10916
  _globals['_SLBGPLSTOPOPREFIXSRCROUTERID']._serialized_end=11001
  _globals['_SLBGPLSTOPOL2BUNDLEMEMBERATTR']._serialized_start=11004
  _globals['_SLBGPLSTOPOL2BUNDLEMEMBERATTR']._serialized_end=12154
  _globals['_SLBGPLSTOPOEXTADMINGROUP']._serialized_start=12156
  _globals['_SLBGPLSTOPOEXTADMINGROUP']._serialized_end=12197
  _globals['_SLBGPLSTOPOUNKNOWNATTR']._serialized_start=12199
  _globals['_SLBGPLSTOPOUNKNOWNATTR']._serialized_end=12272
  _globals['_SLBGPLSTOPO']._serialized_start=13667
  _globals['_SLBGPLSTOPO']._serialized_end=13783
# @@protoc_insertion_point(module_scope)
