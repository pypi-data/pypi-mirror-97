import os
import datetime
from distutils.util import strtobool
from time import sleep


class CLI(object):
    @staticmethod
    def info(text):
        print(f'{Colors.BLUE}{text}{Colors.ENDC}')

    @staticmethod
    def error(text):
        exit(f'{Colors.RED}{text}{Colors.ENDC}')

    @staticmethod
    def underline(text):
        print(f'{Colors.UNDERLINE}{text}{Colors.ENDC}')

    @staticmethod
    def step(index, total, text):
        print(f'{Colors.YELLOW}[{index}/{total}] {text}{Colors.ENDC}')


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PINK = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Mantis(object):
    environment_id = None
    docker_ssh = ''

    def __init__(self, config=None, environment_id=None):
        self.environment_id = environment_id
        self.init_config(config)

    def init_config(self, config):
        if config is not None:
            variables = config
            prefix = ''
        else:
            prefix = 'MANTIS_'
            # self.environment_file_prefix = variables.get(f'{prefix}ENVIRONMENT_FILE_PREFIX', '')
            self.configs_path = os.environ.get(f'{prefix}CONFIGS_FOLDER_PATH', '')
            self.environment_file_prefix = os.environ.get(f'{prefix}ENVIRONMENT_FILE_PREFIX', '')
            self.environment_file = f'{self.configs_path}configs/environments/{self.environment_file_prefix}{self.environment_id}.env'
            # variables = os.environ
            variables = self.load_environment()

        self.user = variables[f'{prefix}USER']

        if self.environment_id is not None:
            # Get environment settings
            if self.environment_id == 'dev':
                self.host = 'localhost'
            else:
                self.host = variables[f'{prefix}HOST']
                self.port = variables[f'{prefix}PORT']
                self.docker_ssh = f'-H "ssh://{self.user}@{self.host}:{self.port}"'

            print(f'Deploying to {Colors.BOLD}{self.environment_id}{Colors.ENDC}: {Colors.RED}{self.host}{Colors.ENDC}')

        self.PROJECT_NAME = variables[f'{prefix}PROJECT_NAME']
        self.IMAGE_NAME = variables[f'{prefix}IMAGE_NAME']
        self.DOCKER_REPOSITORY = variables[f'{prefix}DOCKER_REPOSITORY']
        self.DOCKER_TAG = variables[f'{prefix}DOCKER_TAG']
        self.CONTAINER_PREFIX = variables[f'{prefix}CONTAINER_PREFIX']
        self.CONTAINER_SUFFIX_DB = variables[f'{prefix}CONTAINER_SUFFIX_DB']
        self.CONTAINER_SUFFIX_CACHE = variables[f'{prefix}CONTAINER_SUFFIX_CACHE']
        self.CONTAINER_SUFFIX_APP = variables[f'{prefix}CONTAINER_SUFFIX_APP']
        self.CONTAINER_SUFFIX_QUEUE = variables[f'{prefix}CONTAINER_SUFFIX_QUEUE']
        self.CONTAINER_SUFFIX_WEBSERVER = variables[f'{prefix}CONTAINER_SUFFIX_WEBSERVER']
        self.CONTAINER_APP = f'{self.CONTAINER_PREFIX}{self.CONTAINER_SUFFIX_APP}'
        self.CONTAINER_QUEUE = f'{self.CONTAINER_PREFIX}{self.CONTAINER_SUFFIX_QUEUE}'
        self.CONTAINER_DB = f'{self.CONTAINER_PREFIX}{self.CONTAINER_SUFFIX_DB}'
        self.CONTAINER_CACHE = f'{self.CONTAINER_PREFIX}{self.CONTAINER_SUFFIX_CACHE}'
        self.CONTAINER_WEBSERVER = f'{self.CONTAINER_PREFIX}{self.CONTAINER_SUFFIX_WEBSERVER}'
        self.WEBSERVER = variables.get(f'{prefix}WEBSERVER', 'nginx')
        self.SWARM = strtobool(variables.get(f'{prefix}SWARM', 'False'))
        self.SWARM_STACK = variables.get(f'{prefix}SWARM_STACK', self.CONTAINER_PREFIX)
        self.compose_name = variables.get(f'{prefix}COMPOSE_NAME', '')
        self.COMPOSE_PREFIX = 'docker-compose' if self.compose_name == '' else f'docker-compose.{self.compose_name}'
        self.webserver_config = f'{self.configs_path}configs/{self.WEBSERVER}/{self.environment_file_prefix}{self.environment_id}.conf'
        self.webserver_config_proxy = f'configs/{self.WEBSERVER}/proxy_directives.conf'
        self.htpasswd = f'secrets/.htpasswd'

    def load_environment(self):
        with open(self.environment_file) as fh:
            return dict(
                (line.split('=', maxsplit=1)[0], line.split('=', maxsplit=1)[1].rstrip("\n"))
                for line in fh.readlines() if not line.startswith('#')
            )

    def build(self, params=''):
        CLI.info(f'Building...')
        CLI.info(f'Params = {params}')
        steps = 1

        CLI.step(1, steps, 'Building Docker image...')

        env = self.load_environment()
        build_args = env.get('MANTIS_BUILD_ARGS', '')

        if build_args != '':
            build_args = build_args.split(',')
            build_args = [f'--build-arg {arg}' for arg in build_args]
            build_args = ' '.join(build_args)

        os.system(f'docker build . {build_args} -t {self.IMAGE_NAME} -f configs/docker/Dockerfile {params}')

    def push(self):
        CLI.info(f'Pushing...')

        steps = 2
        CLI.step(1, steps, 'Tagging Docker image...')
        os.system(f'docker tag {self.IMAGE_NAME} {self.DOCKER_REPOSITORY}:{self.DOCKER_TAG}')
        print(f'Successfully tagged {self.DOCKER_REPOSITORY}:{self.DOCKER_TAG}')

        CLI.step(2, steps, 'Pushing Docker image...')
        os.system(f'docker push {self.DOCKER_REPOSITORY}:{self.DOCKER_TAG}')

    def pull(self):
        CLI.info('Pulling docker image...')
        os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml pull')

    def upload(self):
        CLI.info('Uploading...')
        steps = 2

        CLI.step(1, steps, 'Uploading webserver server configs...')

        if self.environment_id == 'dev':
            print('Skippipng...')
        else:
            # rsync -arvz -e 'ssh -p <port-number>' --progress --delete user@remote-server:/path/to/remote/folder /path/to/local/folder
            os.system(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {self.webserver_config} {self.user}@{self.host}:/home/{self.user}/public_html/web/configs/{self.WEBSERVER}/')
            os.system(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {self.webserver_config_proxy} {self.user}@{self.host}:/etc/nginx/conf.d/proxy/')
            os.system(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {self.htpasswd} {self.user}@{self.host}:/etc/nginx/conf.d/')

        CLI.step(2, steps, 'Pulling docker image...')
        os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml pull')

    def restart(self):
        CLI.info('Restarting...')
        steps = 4

        if self.SWARM:
            CLI.step(1, steps, 'Stopping and removing Docker app service...')

            for service in self.get_services():
                if service == self.CONTAINER_APP:
                    os.system(f'docker service rm {service}')

            CLI.step(2, steps, 'Recreating Docker swarm stack...')
            os.system(f'docker stack deploy -c configs/docker/{self.COMPOSE_PREFIX}.yml -c configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml {self.PROJECT_NAME}')

            CLI.step(3, steps, 'Prune Docker images and volumes')  # todo prune on every node
            os.system(f'docker {self.docker_ssh} system prune --volumes --force')

            CLI.step(4, steps, 'Collecting static files')  # todo collect static
            app_container = self.get_containers_starts_with(self.CONTAINER_APP)

            if app_container:
                os.system(f'docker {self.docker_ssh} exec -i {app_container[0]} python manage.py collectstatic --noinput --verbosity 0')

        else:
            CLI.step(1, steps, 'Stopping and removing Docker app container...')

            for container in self.get_containers():
                if container in [self.CONTAINER_APP, self.CONTAINER_QUEUE]:
                    os.popen(f'docker {self.docker_ssh} container stop {container}').read()
                    os.system(f'docker {self.docker_ssh} container rm {container}')

            CLI.step(2, steps, 'Recreating Docker containers...')
            os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml --project-name={self.PROJECT_NAME} up --remove-orphans -d')

            CLI.step(3, steps, 'Prune Docker images and volumes')
            os.system(f'docker {self.docker_ssh} system prune --volumes --force')

            CLI.step(4, steps, 'Collecting static files')
            os.system(f'docker {self.docker_ssh} exec -i {self.CONTAINER_APP} python manage.py collectstatic --noinput --verbosity 0')

    def deploy(self):  # todo deploy swarm
        CLI.info('Deploying...')
        zero_downtime_containers = {'app': self.CONTAINER_APP}
        restart_containers = {'queue': self.CONTAINER_QUEUE}
        steps = 2 * len(zero_downtime_containers) + len(restart_containers) + 3
    
        step = 1
        CLI.step(step, steps, 'Pulling docker image...')
        os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml pull')

        for service, container in zero_downtime_containers.items():
            step += 1
            CLI.step(step, steps, f'Zero downtime deployment of container [{container}]...')

            CLI.info(f'Creating new container [{container}_new]...')
            os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml --project-name={self.PROJECT_NAME} run -d --service-ports --name={container}_new {service}')

            CLI.info(f'Renaming old container [{container}_old]...')

            if container in self.get_containers():
                os.system(f'docker {self.docker_ssh} container rename {container} {container}_old')
            else:
                CLI.info(f'{container}_old was not running')

            CLI.info(f'Renaming new container [{container}]...')
            os.system(f'docker {self.docker_ssh} container rename {container}_new {container}')

        step += 1
        CLI.step(step, steps, 'Collecting static files')
        os.system(f'docker {self.docker_ssh} exec -i {self.CONTAINER_APP} python manage.py collectstatic --noinput --verbosity 0')

        step += 1
        CLI.step(step, steps, 'Reloading webserver...')
        os.system(f'docker {self.docker_ssh} exec -it {self.CONTAINER_WEBSERVER} {self.WEBSERVER} -s reload')

        for service, container in zero_downtime_containers.items():
            step += 1
            CLI.step(step, steps, f'Stopping old container [{container}_old]...')

            if container in self.get_containers():
                CLI.info(f'Stopping old container [{container}_old]...')
                os.system(f'docker {self.docker_ssh} container stop {container}_old')

                CLI.info(f'Removing old container [{container}_old]...')
                os.system(f'docker {self.docker_ssh} container rm {container}_old')
            else:
                CLI.info(f'{container}_old was not running')

        for service, container in restart_containers.items():
            step += 1
            CLI.step(step, steps, f'Recreating container [{container}]...')

            if container in self.get_containers():
                CLI.info(f'Stopping container [{container}]...')
                os.system(f'docker {self.docker_ssh} container stop {container}')

                CLI.info(f'Removing container [{container}]...')
                os.system(f'docker {self.docker_ssh} container rm {container}')

                CLI.info(f'Creating new container [{container}]...')
                os.system(f'docker-compose {self.docker_ssh} -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.yml -f {self.configs_path}configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml --project-name={self.PROJECT_NAME} run -d --service-ports --name={container} {service}')
            else:
                CLI.info(f'{container} was not running')

    def stop(self, params=None):
        if self.SWARM:  # todo can stop service ?
            CLI.info('Removing services...')
            os.system(f'docker stack rm {self.PROJECT_NAME}')

        else:
            CLI.info('Stopping containers...')

            containers = self.get_containers() if not params else params.split(' ')

            steps = len(containers)

            for index, container in enumerate(containers):
                CLI.step(index + 1, steps, f'Stopping {container}')
                os.system(f'docker {self.docker_ssh} container stop {container}')

    def start(self, params):
        if self.SWARM:
            CLI.info('Starting services...')
            os.system(f'docker stack deploy -c configs/docker/{self.COMPOSE_PREFIX}.yml -c configs/docker/{self.COMPOSE_PREFIX}.{self.environment_id}.yml {self.PROJECT_NAME}')

        else:
            CLI.info('Starting containers...')

            containers = self.get_containers() if not params else params.split(' ')

            steps = len(containers)

            for index, container in enumerate(containers):
                CLI.step(index + 1, steps, f'Starting {container}')
                os.system(f'docker {self.docker_ssh} container start {container}')

    def remove(self, params=''):
        if self.SWARM:  # todo remove containers as well ?
            CLI.info('Removing services...')
            os.system(f'docker stack rm {self.PROJECT_NAME}')

        else:
            CLI.info('Removing containers...')

            containers = self.get_containers() if params == '' else params.split(' ')

            steps = len(containers)

            for index, container in enumerate(containers):
                CLI.step(index + 1, steps, f'Removing {container}')
                os.system(f'docker {self.docker_ssh} container rm {container}')

    def clean(self):  # todo clean on all nodes
        CLI.info('Cleaning...')
        steps = 1

        CLI.step(1, steps, 'Prune Docker images and volumes')
        os.system(f'docker {self.docker_ssh} system prune --volumes --force')

    def reload_webserver(self):
        CLI.info('Reloading webserver...')
        os.system(f'docker {self.docker_ssh} exec -it {self.CONTAINER_WEBSERVER} {self.WEBSERVER} -s reload')

    def restart_proxy(self):
        CLI.info('Restarting proxy...')
        steps = 1

        CLI.step(1, steps, 'Reloading proxy container...')
        os.system(f'docker-compose {self.docker_ssh} -f configs/docker/docker-compose.{self.environment_id}.proxy.yml --project-name=reverse up -d')

    def status(self):
        if self.SWARM:  # todo remove containers as well ?
            CLI.info('Getting status...')
            os.system(f'docker stack services {self.PROJECT_NAME}')

        else:
            CLI.info('Getting status...')
            steps = 2

            CLI.step(1, steps, 'List of Docker images')
            os.system(f'docker {self.docker_ssh} image ls')

            CLI.step(2, steps, 'Docker containers')
            os.system(f'docker {self.docker_ssh} container ls -a --size')

    def networks(self):
        # todo for swarm
        CLI.info('Getting networks...')
        steps = 1

        CLI.step(1, steps, 'List of Docker networks')

        networks = os.popen(f'docker {self.docker_ssh} network ls').read()
        networks = networks.strip().split('\n')

        for index, network in enumerate(networks):
            network_data = list(filter(lambda x: x != '', network.split(' ')))
            network_name = network_data[1]

            if index == 0:
                print(f'{network}\tCONTAINERS')
            else:
                containers = os.popen(f'docker {self.docker_ssh} network inspect -f \'{{{{ range $key, $value := .Containers }}}}{{{{ .Name }}}} {{{{ end }}}}\' {network_name}').read()
                containers = ', '.join(containers.split())
                print(f'{network}\t{containers}'.strip())

    def logs(self, params=None):
        if self.SWARM:
            CLI.info('Reading logs...')

            services = params.split(' ') if params else self.get_services()
            lines = '-f' if params else '--tail 10'
            steps = len(services)

            for index, service in enumerate(services):
                CLI.step(index + 1, steps, f'{service} logs')
                os.system(f'docker service logs {service} {lines}')

        else:
            CLI.info('Reading logs...')

            containers = params.split(' ') if params else self.get_containers()
            lines = '-f' if params else '--tail 10'
            steps = len(containers)

            for index, container in enumerate(containers):
                CLI.step(index + 1, steps, f'{container} logs')
                os.system(f'docker {self.docker_ssh} logs {container} {lines}')

    def shell(self):
        CLI.info('Connecting to Django shell...')
        os.system(f'docker {self.docker_ssh} exec -i {self.CONTAINER_APP} python manage.py shell')

    def ssh(self, params):
        CLI.info('Logging to container...')
        os.system(f'docker {self.docker_ssh} exec -it {params} /bin/sh')

    def manage(self, params):
        CLI.info('Django manage...')
        os.system(f'docker {self.docker_ssh} exec -ti {self.CONTAINER_APP} python manage.py {params}')

    def psql(self):
        CLI.info('Starting psql...')
        env = self.load_environment()
        os.system(f'docker {self.docker_ssh} exec -it {self.CONTAINER_DB} psql -h {env["POSTGRES_HOST"]} -U {env["POSTGRES_USER"]} -d {env["POSTGRES_DBNAME"]} -W')
        # https://blog.sleeplessbeastie.eu/2014/03/23/how-to-non-interactively-provide-password-for-the-postgresql-interactive-terminal/
        # TODO: https://www.postgresql.org/docs/9.1/libpq-pgpass.html

    def exec(self, params):
        container, command = params.split(' ', maxsplit=1)
        CLI.info(f'Executing command "{command}" in container {container}...')
        os.system(f'docker {self.docker_ssh} exec -it {container} {command}')

    def pg_dump(self):
        now = datetime.datetime.now()
        # filename = now.strftime("%Y%m%d%H%M%S")
        filename = now.strftime(f"{self.PROJECT_NAME}_%Y%m%d_%H%M.pg")
        CLI.info(f'Backuping database into file {filename}')
        env = self.load_environment()
        os.system(f'docker {self.docker_ssh} exec -it {self.CONTAINER_DB} bash -c \'pg_dump -Fc -h {env["POSTGRES_HOST"]} -U {env["POSTGRES_USER"]} {env["POSTGRES_DBNAME"]} -W > /backups/{filename}\'')
        # https://blog.sleeplessbeastie.eu/2014/03/23/how-to-non-interactively-provide-password-for-the-postgresql-interactive-terminal/
        # TODO: https://www.postgresql.org/docs/9.1/libpq-pgpass.html

    def pg_restore(self, params):
        CLI.info(f'Restoring database from file {params}')
        CLI.underline("Don't forget to drop database at first to prevent constraints collisions!")
        env = self.load_environment()
        os.system(f'docker {self.docker_ssh} exec -it {self.CONTAINER_DB} bash -c \'pg_restore -h {env["POSTGRES_HOST"]} -U {env["POSTGRES_USER"]} -d {env["POSTGRES_DBNAME"]} -W < /backups/{params}\'')
        # https://blog.sleeplessbeastie.eu/2014/03/23/how-to-non-interactively-provide-password-for-the-postgresql-interactive-terminal/
        # TODO: https://www.postgresql.org/docs/9.1/libpq-pgpass.html

    def send_test_email(self):
        CLI.info('Sending test email...')
        os.system(f'docker {self.docker_ssh} exec -i {self.CONTAINER_APP} python manage.py sendtestemail --admins')

    def get_containers(self):
        containers = os.popen(f'docker {self.docker_ssh} container ls -a --format \'{{{{.Names}}}}\'').read()
        containers = containers.strip().split('\n')
        containers = list(filter(lambda x: x.startswith(self.CONTAINER_PREFIX), containers))
        return containers

    def get_services(self):
        services = os.popen(f'docker stack services {self.SWARM_STACK} --format \'{{{{.Name}}}}\'').read()
        services = services.strip().split('\n')
        services = list(filter(lambda x: x.startswith(self.CONTAINER_PREFIX), services))
        return services

    def get_containers_starts_with(self, start_with):
        return [i for i in self.get_containers() if i.startswith(start_with)]
