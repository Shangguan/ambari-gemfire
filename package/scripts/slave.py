from resource_management import *
import pwd

class Slave(Script):

	def gemfire_user_exists(self):
		import params
		try:
			pwd.getpwnam(params.gemfire_user)
			return True
		except KeyError:
			return False

	def install(self, env):
		import os
		import params

		env.set_params(params)

		self.configure(env)

		cmd = 'tar -zvxf ' + params.gemfire_tarball_path + ' -C ' + params.gemfire_install_dir
		Execute(cmd, user=params.gemfire_user, timeout=300)

		cmd = 'ln -s ' + params.gemfire_install_dir + '/' + os.path.basename(params.gemfire_tarball_path).split('.')[0] + ' ' + params.gemfire_install_target
		Execute(cmd, user=params.gemfire_user, timeout=300)

	def configure(self, env):
		import crypt
		import params

		env.set_params(params)

		if not self.gemfire_user_exists():
			Group(params.gemfire_group)
			User(params.gemfire_user,
				gid=params.gemfire_group,
				password=crypt.crypt(params.gemfire_password, 'salt'),
				groups=[params.gemfire_group],
				ignore_failures=True)

		Directory(params.gemfire_install_dir,
			owner=params.gemfire_user,
			group=params.gemfire_group,
			recursive=True)

		Directory(params.conf_dir,
			owner=params.gemfire_user,
			group=params.gemfire_group,
			recursive=True)

		Directory(params.gemfire_server_dir,
			owner=params.gemfire_user,
			group=params.gemfire_group,
			recursive=True)

		File(format("{conf_dir}/gemfire-env.sh"),
			owner=params.gemfire_user,
			group=params.gemfire_group,
			content=InlineTemplate(params.gemfire_env_sh_template))

		File(format("{conf_dir}/gemfire.properties"),
			owner=params.gemfire_user,
			group=params.gemfire_group,
			content=InlineTemplate(params.gemfire_server_properties_file))

	def start(self, env):
		import time
		import params
		env.set_params(params)

		self.configure(env)

		time.sleep(120)

		cmd = """
source {conf_dir}/gemfire-env.sh
gfsh << EOF
start server --name=server-$HOSTNAME --server-port={gemfire_server_port} --dir={gemfire_server_dir} --locators={gemfire_locator_hostname}[{gemfire_locator_port}] --properties-file={conf_dir}/gemfire.properties
exit;
EOF"""
		Execute(format(cmd), user=params.gemfire_user, timeout=600)

	def stop(self, env):
		import params
		env.set_params(params)

		cmd = """
source {conf_dir}/gemfire-env.sh
gfsh << EOF
stop server --dir={gemfire_server_dir}
exit;
EOF"""
		Execute(format(cmd), user=params.gemfire_user)

	def status(self, env):
		import status_params
		env.set_params(status_params)
		check_process_status(status_params.server_pidfile)

if __name__ == '__main__':
	Slave().execute()