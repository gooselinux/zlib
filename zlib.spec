Summary: The zlib compression and decompression library
Name: zlib
Version: 1.2.3
Release: 26%{?dist}
Group: System Environment/Libraries
Source: http://www.zlib.net/zlib-%{version}.tar.gz
Source1: zlib.pc.in
Patch3: zlib-1.2.3-autotools.patch
Patch6: minizip-1.2.3-malloc.patch
Patch7: zlib-1.2.3-pc_file.patch
URL: http://www.gzip.org/zlib/
# /contrib/dotzlib/ have Boost license
License: zlib and Boost
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%package -n minizip
Summary: Minizip manipulates files from a .zip archive
Group: System Environment/Libraries
Requires: zlib = %{version}-%{release}

%description -n  minizip
Minizip manipulates files from a .zip archive.

%package -n minizip-devel
Summary: Development files for the minizip library
Group: Development/Libraries
Requires: minizip = %{version}-%{release}
Requires: zlib-devel = %{version}-%{release}
Requires: pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%prep
%setup -q
%patch3 -p1 -b .atools
# patch cannot create an empty dir
mkdir m4
%patch6 -p1 -b .mal
%patch7 -p1 -b .pc
iconv -f windows-1252 -t utf-8 <ChangeLog >ChangeLog.tmp
mv ChangeLog.tmp ChangeLog
cp Makefile Makefile.old
cp %{SOURCE1} ./

%build
autoreconf --install;
%configure
make %{?_smp_mflags}

%check
make test -f Makefile.old

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libz.so.* $RPM_BUILD_ROOT/%{_lib}/

reldir=$(echo %{_libdir} | sed 's,/$,,;s,/[^/]\+,../,g')%{_lib}
oldlink=$(readlink $RPM_BUILD_ROOT%{_libdir}/libz.so)
ln -sf $reldir/$(basename $oldlink) $RPM_BUILD_ROOT%{_libdir}/libz.so

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

    
%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README ChangeLog FAQ
/%{_lib}/libz.so.*

%files devel
%defattr(-,root,root,-)
%doc README algorithm.txt minigzip.c example.c
%{_libdir}/libz.so
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_mandir}/man3/zlib.3*
%{_libdir}/pkgconfig/zlib.pc

%files static
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%doc contrib/minizip/ChangeLogUnzip
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Fri Jul  8 2011 Mike Adams <shalkie@gooseproject.org> - 1.2.3-26
- Rebuild pakcage for GoOSe Linux 6

* Tue Jun  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.3-25
- Resolves: #597954
  add zlib .pc file

* Mon Mar  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.3-24
- Resolves: #543948
  add Boost license

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.3-23.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Stepan Kasal <skasal@redhat.com> - 1.2.3-22
- fix the libz.so symlink

