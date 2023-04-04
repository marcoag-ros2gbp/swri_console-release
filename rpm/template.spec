%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-swri-console
Version:        2.0.4
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS swri_console package

License:        BSD
URL:            http://ros.org/wiki/swri_console
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-humble-rcl-interfaces
Requires:       ros-humble-rclcpp
Requires:       ros-humble-rosidl-default-runtime
Requires:       ros-humble-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-gui
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-rcl-interfaces
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-ros-environment
BuildRequires:  ros-humble-rosidl-default-generators
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A rosout GUI viewer developed at Southwest Research Insititute as an alternative
to rqt_console.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Tue Apr 04 2023 P. J. Reed <preed@swri.org> - 2.0.4-1
- Autogenerated by Bloom

* Thu Feb 23 2023 P. J. Reed <preed@swri.org> - 2.0.3-2
- Autogenerated by Bloom

* Thu Feb 23 2023 P. J. Reed <preed@swri.org> - 2.0.3-1
- Autogenerated by Bloom

* Thu Nov 03 2022 P. J. Reed <preed@swri.org> - 2.0.2-1
- Autogenerated by Bloom

