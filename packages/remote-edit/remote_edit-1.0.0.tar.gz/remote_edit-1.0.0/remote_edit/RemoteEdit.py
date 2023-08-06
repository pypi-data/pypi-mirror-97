from pyngrok import ngrok
import argparse
from flaskcode.cli import create_flask_app


class RemoteEdit:

    def __init__(self, path, port, username, password):
        self.path = path
        self.port = port
        self.username = username
        self.password = password

    def ngrok_connect(self):
        ngrok.connect(self.port)
        tunnels = ngrok.get_tunnels()
        public_url = tunnels[0].public_url
        print("Please use this URL: {url}".format(url= public_url))
        ngrok_process = ngrok.get_ngrok_process()

        app = create_flask_app(username=self.username, password=self.password)
        app.config['FLASKCODE_RESOURCE_BASEPATH'] = self.path
        app.config['FLASKCODE_EDITOR_THEME'] = "vs-dark"
        app.run(host="0.0.0.0", port=5001, debug=False)
        try:
            # Block until CTRL-C or some other terminating event
            ngrok_process.proc.wait()
        except KeyboardInterrupt:
            print(" Shutting down server.")
            ngrok.kill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "--Path", help="Show Path")
    parser.add_argument("--o", "--Output", help="Show Output")
    parser.add_argument("--username", "--Username", help="Username", default=None)
    parser.add_argument("--password", "--Password", help="Password", default=None)
    parser.add_argument("--port", "--port", default=5001, help="Port")
    args = vars(parser.parse_args())
    path = args['path']
    port = args['port']
    username = args['username']
    password = args['password']
    remote_edit = RemoteEdit(path, port, username, password)
    remote_edit.ngrok_connect()
