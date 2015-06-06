LIBDIR = $(DESTDIR)/usr/lib/python2.7/dist-packages
SHAREDIR = $(DESTDIR)/usr/share/durian
BINDIR = $(DESTDIR)/usr/bin
CONFDIR = $(DESTDIR)/etc/default

clean:
	find src lib -name '*.pyc' -exec rm -f {} \;

install:
	mkdir -p $(BINDIR)
	mkdir -p $(LIBDIR)
	mkdir -p $(SHAREDIR)
	mkdir -p $(CONFDIR)

	cp -r lib/. $(LIBDIR)/
	cp -r etc/. $(CONFDIR)/
	cp -r bin/. $(BINDIR)/

	cp -r src/. $(SHAREDIR)/

	cp -r definitions $(SHAREDIR)/
	cp -r seeds $(SHAREDIR)/
	cp -r mirrors $(SHAREDIR)/
	cp -r plugins $(SHAREDIR)/
	cp -r themes $(SHAREDIR)/

uninstall:
	rm -f $(BINDIR)/durian
