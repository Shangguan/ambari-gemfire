from resource_management import *

config = Script.get_config()

# common configs
java64_home = config['hostLevelParams']['java_home']

# gemfire user
gemfire_user = config['configurations']['gemfire-config']['gemfire.user']

# gemfire group
gemfire_group = config['configurations']['gemfire-config']['gemfire.group']

# gemfire user password
gemfire_password = config['configurations']['gemfire-config']['gemfire.user.password']

# gemfire installation directory
gemfire_install_dir = config['configurations']['gemfire-config']['gemfire.installation.directory']

# gemfire locator working directory
gemfire_locator_dir = config['configurations']['gemfire-config']['gemfire.locator.working.directory']

# gemfire locator port
gemfire_locator_port = config['configurations']['gemfire-config']['gemfire.locator.port']

# gemfire server working directory
gemfire_server_dir = config['configurations']['gemfire-config']['gemfire.server.working.directory']

# gemfire server port
gemfire_server_port = config['configurations']['gemfire-config']['gemfire.server.port']

# gemfire tarball
gemfire_tarball_path = config['configurations']['gemfire-config']['gemfire.installation.file.path']

# Locator properties file
gemfire_locator_properties_file = config['configurations']['gemfire-config']['gemfire.locator.properties.file']

# Serer properties file
gemfire_server_properties_file = config['configurations']['gemfire-config']['gemfire.server.properties.file']

# gemfire install target
gemfire_install_target = gemfire_install_dir + '/gemfire'

# gemfire locator hostname
gemfire_locator_hostname = config['clusterHostInfo']['gemfire_locator_hosts'][0]

# GemFire env configs
gemfire_env_sh_template = config['configurations']['gemfire-env']['content']
conf_dir = "/etc/gemfire/conf"