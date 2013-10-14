from fabric.api import env, roles, run, sudo, execute, local, put, get
from fabric.context_managers import settings

# Customize these settings
env.user = 'USER'
env.roledefs = {
    'linode': [  # shameless plug...
        'your.host.here.com',
    ],
}
local_path = ''  # Path to app dir on local box
remote_path = ''  # Path to app dir on remote box
log_dir = ''  # Remote path for logs


def deploy():
    bundle_app()
    env.roles = ['linode']  # Change this if you change the name in roledefs
    execute('deploy_linode')
    # You can add a second roledef with another list of hosts, then define
    # another function like deploy_linode to do special instructions...


def bundle_app():
    local('mrt bundle bundle.tar.gz')


@roles('linode')
def deploy_linode():
    with settings(warn_only=True):
        # Check for remote dir
        run('mkdir %s' % remote_path)

    # TODO: use restart instead of stop and start to lower downtime
    with settings(warn_only=True):
        run('cd %(remote_path)s; forever stop main.js' %
            {'remote_path': remote_path})

    run('cd %(remote_path)s; rm -rf *' % {'remote_path': remote_path})

    put('%s/bundle.tar.gz' % local_path, remote_path)

    run('cd %(remote_path)s; tar -xmf bundle.tar.gz' %
        {'remote_path': remote_path})
    run('cd %(remote_path)s; mv bundle/* ./' % {'remote_path': remote_path})

    run('cd %(remote_path)s; rm -rf bundle' % {'remote_path': remote_path})
    run('cd %(remote_path)s; rm bundle.tar.gz' % {'remote_path': remote_path})

    # Recompile fibers for remote box
    run('cd %(remote_path)s/server; rm -rf node_modules/fibers' %
        {'remote_path': remote_path})
    sudo('cd %(remote_path)s/server; npm install fibers@1.0.0 --production' %
         {'remote_path': remote_path})

    # Recompile xml2js for remote box.
    # This can be removed, changed, or repeated as needed
    run('cd %(remote_path)s; mkdir node_modules' %
        {'remote_path': remote_path})
    sudo('cd %(remote_path)s/; npm install xml2js' %
         {'remote_path': remote_path})

    start_app()


@roles('linode')
def start_app():
    run('cd %(remote_path)s; export MONGO_URL="mongodb://localhost:27017/\
        meteor"; export ROOT_URL="https://YOURURL HERE"; \
        export PORT="3000"; forever start -l %(log_dir)s/forever.log \
        -a -o %(log_dir)s/out.log -e %(log_dir)s/err.log main.js' %
        {'remote_path': remote_path, 'log_dir': log_dir})


@roles('linode')
def stop_app():
    run('cd %(remote_path)s; forever stop main.js' %
        {'remote_path': remote_path})


@roles('linode')
def restart_app():
    run('cd %(remote_path)s; forever restart main.js' %
        {'remote_path': remote_path})


@roles('linode')
def get_mongo_dump():
    run('cd %(remote_path)s; mongodump' % {'remote_path': remote_path})
    run('cd %(remote_path)s; tar -cvf dump.tar.gz dump' %
        {'remote_path': remote_path})
    get('%s/dump.tar.gz' % remote_path, local_path)
