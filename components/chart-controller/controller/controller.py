import subprocess
import json

import os


def refresh_charts(branch='master'):

    cwd = os.getcwd()
    try:
        charts_url = os.environ['CHARTS_URL']
    except Exception:
        charts_url = 'https://github.com/scaleoutsystems/charts/archive/{}.zip'.format(branch)

    status = subprocess.run('rm -rf charts-{}'.format(branch).split(' '), cwd=cwd)
    status = subprocess.run('wget -O {}.zip {}'.format(branch, charts_url).split(' '), cwd=cwd)
    status = subprocess.run('unzip {}.zip'.format(branch).split(' '),cwd=cwd)


class Controller:

    def __init__(self, cwd):
        self.cwd = cwd
        self.branch = os.environ['BRANCH']
        self.default_args = ['helm']
        pass

    def deploy(self, options):
        extras = ''
        """
        try:
            minio = ' --set service.minio=' + str(options['minio_port'])
            extras = extras + minio
        except KeyError as e:
            print("could not get minioport!")
        try:
            controller = ' --set service.controller=' + str(options['controller_port'])
            extras = extras + controller
        except KeyError as e:
            print("could not get controllerport")
            pass
        try:
            user = ' --set alliance.user=' + str(options['user'])
            extras = extras + user
        except KeyError as e:
            print("could not get user")
            pass
        try:
            project = ' --set alliance.project=' + str(options['project'])
            extras = extras + project
        except KeyError as e:
            print("could not get project")
            pass
        try:
            apiUrl = ' --set alliance.apiUrl=' + str(options['api_url'])
            extras = extras + apiUrl
        except KeyError as e:
            print("could not get apiUrl")
            pass
        """

        for key in options:
            extras = extras + ' --set {}={}'.format(key, options[key])

        refresh_charts(self.branch)

        args = 'helm install {release} charts-{branch}/scaleout/{chart}{extras}'.format(release=options['release'],
                                                                                        branch=self.branch,
                                                                                        chart=options['chart'],
                                                                                        extras=extras).split(' ')
        print(args, flush=True)
        #return True
        status = subprocess.run(args, cwd=self.cwd)
        #status = True
        return json.dumps({'helm': {'command': args, 'cwd': str(self.cwd), 'status': str(status)}})

    def delete(self, options):
        args = 'helm delete {release}'.format(release=options['release']).split(' ')
        status = subprocess.run(args, cwd=self.cwd)
        return json.dumps({'helm': {'command': args, 'cwd': str(self.cwd), 'status': str(status)}})

    def update(self, options, chart):
        pass
