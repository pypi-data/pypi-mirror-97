# ghost
serve a web [application](https://github.com/angelogladding/web#a-simple-application) at a domain

**Linux:** `wget gh.ost.lol/ghost.py -qO ghost && python3 ghost`  
**OSX:** `curl gh.ost.lol/ghost.py ghost && python3 ghost`

**Hosts:** [Digital Ocean](https://cloud.digitalocean.com/account/api/tokens)  
**Registrars:** [Dynadot](https://www.dynadot.com/account/domain/setting/api.html)

    $ wget gh.ost.lol/ghost.py -qO ghost && time python3 ghost
    presence name: testing
    digital ocean token:

    creating droplet
    spawning sudoer ghost

     0:00 updating, upgrading
     0:33 installing build-essential, expect, psmisc, xz-utils, zip,
            git, fcgiwrap, supervisor, redis-server, haveged, libicu-dev,
            python3-icu, libsqlite3-dev, libssl-dev, libffi-dev, zlib1g-dev,
            python3-dev, python3-crypto, python3-libtorrent, ffmpeg,
            libsm-dev, python-opencv, libevent-dev, pandoc, graphviz,
            libgtk-3-0, libdbus-glib-1-2, xvfb, x11-utils, libenchant-dev,
            ufw, tmux, php-curl, php-fpm, php-gd, php-intl, php-mbstring,
            php-mysql, php-soap, php-xml, php-xmlrpc, php-zip
     3:27 installing python-3.9.0
     3:27   downloading, extracting, configuring
     4:00   making
     7:40   installing
     8:23 creating virtual environment
     8:29   installing SQLite-latest
    10:19   installing Ghost ecosystem
    10:19     src
    10:43     term
    10:47     kv
    10:53     sql
    10:57     web
    12:22     ghost
    12:27 installing nginx-1.18.0
    12:27   downloading, extracting, configuring
    12:36   making
    13:38   installing
    13:38   generating a large prime for TLS (this will take a long time)

    You may now sign in to your host while installation continues:
        https://165.227.30.1?secret=sepkpt

    13:42 installing tor-0.4.4.5
    13:42   downloading, extracting, configuring
    14:10   making
    21:12   installing
    21:13 installing firefox-82.0
    21:29 installing geckodriver-0.27.0

    python3 ghost ... 22:25.14 total

![](https://github.com/angelogladding/ghost/raw/main/interface.png)
