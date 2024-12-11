# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
#global _disable_lto 1

# This flag prevents internal links
%global _disable_ld_no_undefined 1

%define major 7
%define libname	%mklibname %{name}
%define devname	%mklibname %{name} -d

%define libname_metis	%mklibname %{name}-metis
%define devname_metis	%mklibname %{name}-metis -d

%define libname_openmpi		%mklibname %{name}-openmpi
%define devname_openmpi_parmetis	%mklibname %{name}-openmpi-parmetis
%define devname_openmpi		%mklibname %{name}-openmpi -d

%bcond openmpi	1
%bcond metis	1
%bcond tests	0

Summary:	Graph, mesh and hypergraph partitioning library
Name:		scotch
Version:	7.0.6
Release:	1
Group:		System/Libraries
License:	CeCILL-C
URL:		https://gitlab.inria.fr/scotch/scotch
Source0:	https://gitlab.inria.fr/scotch/scotch/-/archive/v%{version}/scotch-v%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
%if %{with openmpi}
BuildRequires:	pkgconfig(ompi)
%endif
BuildRequires:	pkgconfig(zlib)

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the
ptscotch sub-packages.

#----------------------------------------------------------------------

%package -n %{libname}
Summary:	Graph, mesh and hypergraph partitioning library
Group:		System/Libraries

%description -n %{libname}
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the
ptscotch sub-packages.

