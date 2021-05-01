from ubuntu:20.04

# example:
run apt-get -qq update && apt-get install -qq --no-install-recommends xinetd python3-pip
run pip3 install qunetsim pycryptodome
# TODO: remove this when published
#run apt-get install -qq --no-install-recommends vim netcat

# Note: anything that goes in public_files must be pre-built and checked in git
copy src/service.py /service
copy src/backend.py /backend.py
copy src/coin.py /coin.py
copy src/game.py /game.py
copy src/players.py /players.py
copy src/secret_coin.py /secret_coin.py
copy src/secret_player.py /secret_player.py

# If desired, the deployment tester can pass in the flag from the yaml
ARG THE_FLAG="OOO{this is a test flag}"
RUN touch /flag && chmod 644 /flag && echo $THE_FLAG > /flag

copy service.conf /service.conf
copy banner_fail /banner_fail
copy wrapper /wrapper

expose 5000
cmd ["/usr/sbin/xinetd", "-filelog", "/dev/stderr", "-dontfork", "-f", "/service.conf"]
# ^^ If ps would be too revealing, replace with the line below.
#    AFAIK, this also disables the built-in printf(%n) protection, so YMMV.
#cmd chmod go-rwx /proc && /usr/sbin/xinetd -filelog /dev/stderr -dontfork -f /service.conf
