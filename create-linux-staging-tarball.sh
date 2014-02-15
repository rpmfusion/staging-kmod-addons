#! /bin/bash
if [[ ! "${1}" ]]; then
	echo "Please give version number as parameter"
	exit 1
fi

tmpdir="$(mktemp -td $(basename ${0}).XXXXXXXXX)"
#targetdir="${PWD}"
targetdir="$(rpm --eval %{_sourcedir})"

# fixme:
# * error handling completely missing
# * remove tmpdir on abortion
pushd ${tmpdir}/ > /dev/null
echo downloading
wget --quiet http://www.kernel.org/pub/linux/kernel/v3.0/linux-${1}.tar.xz
echo extracing
tar -xJf linux-${1}.tar.xz linux-${1}/COPYING linux-${1}/drivers/staging/ linux-${1}/drivers/video/sis/
echo creating archive
mv linux-${1} linux-staging-${1}
# drivers/video/sis/vgatypes.h needed for FB_XGI
tar -cJf ${targetdir}/linux-staging-${1}.tar.xz linux-staging-${1}/COPYING linux-staging-${1}/drivers/staging/ linux-staging-${1}/drivers/video/sis/
rm -rf linux-${1}.tar.xz linux-staging-${1}/
popd > /dev/null
rmdir ${tmpdir}
echo done: ${targetdir}/linux-staging-${1}.tar.xz


