entry_points = {
    'SSHBaseForwarder': [
        'base = ssh_proxy_server.forwarders.ssh:SSHForwarder',
        'mirrorshell = ssh_proxy_server.plugins.ssh.mirrorshell:SSHMirrorForwarder',
        'noshell = ssh_proxy_server.plugins.ssh.noshell:NoShellForwarder',
        'sessionlogger = ssh_proxy_server.plugins.ssh.sessionlogger:SSHLogForwarder'
    ],
    'SCPBaseForwarder': [
        'base = ssh_proxy_server.forwarders.scp:SCPForwarder',
        'inject_file = ssh_proxy_server.plugins.scp.inject_file:SCPInjectFile',
        'replace_file = ssh_proxy_server.plugins.scp.replace_file:SCPReplaceFile',
        'store_file = ssh_proxy_server.plugins.scp.store_file:SCPStorageForwarder'
    ],
    'BaseSFTPServerInterface': [
        'base = ssh_proxy_server.interfaces.sftp:SFTPProxyServerInterface'
    ],
    'SFTPHandlerBasePlugin': [
        'base = ssh_proxy_server.forwarders.sftp:SFTPHandlerPlugin',
        'replace_file = ssh_proxy_server.plugins.sftp.replace_file:SFTPProxyReplaceHandler',
        'store_file = ssh_proxy_server.plugins.sftp.store_file:SFTPHandlerStoragePlugin'
    ],
    'BaseServerInterface': [
        'base = ssh_proxy_server.interfaces.server:ServerInterface'
    ],
    'BaseSSHProxyManager': [
        'base = ssh_proxy_server.interfaces.server:SSHProxyManager'
    ],
    'Authenticator': [
        'passthrough = ssh_proxy_server.authentication:AuthenticatorPassThrough'
    ]
}
