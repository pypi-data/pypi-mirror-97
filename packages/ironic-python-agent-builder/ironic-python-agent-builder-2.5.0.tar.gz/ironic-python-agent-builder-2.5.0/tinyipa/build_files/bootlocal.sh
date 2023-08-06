#!/bin/sh
# put other system startup commands here

#exec > /tmp/installlogs 2>&1
set -x

echo "Starting bootlocal script:"
date

export HOME=/root

# Start SSHd
if [ -x /usr/local/etc/init.d/openssh ]; then
    echo "Starting OpenSSH server:"
    /usr/local/etc/init.d/openssh start
fi

# Start haveged
if [ -x /usr/local/sbin/haveged ]; then
    echo "Starting haveged entropy daemon:"
    /usr/local/sbin/haveged
fi

# Maybe save some RAM?
#rm -rf /tmp/builtin

# Install IPA and dependecies
if ! type "ironic-python-agent" > /dev/null ; then
    PIP_COMMAND="pip"
    if hash pip3 2>/dev/null; then
        PIP_COMMAND="pip3"
    fi
    $PIP_COMMAND install --no-index --find-links=file:///tmp/wheelhouse ironic_python_agent
fi

# Create ipa-rescue-config directory for rescue password
sudo mkdir -p /etc/ipa-rescue-config

# Setup DHCP network
configure_dhcp_network() {
    for pidfile in `ls /var/run/udhcpc*.pid`; do
        kill `cat $pidfile`
    done

    # NOTE(TheJulia): We may need to add a short wait here as
    # network interface plugging actions may not be asynchronous.
    echo "Sleeping 30 sec as network interface is being updated"
    sleep 30
    INTERFACES=$(ip -o link |grep "LOWER_UP"|cut -f2 -d" "|sed 's/://'|grep -v "lo")
    for interface in $INTERFACES; do
        pidfile="/var/run/udhcpc/${interface}.pid"
        /sbin/udhcpc -b -p ${pidfile} -i ${interface} -s /opt/udhcpc.script >> /var/log/udhcpc.log 2>&1
    done
    echo "Completed DHCP client restart"
    echo "Outputting IP and Route information"
    ip addr || true
    ip route || true
    ip -6 route || true
    echo "Logging IPv4 sysctls"
    sysctl -a |grep ipv4 || true
    echo "Logging IPv6 sysctls"
    sysctl -a |grep ipv6 || true
}

# Configure networking, use custom udhcpc script to handle MTU option
configure_dhcp_network

mkdir -p /etc/ironic-python-agent.d/

# Run IPA
echo "Starting Ironic Python Agent:"
date
ironic-python-agent --config-dir /etc/ironic-python-agent.d/ 2>&1 | tee /var/log/ironic-python-agent.log


create_rescue_user() {
    crypted_pass=$(cat /etc/ipa-rescue-config/ipa-rescue-password)
    sudo adduser rescue -D -G root # no useradd
    echo "rescue:$crypted_pass" | sudo chpasswd -e
    sudo sh -c "echo \"rescue ALL=(ALL) NOPASSWD: ALL\" >> /etc/sudoers" # no suooers.d in tiny core.

    # Restart sshd with allowing password authentication
    sudo sed -i -e 's/^PasswordAuthentication no/PasswordAuthentication yes/' /usr/local/etc/ssh/sshd_config
    sudo /usr/local/etc/init.d/openssh restart
}

if [ -f /etc/ipa-rescue-config/ipa-rescue-password ]; then
    create_rescue_user || exit 0
    # The network might change during rescue, renew addresses in this case.
    configure_dhcp_network || exit 0
else
    echo "IPA has exited. No rescue password file was defined."
fi
