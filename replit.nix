{ pkgs }: {
  deps = [
    pkgs.glibc
    pkgs.glibcLocales
    pkgs.zlib
    pkgs.which
    pkgs.snappy
    pkgs.openssl
    pkgs.libjpeg_turbo
    pkgs.jsoncpp
    pkgs.grpc
    pkgs.gitFull
    pkgs.giflib
    pkgs.double-conversion
    pkgs.curl
    pkgs.bazel
    pkgs.python310
  ];
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
    ];
    PYTHONBIN = "${pkgs.python310}/bin/python3.10";
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.glibcLocales
    ];
    LANG = "en_US.UTF-8";
  };
}