%files -n %{libname}
%license doc/CeCILL-C_V1-en.txt
%doc doc/*.pdf
%doc doc/scotch_example.f
%{_libdir}/libesmumps.so.%{major}*
%{_libdir}/libscotch.so.%{major}*
%{_libdir}/libscotcherr.so.%{major}*
%{_libdir}/libscotcherrexit.so.%{major}*
%if %{with metis}
%{_libdir}/libscotchmetisv3.so.%{major}*
%{_libdir}/libscotchmetisv5.so.%{major}*
%endif

#-----------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries for scotch
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains development libraries for scotch.

%files -n %{devname}
%dir %{_includedir}/scotch
%{_includedir}/scotch/scotch.h
%{_includedir}/scotch/scotchf.h
%{_includedir}/scotch/esmumps.h
%{_libdir}/libesmumps.so
%{_libdir}/libscotch.so
%{_libdir}/libscotcherr.so
%{_libdir}/libscotcherrexit.so
%if %{with metis}
%{_libdir}/libscotchmetisv3.so
%{_libdir}/libscotchmetisv5.so
%endif
%dir %{_libdir}/cmake/scotch/
#{_libdir}/cmake/scotch/ptesmumpsTargets*
%{_libdir}/cmake/scotch/esmumpsTargets*
%{_libdir}/cmake/scotch/SCOTCH*
%{_libdir}/cmake/scotch/scotchTargets*
%{_libdir}/cmake/scotch/scotcherrTargets*
%{_libdir}/cmake/scotch/scotcherrexitTargets*

#-----------------------------------------------------------------------

%if %{with metis}
%package -n %{devname_metis} 
Summary:	Metis compatibility header
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}

%description -n %{devname_metis} 
This header is a drop-in replacement for the original metis.h header
to build against the scotch.

%files -n %{devname_metis} 
%dir %{_includedir}/scotch
%{_includedir}/scotch/scotchmetis.h
%{_includedir}/scotch/scotchmetisf.h
%{_libdir}/libscotchmetis.so
%{_libdir}/cmake/scotch/scotchmetisTargets*
%endif

#-----------------------------------------------------------------------

%if %{with openmpi}
%package -n %{libname_openmpi}
Summary:	PT-Scotch libraries compiled against openmpi
Group:		System/Libraries

%description -n %{libname_openmpi}
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. This sub-package provides parallelized scotch libraries
compiled with openmpi.

%files -n %{libname_openmpi}
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/openmpi/lib/libesmumps.so.%{major}*
%{_libdir}/openmpi/lib/libscotch.so.%{major}*
%{_libdir}/openmpi/lib/libscotcherr.so.%{major}*
%{_libdir}/openmpi/lib/libscotcherrexit.so.%{major}*
%{_libdir}/openmpi/lib/libptscotch.so.%{major}*
%{_libdir}/openmpi/lib/libptesmumps.so.%{major}*
%{_libdir}/openmpi/lib/libptscotcherr.so.%{major}*
%{_libdir}/openmpi/lib/libptscotcherrexit.so.%{major}*
%if %{with metis}
%{_libdir}/openmpi/lib/libscotchmetisv3.so.%{major}*
%{_libdir}/openmpi/lib/libscotchmetisv5.so.%{major}*
%{_libdir}/openmpi/lib/libptscotchparmetisv3.so.%{major}*
%endif
%endif

#-----------------------------------------------------------------------

%if %{with openmpi}
%package -n %{devname_openmpi}
Summary:	Development libraries for PT-Scotch (openmpi)
Group:		Development/C
Requires:	%{libname_openmpi} = %{version}-%{release}

%description -n %{devname_openmpi}
This package contains development libraries for PT-Scotch, compiled against
openmpi.

%files -n %{devname_openmpi}
%dir %{_includedir}/openmpi*/scotch
%{_includedir}/openmpi*/scotch/ptscotch.h
%{_includedir}/openmpi*/scotch/ptscotchf.h
%{_includedir}/openmpi*/scotch/scotch.h
%{_includedir}/openmpi*/scotch/scotchf.h
%{_includedir}/openmpi*/scotch/esmumps.h
%{_libdir}/openmpi/lib/libesmumps.so
%{_libdir}/openmpi/lib/libscotch.so
%{_libdir}/openmpi/lib/libscotcherr.so
%{_libdir}/openmpi/lib/libscotcherrexit.so
%{_libdir}/openmpi/lib/libptesmumps.so
%{_libdir}/openmpi/lib/libptscotch.so
%{_libdir}/openmpi/lib/libptscotcherr.so
%{_libdir}/openmpi/lib/libptscotcherrexit.so
%if %{with metis}
%{_libdir}/openmpi/lib/libscotchmetisv3.so
%{_libdir}/openmpi/lib/libscotchmetisv5.so
%{_libdir}/openmpi/lib/libptscotchparmetisv3.so
%endif
%dir %{_libdir}/openmpi/lib/cmake/scotch/
%{_libdir}/openmpi/lib/cmake/scotch/ptesmumpsTargets*
%{_libdir}/openmpi/lib/cmake/scotch/SCOTCHConfig.cmake
%{_libdir}/openmpi/lib/cmake/scotch/SCOTCHConfigVersion.cmake
%{_libdir}/openmpi/lib/cmake/scotch/esmumpsTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotchTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotcherrTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotcherrexitTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotchTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotcherrTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotcherrexitTargets*
%endif

#-----------------------------------------------------------------------

%if %{with openmpi} && %{with metis}
%package -n %{devname_openmpi_parmetis}
Summary:	Parmetis compatibility header
Group:		System/Libraries
Requires:	%{devname_openmpi} = %{version}-%{release}

%description -n %{devname_openmpi_parmetis}
This header is a drop-in replacement for the original parmetis.h header
to build against the scotch.

%files -n %{devname_openmpi_parmetis}
%dir %{_includedir}/openmpi*/scotch
%{_includedir}/openmpi*/scotch/scotchmetis.h
%{_includedir}/openmpi*/scotch/scotchmetisf.h
%{_includedir}/openmpi*/scotch/parmetis.h
%{_libdir}/openmpi/lib/libparmetis.so
%{_libdir}/openmpi/lib/libptscotchparmetis.so
%{_libdir}/openmpi/lib/libscotchmetis.so
%{_libdir}/openmpi/lib/cmake/scotch/ptscotchparmetisTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotchmetisTargets*
%endif

#-----------------------------------------------------------------------

%prep
%autosetup -N -n %{name}-v%{version}

