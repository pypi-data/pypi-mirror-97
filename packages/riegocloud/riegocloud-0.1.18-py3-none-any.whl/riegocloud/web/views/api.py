from aiohttp import web
import asyncio
from jinja2 import FileSystemLoader, Environment, TemplateNotFound
from pathlib import Path

from logging import getLogger
_log = getLogger(__name__)


class Api():
    def __init__(self, app, db, security, options):
        self._db_conn = db.conn
        self._security = security
        self._options = options
        app.router.add_post(options.http_server_endpoint,
                            self._api_post, name='api')

    async def _api_post(self, request):
        data = await request.json()
        cloud_identifier = data.get('cloud_identifier', '')
        public_user_key = data.get('public_user_key', '')
        if not len(cloud_identifier) or not len(public_user_key):
            await asyncio.sleep(5)
            raise web.HTTPBadRequest

        cursor = self._db_conn.cursor()
        cursor.execute("""SELECT MAX(ssh_server_listen_port) AS max_port
                        FROM clients""")
        max_port = cursor.fetchone()
        max_port = max_port['max_port']
        if max_port is None or max_port == 0:
            ssh_server_listen_port = 33333
        else:
            ssh_server_listen_port = max_port + 1
        try:
            cursor.execute(
                """INSERT INTO clients
                        (cloud_identifier, public_user_key,
                        ssh_server_listen_port,
                        ssh_server_hostname, ssh_server_port)
                        VALUES (%s,%s,%s,%s,%s)""",
                (cloud_identifier, public_user_key,
                 ssh_server_listen_port,
                 self._options.ssh_server_hostname,
                 self._options.ssh_server_port))
            self._db_conn.commit()
        except Exception:
            self._db_conn.rollback()
            cursor.execute('''UPDATE clients SET
                        public_user_key = %s,
                        ssh_server_listen_port = %s,
                        ssh_server_hostname = %s,
                        ssh_server_port = %s
                        WHERE cloud_identifier = %s ''',
                           (public_user_key,
                            ssh_server_listen_port,
                            self._options.ssh_server_hostname,
                            self._options.ssh_server_port,
                            cloud_identifier))
            self._db_conn.commit()
            if cursor.rowcount < 1:
                _log.error('Cannot update Client:')
                await asyncio.sleep(5)
                raise web.HTTPBadRequest
            else:
                _log.debug(f'Updated Client: {cloud_identifier}')
        else:
            _log.debug(f'Created Client: {cloud_identifier}')

        data['ssh_server_hostname'] = self._options.ssh_server_hostname
        data['ssh_server_port'] = self._options.ssh_server_port
        data['ssh_server_listen_port'] = ssh_server_listen_port
        data['cloud_server_url'] = self._options.cloud_server_url

        await self._create_apache_conf()
        await self._create_nginx_conf()
        return web.json_response(data)

    async def _create_apache_conf(self):
        cursor = self._db_conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()

        env = Environment(
            loader=FileSystemLoader(
                Path(self._options.apache_tpl_file).parent),
            autoescape=False
        )
        try:
            template = env.get_template(
                Path(self._options.apache_tpl_file).name)
        except TemplateNotFound as e:
            _log.error(f'No Apache template found: {e}')
            return False

        Path(self._options.apache_conf_file).parent.mkdir(
            parents=True, exist_ok=True)

        with open(self._options.apache_conf_file, "w") as f:
            f.write(template.render(clients=clients))

        try:
            proc = await asyncio.create_subprocess_exec(
                '/usr/bin/sudo',
                '/usr/sbin/apachectl', 'graceful',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            print(f'stdout: {stdout}, stderr: {stderr}')
        except FileNotFoundError as e:
            print(f'Apache not reloaded: {e}')
            return False
        return True

    async def _create_nginx_conf(self):
        cursor = self._db_conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()

        env = Environment(
            loader=FileSystemLoader(Path(self._options.nginx_tpl_file).parent),
            autoescape=False
        )
        try:
            template = env.get_template(
                Path(self._options.nginx_tpl_file).name)
        except TemplateNotFound as e:
            _log.error(f'No NGINX template found: {e}')
            return False

        Path(self._options.nginx_conf_file).parent.mkdir(
            parents=True, exist_ok=True)

        with open(self._options.nginx_conf_file, "w") as f:
            f.write(template.render(clients=clients))

        try:
            proc = await asyncio.create_subprocess_exec(
                '/usr/bin/sudo',
                '/bin/systemctl', 'reload', 'nginx',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            print(f'stdout: {stdout}, stderr: {stderr}')
        except FileNotFoundError as e:
            print(f'NGINX not reloaded: {e}')
            return False
        return True
