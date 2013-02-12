# Maintainer: arfoll <brendan@fridu.net>

pkgname=rs232server
pkgver=1
pkgrel=1
pkgdesc="script to control rs232server"
arch=('any')
url="http://github.com/arfoll/rs232server"
license=('GPL')
depends=('python2-pyserial' 'python2-dbus')

_prefix='/usr'

if [ -e .githash_$CARCH ] ; then
	_gitphash=$(cat .githash_$CARCH)
else
	_gitphash=""
fi

_gitname='rs232server'
_gitroot='git://github.com/arfoll/rs232server.git'
#_commit=f122e08648b515b61999729cb7c6dffbc8befbfb

build() {
	if [ -d ${srcdir}/${_gitname}/.git ] ; then
	(
		cd ${srcdir}/${_gitname} && \
		git checkout master && \
		git pull origin master
	)
	msg "The local files are updated."
	else
		( git clone ${_gitroot} ${_gitname} )
	fi
	msg "GIT checkout done or server timeout"

	cd ${_gitname}
	# when commit is set, check that out
	[[ "${_commit}" ]] && git checkout "${_commit}"
	if [ "${_gitphash}" == "$(git show | grep -m 1 commit | sed 's/commit //')" ]; then
		msg "Git hash is the same as previous build"
		return 1
	fi

	msg "creating build directory"
	cd ${srcdir}
	[ -d ${_gitname}-build ] && rm -rf ${_gitname}-build
	/usr/share/git/workdir/git-new-workdir ${_gitname} ${_gitname}-build master

	msg "Starting build..."
	cd ${_gitname}-build

	python2 setup.py build
	cd miniclient/
	./autogen.sh
	./configure --prefix=$_prefix --exec-prefix=$_prefix
	make
}

package() {
	cd ${_gitname}-build/
	python2 setup.py install --root="$pkgdir/" --skip-build --optimize=1
	cd miniclient/
	msg2 "Running make install" 
	make DESTDIR="$pkgdir" install

	# install license file
	install -dm755 ${pkgdir}${_prefix}/share/licenses/${pkgname}
	cp $srcdir/${_gitname}-build/COPYING \
		${pkgdir}${_prefix}/share/licenses/${pkgname}
	# install systemd service
	install -Dm0644 $srcdir/${_gitname}-build/rs232server.service $pkgdir/usr/lib/systemd/system/rs232server.service

	git show | grep -m 1 commit | sed 's/commit //' > ${startdir}/.githash_${CARCH}
}

