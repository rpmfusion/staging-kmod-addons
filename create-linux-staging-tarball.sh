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
wget --quiet http://www.kernel.org/pub/linux/kernel/v2.6/linux-${1}.tar.bz2
echo extracing
tar -xjf linux-${1}.tar.bz2 linux-${1}/COPYING linux-${1}/drivers/staging/
echo creating archive
mv linux-${1} linux-staging-${1}
tar -cjf ${targetdir}/linux-staging-${1}.tar.bz2 linux-staging-${1}/COPYING linux-staging-${1}/drivers/staging/
rm -rf linux-${1}.tar.bz2 linux-staging-${1}/
popd > /dev/null
rmdir ${tmpdir}
echo done: ${targetdir}/linux-staging-${1}.tar.bz2


