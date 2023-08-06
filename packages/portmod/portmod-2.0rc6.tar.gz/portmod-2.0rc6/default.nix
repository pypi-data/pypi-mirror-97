{ pkgs ? import (builtins.fetchTarball {
  name = "nixpkgs-unstable";
  url = "https://github.com/nixos/nixpkgs/archive/ebd2e632d613b1e42a3ca35c9dd495693f93e706.tar.gz"; # as of 6 september 2020
  sha256 = "100q0pkx24z0iabq40dnbdximdg3k31b0jbmfz8xyvxz3cix1llv";
}) {},
naersk ? pkgs.fetchFromGitHub {
	owner = "nmattia";
	repo = "naersk";
	rev = "529e910a3f423a8211f8739290014b754b2555b6";
	sha256 = "3pDN/W17wjVDbrkgo60xQSb24+QAPQ7ulsUq5atNni0=";
} }:

let

	src = ./.;

	py-package = pkgs.python3Packages;

	naersk-lib = pkgs.callPackage naersk {};

	portmod-rust-srcs = {
		cargo-toml = ./Cargo.toml;
		cargo-lock = ./Cargo.lock;
		rust-src = ./src;
		locales = ./l10n;
	};

	portmod-rust-src = pkgs.stdenv.mkDerivation {
		name = "portmod-src-git";
		src = portmod-rust-srcs.rust-src;
		installPhase = ''
			mkdir $out
			cp ${portmod-rust-srcs.cargo-toml} $out/Cargo.toml
			cp ${portmod-rust-srcs.cargo-lock} $out/Cargo.lock
			cp -rf ${portmod-rust-srcs.rust-src} $out/src
			cp -rf ${portmod-rust-srcs.locales} $out/l10n
		'';
		noAuditTmpdir = true;
	};

	portmod-rust = naersk-lib.buildPackage {
		src = portmod-rust-src;
		buildInputs = [ py-package.python ];
		copyLibs = true;
	};

	pysat = py-package.buildPythonPackage rec {
    pname = "pysat";
    version = "0.1.6.dev6";

    src = pkgs.fetchFromGitHub {
      owner = "pysathq";
      repo = "pysat";
      rev = version;
      sha256 = "3hgZG9emcjWYrIUOoYHH2ktDAu6/o8frPdz/PTHsk70=";
    };

    doCheck = false; # require optional dependancies

    propagatedBuildInputs = [ py-package.six ];
  };

	baron = py-package.buildPythonPackage rec {
		pname = "baron";
		version = "0.9";

		src = py-package.fetchPypi {
			inherit version pname;
			sha256 = "sFifMrkc9txFDqanG0oijEM++HVrQfq/iIFaPC05Kzo=";
		};

		checkInputs = [ py-package.pytest ];
		propagatedBuildInputs = [ py-package.rply ];
	};

  redbaron = py-package.buildPythonPackage rec {
    pname = "redbaron";
    version = "0.9.2";

    src = py-package.fetchPypi {
      inherit version pname;
      sha256 = "Ry0HOcprIkC7IniuQoYEp1RyycEuhsYyHowBYTnAEy8=";
    };

    doCheck = false; # some test fails...
    propagatedBuildInputs = [ baron ];
  };

  patool = py-package.buildPythonApplication rec {
    pname = "patool";
    version = "1.12";

    src = py-package.fetchPypi {
      inherit version pname;
      sha256 = "4xgM+L/hO+289vVihFL8oMLISjta6MLT9Vcg6gTLEJc=";
    };

		doCheck = false; # require a bunch of archive manager
		checkInputs = [ py-package.pytest ];
  };

	perl-package = pkgs.perlPackages;

	tes3cmd = pkgs.stdenv.mkDerivation rec {
		pname = "tes3cmd";
		version = "v0.40-pre-release-2";

		src = pkgs.fetchFromGitHub {
			owner = "john-moonsugar";
			repo = pname;
			rev = "f72e9ed9dd18e8545dd0dc2a4056c250cf505790";
			sha256 = "Ry05CAsdNkhlKSKOLiwcLhvz5wd2mEQKtR0sjy69+Ac=";
		};

		buildInputs = [ perl-package.perl ];

		installPhase = ''
			mkdir -p $out/bin

			cp tes3cmd $out/bin/tes3cmd
		'';
	};

	tr-patcher = let
		translation_file = pkgs.fetchurl {
			url = "https://gitlab.com/bmwinger/tr-patcher/-/raw/master/lib/Translation.txt?inline=false";
			sha256 = "yB6bnvYJNUeMOn5Yi8hBhNRliomdk2EFD5ascbRo34w=";
		};
	in
	pkgs.stdenv.mkDerivation rec {
		pname = "tr-patcher";
		version = "1.0.5";

		src = pkgs.fetchzip {
			url = "https://gitlab.com/bmwinger/tr-patcher/uploads/b57899980b2351c136393f02977c4fab/tr-patcher-shadow.zip";
			sha256 = "3HYbYeZodNvySJxk6W8umPiCRLBpiQ+YFXe4R+uyR20=";
		};

		nativeBuildInputs = [ pkgs.makeWrapper ];

		installPhase = ''
			mkdir -p $out/bin
			mkdir -p $out/lib
			cp lib/tr-patcher-all.jar $out/lib/tr-patcher.jar
			cp ${translation_file} $out/lib/Translation.txt
			makeWrapper ${pkgs.jre}/bin/java $out/bin/tr-patcher \
				--add-flags "-jar $out/lib/tr-patcher.jar"
		'';
	};

	bin-program = [
		tes3cmd
		tr-patcher
		py-package.virtualenv
		pkgs.imagemagick7
		pkgs.p7zip
		pkgs.bubblewrap
		pkgs.unrar
		pkgs.git
		pkgs.file
		pkgs.openmw
	];
in
py-package.buildPythonApplication rec {
	inherit src;
	pname = "portmod";

	version = "git"; #TODO: dynamically find the version

	prePatch = ''
		echo patching setup.py to make him not compile the rust library
		substituteInPlace setup.py \
			--replace "from setuptools_rust import Binding, RustExtension" "" \
			--replace "RustExtension(\"portmod.portmod\", binding=Binding.PyO3, strip=True)" ""
	'';

	SETUPTOOLS_SCM_PRETEND_VERSION = version;

	propagatedBuildInputs = with py-package; [
		setuptools_scm
		setuptools
		requests
		chardet
		colorama
		restrictedpython
		appdirs
		black
		GitPython
		progressbar2
		pysat
		redbaron
		patool
		packaging
	];

	nativeBuildInputs = bin-program ++ [ py-package.pytest py-package.black ];

	doCheck = false; # python doesn't seem to have access to example repo ...

	postInstall = ''
	echo $out/bin/*
		cp ${portmod-rust}/lib/libportmod.so $(echo $out/lib/python*/*/portmod)/portmod.so
		for script in $out/bin/*
		do
			wrapProgram $script \
				--prefix PATH : ${pkgs.lib.makeBinPath bin-program } \
				--prefix GIT_SSL_CAINFO : ${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
		done
	'';
}