* Tue Mar 17 2009 Stepan Kasal <skasal@redhat.com> - 1.2.3-21
- consolidate the autoconfiscation patches into one and clean it up
- consequently, clean up the %%build and %%install sections
- zconf.h includes unistd.h again (#479133)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-19
- fix 473490 - unchecked malloc

* Wed Feb 13 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-18
- change license tag (226671#c29)

* Mon Feb 11 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-17
- spec file changes

* Fri Nov 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-16
- remove minizip headers to minizip-devel
- spec file cleanup
- fix minizip.pc file

* Wed Nov 14 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-15
- separate static subpackage

* Wed Aug 15 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-14
- create minizip subpackage

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-13
- remove .so,.a

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-12
- Resolves #240277
  Move libz to /lib(64)

* Mon Apr 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-11
- Resolves: 237295
  fix Summary tag

* Fri Mar 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-10
- remove zlib .so.* packages to /lib

* Fri Mar  9 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-9
- incorporate package review feedback

* Tue Feb 21 2007 Adam Tkac <atkac redhat com> - 1.2.3-8
- fixed broken version of libz

* Tue Feb 20 2007 Adam Tkac <atkac redhat com> - 1.2.3-7
- building is now automatized
- specfile cleanup

* Tue Feb 20 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-6
- remove the compilation part to build section
  some minor changes

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-5
- incorporate package review feedback

* Mon Oct 23 2006 Ivana Varekova <varekova@redhat.com> - 1.2.3-4
- fix #209424 - fix libz.a permissions

* Wed Jul 19 2006 Ivana Varekova <varekova@redhat.com> - 1.2.3-3
- add cflags (#199379)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Florian La Roche <laroche@redhat.com>
- update to 1.2.3

* Fri Jul 22 2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-5
- fix bug 163038 - CAN-2005-1849 - zlib buffer overflow

* Thu Jul 7  2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-4
- fix bug 162392 - CAN-2005-2096 

* Wed Mar 30 2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-3
- fix bug 122408 - zlib build process runs configure twice

* Fri Mar  4 2005 Jeff Johnson <jbj@redhat.com> 1.2.2.2-2
- rebuild with gcc4.

* Sat Jan  1 2005 Jeff Johnson <jbj@jbj.org> 1.2.2.2-1
- upgrade to 1.2.2.2.

* Fri Nov 12 2004 Jeff Johnson <jbj@jbj.org> 1.2.2.1-1
- upgrade to 1.2.2.1.

* Sun Sep 12 2004 Jeff Johnson <jbj@redhat.com> 1.2.1.2-1
- update to 1.2.1.2 to fix 2 DoS problems (#131385).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 18 2004 Jeff Johnson <jbj@jbj.org> 1.2.1.1-1
- upgrade to zlib-1.2.1.1.

* Sun Nov 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.1 release

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 1.2.0.7-3
- unrevert zlib.h include constants (#106291), rejected upstream.

* Wed Oct  8 2003 Jeff Johnson <jbj@jbj.org> 1.2.0.7-2
- fix: gzeof not set when reading compressed file (#106424).
- fix: revert zlib.h include constants for now (#106291).

* Tue Sep 23 2003 Jeff Johnson <jbj@redhat.com> 1.2.0.7-1
- update to 1.2.0.7, penultimate 1.2.1 release candidate.

* Tue Jul 22 2003 Jeff Johnson <jbj@redhat.com> 1.2.0.3-0.1
- update to release candidate.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 1.1.4-9
- rebuild, revert from 1.2.0.1.

* Mon Feb 24 2003 Jeff Johnson <jbj@redhat.com> 1.1.4-8
- fix gzprintf buffer overrun (#84961).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.1.4-7
- rebuilt

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 1.1.4-6
- Make ./configure use $CC to ease cross-compilation

* Tue Nov 12 2002 Jeff Johnson <jbj@redhat.com> 1.1.4-5
- rebuild from cvs.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr 26 2002 Jakub Jelinek <jakub@redhat.com> 1.1.4-2
- remove glibc patch, it is no longer needed (zlib uses gcc -shared
  as it should)
- run tests and only build the package if they succeed

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.1.4-1
- 1.1.4

* Wed Jan 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.1.3-25.7
- Fix double free

* Sun Aug 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.1.3-24
- Add example.c and minigzip.c to the doc files, as
  they are listed as examples in the README (#52574)

* Mon Jun 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Updated URL
- Add version dependency for zlib-devel
- s/Copyright/License/

* Wed Feb 14 2001 Trond Eivind Glomsrød <teg@redhat.com>
- bumped version number - this is the old version without the performance enhancements

* Fri Sep 15 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add -fPIC for shared libs (patch by Fritz Elfert)

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- on 64bit systems, make sure libraries are located correctly.

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 13 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging to build on solaris2.5.1.

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir} and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated URL and source location
- moved README to main package

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- link against glibc

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 1.1.3

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.2
- buildroot

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- added URL tag (down at the moment so it may not be correct)
- made zlib-devel require zlib

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