%build
export FC=gfortran
export DEFAULT_PATH="$PATH"

for d in %{_target_cpu}%{?with_openmpi:{,_openmpi}}
do
	if [[ "$d" =~ "openmpi" ]]; then
		INSTALL_BINDIR=%{_libdir}/openmpi/bin
		INSTALL_LIBDIR=%{_libdir}/openmpi/lib/
		INSTALL_INCLUDEDIR=%{_includedir}/openmpi-%{_target_cpu}/scotch
		SCOTCH_PARMETIS_VERSION=3
		BUILD_PTSCOTCH=ON
		MPI_THREAD_MULTIPLE=ON
		PATH=%{_libdir}/openmpi/bin
	else
		INSTALL_BINDIR=%{_bindir}
		INSTALL_LIBDIR=%{_libdir}
		INSTALL_INCLUDEDIR=%{_includedir}/scotch
		SCOTCH_PARMETIS_VERSION=
		BUILD_PTSCOTCH=OFF
		MPI_THREAD_MULTIPLE=OFF
		PATH=
	fi

	PATH="${DEFAULT_PATH}:${PATH}"
	CMAKE_BUILD_DIR="build-$d"
	%cmake \
		-DTHREADS:BOOL=ON \
		-DMPI_THREAD_MULTIPLE:BOOL=${MPI_THREAD_MULTIPLE} \
		-DBUILD_PTSCOTCH:BOOL=${BUILD_PTSCOTCH} \
		-DBUILD_LIBESMUMPS:BOOL=ON \
		-DBUILD_LIBSCOTCHMETIS:BOOL=%{?with_metis:ON}%{?!with_metis:OFF} \
		-DCMAKE_INSTALL_BINDIR=${INSTALL_BINDIR}\
		-DCMAKE_INSTALL_LIBDIR=${INSTALL_LIBDIR} \
		-DCMAKE_INSTALL_INCLUDEDIR=${INSTALL_INCLUDEDIR} \
		-DENABLE_TESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
		-GNinja
	%ninja_build
	cd ..
done

%install
for d in %{_target_cpu}%{?with_openmpi:{,_openmpi}}
do
	if [[ "$d" =~ "openmpi" ]]; then
		INSTALL_BINDIR=%{_libdir}/openmpi/bin
		INSTALL_LIBDIR=%{_libdir}/openmpi/lib
		INSTALL_INCLUDEDIR=%{_includedir}/openmpi-%{_target_cpu}/scotch
	else
		INSTALL_BINDIR=%{_bindir}
		INSTALL_LIBDIR=%{_libdir}
		INSTALL_INCLUDEDIR=%{_includedir}/scotch
	fi

	%define _vpath_builddir build-$d
	%ninja_install -C build-$d

	%if %{with metis}
	# Default to the v5 API for the metis compat library
	ln -s libscotchmetisv5.so %{buildroot}${INSTALL_LIBDIR}/libscotchmetis.so
	if [[ "$d" =~ "openmpi" ]]; then
		ln -s libptscotchparmetisv3.so %{buildroot}${INSTALL_LIBDIR}/libparmetis.so
		ln -s libptscotchparmetisv3.so %{buildroot}${INSTALL_LIBDIR}/libptscotchparmetis.so
	fi
	# Rename include files to avoid conflicts with original Metis
	mv %{buildroot}${INSTALL_INCLUDEDIR}/metis.h %{buildroot}${INSTALL_INCLUDEDIR}/scotchmetis.h
	mv %{buildroot}${INSTALL_INCLUDEDIR}/metisf.h %{buildroot}${INSTALL_INCLUDEDIR}/scotchmetisf.h
	%endif

	# Don't install executables
	rm -f %{buildroot}${INSTALL_BINDIR}/*
	rm -rf %{buildroot}%{_mandir}/*
done

%check
%if %{with tests}
for d in %{_target_cpu}%{?with_openmpi:{,_openmpi}}
do
	pushd build-$d
	ctest || :
	popd 1>/dev/null
done
%endif

