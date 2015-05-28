from resource_management import *
import pwd

class Master(Script):

	def gemfire_user_exists(self):
		import params
		try:
			pwd.getpwnam(params.gemfire_user)
			return True
		except KeyError:
			return False

	def install(self, env):
		self.configure(env)

		import os
		import crypt
		import params

		# create gemfire user if not exist
		if not self.gemfire_user_exists():
			Group(params.gemfire_group)
			User(params.gemfire_user,
				gid=params.gemfire_group,
				password=crypt.crypt(params.gemfire_password, 'salt'),
				groups=[params.gemfire_group],
				ignore_failures=True)


		# create gemfire install dir, owner set to gemfire:gemfire
		Directory(params.gemfire_install_dir,
			owner=params.gemfire_user,
			group=params.gemfire_group,
			recursive=True)

		cmd = 'tar -zvxf ' + params.gemfire_tarball_path + ' -C ' + params.gemfire_install_dir
		Execute(cmd, user=params.gemfire_user, timeout=300)

		cmd = 'ln -s ' + params.gemfire_install_dir + '/' + os.path.basename(params.gemfire_tarball_path).split('.')[0] + ' ' + params.gemfire_install_target
		Execute(cmd, user=params.gemfire_user, timeout=300)

		#cmd = 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))'
		#Execute(cmd, user=params.gemfire_user)

		#cmd = 'export PATH=$PATH:$JAVA_HOME/bin:{0}/bin'.format(params.gemfire_install_dir)
		#Execute(cmd, user=params.gemfire_user)

	def configure(self, env):
		import params
		env.set_params(params)

	def start(self, env):
		self.configure(env)

		import params

		# create gemfire working dir, owner set to gemfire:gemfire
		Directory(params.gemfire_locator_dir,
			owner=params.gemfire_user,
			group=params.gemfire_group,
			recursive=True)

		cmd = """
export JAVA_HOME=/usr/jdk64/jdk1.7.0_67
export PATH=$PATH:$JAVA_HOME/bin:{0}/bin
gfsh << EOF
start locator --name=locator-$HOSTNAME --port={1} --dir={2} --J=-Dgemfire.jmx-manager=true --J=-Dgemfire.jmx-manager-start=true
exit;
EOF"""
		Execute(
			cmd.format(params.gemfire_install_target,
				params.gemfire_locator_port,
				params.gemfire_locator_dir),
			user=params.gemfire_user,
			timeout=300)

	def stop(self, env):
		self.configure(env)

		import params

		cmd = """
export JAVA_HOME=/usr/jdk64/jdk1.7.0_67
export PATH=$PATH:$JAVA_HOME/bin:{0}/bin
gfsh << EOF
stop locator --dir={1}
exit;
EOF"""
		Execute(cmd.format(params.gemfire_install_target, params.gemfire_locator_dir), user=params.gemfire_user)

	def status(self, env):
		import status_params
		env.set_params(status_params)
		check_process_status(status_params.locator_pidfile)

if __name__ == '__main__':
	Master().execute()