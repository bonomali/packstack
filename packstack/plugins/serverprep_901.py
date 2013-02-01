"""
prepare server
"""

import os
import logging
import os

from packstack.installer import basedefs
from packstack.installer import common_utils as utils
from packstack.installer import engine_validators as validate
from packstack.installer.exceptions import InstallError


from packstack.modules.ospluginutils import gethostlist

# Controller object will be initialized from main flow
controller = None

# Plugin name
PLUGIN_NAME = "OS-SERVERPREPARE"
PLUGIN_NAME_COLORED = utils.getColoredText(PLUGIN_NAME, basedefs.BLUE)

logging.debug("plugin %s loaded", __name__)

def initConfig(controllerObject):
    global controller
    controller = controllerObject
    logging.debug("Adding SERVERPREPARE KEY configuration")
    conf_params = {"SERVERPREPARE": [
                  {"CMD_OPTION"      : "use-epel",
                   "USAGE"           : "Install OpenStack from EPEL. If set to \"y\" EPEL will be installed on each server",
                   "PROMPT"          : "Should Packstack install EPEL on each server",
                   "OPTION_LIST"     : ["y", "n"],
                   "VALIDATORS"      : [validate.validate_options],
                   "DEFAULT_VALUE"   : "n",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_USE_EPEL",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "additional-repo",
                   "USAGE"           : "A comma separated list of URLs to any additional yum repositories to install",
                   "PROMPT"          : "Enter a comma separated list of URLs to any additional yum repositories to install",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_REPO",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rh-username",
                   "USAGE"           : "To subscribe each server with Red Hat subscription manager, include this with CONFIG_RH_PASSWORD",
                   "PROMPT"          : "To subscribe each server to Red Hat enter a username here",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_RH_USERNAME",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rh-password",
                   "USAGE"           : "To subscribe each server with Red Hat subscription manager, include this with CONFIG_RH_USERNAME",
                   "PROMPT"          : "To subscribe each server to Red Hat enter your password here",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_RH_PASSWORD",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rh-beta-repo",
                   "USAGE"           : "To subscribe each server with Red Hat subscription manager, to Red Hat Beta RPM's",
                   "PROMPT"          : "To subscribe each server to Red Hat Beta RPM's enter y",
                   "OPTION_LIST"     : ["y", "n"],
                   "VALIDATORS"      : [validate.validate_options],
                   "DEFAULT_VALUE"   : "n",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_RH_BETA_REPO",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-server",
                   "USAGE"           : ("To subscribe each server with RHN Satellite,"
                                        "fill Satellite's URL here. Note that either "
                                        "satellite's username/password or activtion "
                                        "key has to be provided/"),
                   "PROMPT"          : ("To subscribe each server with RHN Satellite "
                                        "enter RHN Satellite server URL"),
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_URL",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-username",
                   "USAGE"           : "Username to access RHN Satellite",
                   "PROMPT"          : ("Enter RHN Satellite username or leave plain "
                                        "if you will use activation key instead"),
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : False,
                   "LOOSE_VALIDATION": True,
                   "CONF_NAME"       : "CONFIG_SATELLITE_USERNAME",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-password",
                   "USAGE"           : "Password to access RHN Satellite",
                   "PROMPT"          : ("Enter RHN Satellite password or leave plain "
                                        "if you will use activation key instead"),
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_PASSWORD",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-activation-key",
                   "USAGE"           : "Activation key for subscription to RHN Satellite",
                   "PROMPT"          : ("Enter RHN Satellite activation key or leave plain "
                                        "if you used username/password instead"),
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_AKEY",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-cacert",
                   "USAGE"           : "Specify a path or URL to a SSL CA certificate to use",
                   "PROMPT"          : "Specify a path or URL to a SSL CA certificate to use",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_CACERT",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-profile",
                   "USAGE"           : ("If required specify the profile name that should "
                                        "be used as an identifier for the system in RHN "
                                        "Satellite"),
                   "PROMPT"          : ("If required specify the profile name that should "
                                        "be used as an identifier for the system in RHN "
                                        "Satellite"),
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_PROFILE",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-proxy-host",
                   "USAGE"           : "Specify a HTTP proxy to use with RHN Satellite",
                   "PROMPT"          : "Specify a HTTP proxy to use with RHN Satellite",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_PROXY",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-proxy-username",
                   "USAGE"           : "Specify a username to use with an authenticated HTTP proxy",
                   "PROMPT"          : "Specify a username to use with an authenticated HTTP proxy",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_PROXY_USERNAME",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-proxy-password",
                   "USAGE"           : "Specify a password to use with an authenticated HTTP proxy.",
                   "PROMPT"          : "Specify a password to use with an authenticated HTTP proxy.",
                   "OPTION_LIST"     : [],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_PROXY_PASSWORD",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
                  {"CMD_OPTION"      : "rhn-satellite-flags",
                   "USAGE"           : ("Comma separated list of flags passed to rhnreg_ks. Valid "
                                        "flags are: novirtinfo, norhnsd, nopackages"),
                   "PROMPT"          : "Enter comma separated list of flags passed to rhnreg_ks",
                   "OPTION_LIST"     : ['novirtinfo', 'norhnsd', 'nopackages'],
                   "VALIDATORS"      : [validate_multi_options],
                   "DEFAULT_VALUE"   : "",
                   "MASK_INPUT"      : True,
                   "LOOSE_VALIDATION": False,
                   "CONF_NAME"       : "CONFIG_SATELLITE_FLAGS",
                   "USE_DEFAULT"     : False,
                   "NEED_CONFIRM"    : False,
                   "CONDITION"       : False },
            ]
        }

    conf_groups = [
            { "GROUP_NAME"            : "SERVERPREPARE",
              "DESCRIPTION"           : "Server Prepare Configs ",
              "PRE_CONDITION"         : utils.returnYes,
              "PRE_CONDITION_MATCH"   : "yes",
              "POST_CONDITION"        : False,
              "POST_CONDITION_MATCH"  : True},
        ]

    for group in conf_groups:
        paramList = conf_params[group["GROUP_NAME"]]
        controller.addGroup(group, paramList)


def validate_multi_options(param, options=None):
    """
    Validates if comma separated values given in params are members
    of options.
    """
    # TO-DO: Move this to packstack.installer.setup_validators and modify
    #        it to raise exception as soon as I1bb3486e will be accepted
    options = options or []
    for i in param.split(','):
        if i.strip() not in options:
            msg = 'Given value is not member of allowed values %s: %s'
            # TO-DO: raise ParamValidationError(msg % (options, param))
            print msg % (options, param)
            return False
    return True


def run_rhn_reg(host, server_url, username=None, password=None,
                cacert=None, activation_key=None, profile_name=None,
                proxy_host=None, proxy_user=None, proxy_pass=None,
                flags=None):
    """
    Registers given host to given RHN Satellite server. To successfully
    register either activation_key or username/password is required.
    """
    logging.debug('Setting RHN Satellite server: %s.' % locals())

    mask = []
    cmd = ['/usr/sbin/rhnreg_ks']
    server = utils.ScriptRunner(host)

    # check satellite server url
    server_url = server_url.rstrip('/').endswith('/XMLRPC') \
                    and server_url \
                    or '%s/XMLRPC' % server_url
    cmd.extend(['--serverUrl', server_url])

    if activation_key:
        cmd.extend(['--activationkey', activation_key])
    elif username:
        cmd.extend(['--username', username])
        if password:
            cmd.extend(['--password', password])
            mask.append(password)
    else:
        raise InstallError('Either RHN Satellite activation key or '
                           'username/password must be provided.')

    if cacert:
        # use and if required download given certificate
        location = "/etc/sysconfig/rhn/%s" % os.path.basename(cacert)
        if not os.path.isfile(location):
            logging.debug('Downloading cacert from %s.' % server_url)
            wget_cmd = ('ls %(location)s &> /dev/null && echo -n "" || '
                        'wget -nd --no-check-certificate --timeout=30 '
                        '--tries=3 -O "%(location)s" "%(cacert)s"' %
                        locals())
            server.append(wget_cmd)
        cmd.extend(['--sslCACert', location])

    if profile_name:
        cmd.extend(['--profilename', profile_name])
    if proxy_host:
        cmd.extend(['--proxy', proxy_host])
        if proxy_user:
            cmd.extend(['--proxyUser', proxy_user])
            if proxy_pass:
                cmd.extend(['--proxyPassword', proxy_pass])
                mask.append(proxy_pass)

    flags = flags or []
    flags.append('force')
    for i in flags:
        cmd.append('--%s' % i)

    server.append(' '.join(cmd))
    server.append('yum clean metadata')
    server.execute(maskList=mask)


def run_rhsm_reg(host, username, password, beta):
    """
    Registers given host to Red Hat Repositories via subscription manager.
    """
    server = utils.ScriptRunner(host)

    # register host
    cmd = ('subscription-manager register --username=\"%s\" '
                            '--password=\"%s\" --autosubscribe || true')
    server.append(cmd % (username, password.replace('"','\\"')))

    # subscribe to required channel
    cmd = ('subscription-manager list --consumed | grep -i openstack || '
           'subscription-manager subscribe --pool %s')
    pool = ("$(subscription-manager list --available | "
            "grep -e 'Red Hat OpenStack' -m 1 -A 2 | grep 'Pool Id' | "
            "awk '{print $3}')")
    server.append(cmd % pool)

    server.append("yum clean all")
    server.append("yum-config-manager --enable rhel-server-ost-6-folsom-rpms")
    if beta:
        server.append("yum-config-manager --enable rhel-6-server-beta-rpms")
    server.append("yum clean metadata")
    server.execute(maskList=[password])


def initSequences(controller):
    preparesteps = [
             {'title': 'Preparing servers', 'functions':[serverprep]}
    ]
    controller.addSequence("Preparing servers", [], [], preparesteps)


def serverprep():
    config = controller.CONF

    rh_username = config["CONFIG_RH_USERNAME"].strip()
    rh_password = config["CONFIG_RH_PASSWORD"].strip()

    sat_registered = set()
    satellite_flags = map(lambda i: i.strip(),
                          config["CONFIG_SATELLITE_FLAGS"].split(','))
    satellite_url = config["CONFIG_SATELLITE_URL"]
    satellite_args = {'username': config["CONFIG_SATELLITE_USERNAME"].strip(),
                      'password': config["CONFIG_SATELLITE_PASSWORD"].strip(),
                      'cacert': config["CONFIG_SATELLITE_CACERT"].strip(),
                      'activation_key': config["CONFIG_SATELLITE_AKEY"].strip(),
                      'profile_name': config["CONFIG_SATELLITE_PROFILE"].strip(),
                      'proxy_host': config["CONFIG_SATELLITE_PROXY"].strip(),
                      'proxy_user': config["CONFIG_SATELLITE_PROXY_USERNAME"].strip(),
                      'proxy_pass': config["CONFIG_SATELLITE_PROXY_PASSWORD"].strip(),
                      'flags': satellite_flags}

    for hostname in gethostlist(config):
        if '/' in hostname:
            hostname = hostname.split('/')[0]
        server = utils.ScriptRunner(hostname)

        # install epel if on rhel (or popular derivative thereof) and epel is configured
        if config["CONFIG_USE_EPEL"] == 'y':
            server.append("REPOFILE=$(mktemp)")
            server.append("cat /etc/yum.conf > $REPOFILE")
            server.append("echo -e '[packstack-epel]\nname=packstack-epel\n"
                          "enabled=1\n"
                          "mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch'"
                          ">> $REPOFILE")

            server.append("grep -e 'Red Hat Enterprise Linux' -e 'CentOS' -e 'Scientific Linux' /etc/redhat-release && "
                          "( rpm -q epel-release || yum install -y --nogpg -c $REPOFILE epel-release ) || echo -n ''")
            server.append("rm -rf $REPOFILE")

        # Create the packstack tmp directory
        server.append("mkdir -p %s" % basedefs.PACKSTACK_VAR_DIR)
        # Separately create the tmp directory for this packstack run, this will fail if
        # the directory already exists
        server.append("mkdir --mode 0700 %s" % basedefs.VAR_DIR)

        # set highest priority of RHOS repository if EPEL is installed
        server.append("rpm -q epel-release && yum install -y yum-plugin-priorities || true")
        subs_cmd = ('rpm -q epel-release && openstack-config --set %(repo_file)s %(repo)s priority %(priority)s || true')
        server.append(subs_cmd % {"repo_file": "/etc/yum.repos.d/redhat.repo",
                                  "repo": "rhel-server-ost-6-folsom-rpms",
                                  "priority": 1})

        # Add yum repositories if configured
        CONFIG_REPO = config["CONFIG_REPO"].strip()
        if CONFIG_REPO:
            for i, url in enumerate(CONFIG_REPO.split(',')):
                reponame = 'packstack_%d' % i
                server.append('echo "[%s]\nname=%s\nbaseurl=%s\nenabled=1\npriority=1\ngpgcheck=0"'
                              ' > /etc/yum.repos.d/%s.repo' % (reponame, reponame, url, reponame))

        server.append("yum clean metadata")
        server.execute()

        # Subscribe to Red Hat Repositories if configured
        if rh_username:
            run_rhsm_reg(hostname, rh_username, rh_password, config["CONFIG_RH_BETA_REPO"] == 'y')

        # Subscribe to RHN Satellite if configured
        if satellite_url and hostname not in sat_registered:
            run_rhn_reg(hostname, satellite_url, **satellite_args)
            sat_registered.add(hostname)
