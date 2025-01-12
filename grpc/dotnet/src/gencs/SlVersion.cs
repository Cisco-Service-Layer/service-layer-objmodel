// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: sl_version.proto
// </auto-generated>
#pragma warning disable 1591, 0612, 3021
#region Designer generated code

using pb = global::Google.Protobuf;
using pbc = global::Google.Protobuf.Collections;
using pbr = global::Google.Protobuf.Reflection;
using scg = global::System.Collections.Generic;
namespace ServiceLayer {

  /// <summary>Holder for reflection information generated from sl_version.proto</summary>
  public static partial class SlVersionReflection {

    #region Descriptor
    /// <summary>File descriptor for sl_version.proto</summary>
    public static pbr::FileDescriptor Descriptor {
      get { return descriptor; }
    }
    private static pbr::FileDescriptor descriptor;

    static SlVersionReflection() {
      byte[] descriptorData = global::System.Convert.FromBase64String(
          string.Concat(
            "ChBzbF92ZXJzaW9uLnByb3RvEg1zZXJ2aWNlX2xheWVyKmYKCVNMVmVyc2lv",
            "bhIVChFTTF9WRVJTSU9OX1VOVVNFRBAAEhQKEFNMX01BSk9SX1ZFUlNJT04Q",
            "ABIUChBTTF9NSU5PUl9WRVJTSU9OEAoSEgoOU0xfU1VCX1ZFUlNJT04QABoC",
            "EAFCUVpPZ2l0aHViLmNvbS9DaXNjby1zZXJ2aWNlLWxheWVyL3NlcnZpY2Ut",
            "bGF5ZXItb2JqbW9kZWwvZ3JwYy9wcm90b3M7c2VydmljZV9sYXllcmIGcHJv",
            "dG8z"));
      descriptor = pbr::FileDescriptor.FromGeneratedCode(descriptorData,
          new pbr::FileDescriptor[] { },
          new pbr::GeneratedClrTypeInfo(new[] {typeof(global::ServiceLayer.SLVersion), }, null, null));
    }
    #endregion

  }
  #region Enums
  /// <summary>
  /// Service Layer API version.
  /// This is used in the Global init message exchange to handshake client/server
  /// Version numbers.
  /// </summary>
  public enum SLVersion {
    [pbr::OriginalName("SL_VERSION_UNUSED")] Unused = 0,
    [pbr::OriginalName("SL_MAJOR_VERSION", PreferredAlias = false)] SlMajorVersion = 0,
    [pbr::OriginalName("SL_MINOR_VERSION")] SlMinorVersion = 10,
    [pbr::OriginalName("SL_SUB_VERSION", PreferredAlias = false)] SlSubVersion = 0,
  }

  #endregion

}

#endregion Designer generated code
