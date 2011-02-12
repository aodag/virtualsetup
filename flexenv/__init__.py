import pkg_resources
import site
from argparse import ArgumentParser
import os



def list_versions(args, env):
    project_name = args.project_name
    dists = env[project_name]
    for dist in dists:
        print dist.version, dist.location
    
def apply(args, env):
    pth = os.path.join(args.virtualenv_dir, 'lib', 'python2.6', 'site-packages', 'flexenv.pth')
    locations = []
    project_name = args.project_name
    dists = env[project_name]
    for dist in dists:
        locations.append(dist.location)
        for req in dist.requires():
            req_dists = env[req.project_name] 
            for req_dist in req_dists:
                locations.append(req_dist.location)
    print "create %s" % pth
    with open(pth, "wb") as f:
        for loc in locations:
            f.write(loc)
            f.write('\n')


def develop(args, env):
    if 'VIRTUAL_ENV' not in os.environ:
        print >> os.stderr, "use virtualenv"
        sys.exit()

    pth = os.path.join(os.environ['VIRTUAL_ENV'], 'lib', 'python2.6', 'site-packages', 'flexenv.pth')
    develop_path = args.develop_path
    develop_env = pkg_resources.Environment(search_path=[develop_path])
    dists = []
    for x in develop_env:
        for dist in develop_env[x]:
            dists.extend(_resolve_requires(dist, env))

    print 'create pth : %s ' % pth
    with open(pth, "wb") as f:
        for dist in dists:
            f.write(dist.location)
            f.write('\n')

def _resolve_requires(dist, env):
    results = []
    for req in dist.requires():
        req_dists = env[req.project_name]
        for req_dist in req_dists:
            results.extend(_resolve_requires(req_dist, env))
            results.append(req_dist)

    return results
    


parser = ArgumentParser()
parser.add_argument('--packages-dir', action="store", 
    default=site.USER_SITE)
command_parser = parser.add_subparsers()
list_versions_parser = command_parser.add_parser('list')
list_versions_parser.add_argument('project_name', action="store")
list_versions_parser.set_defaults(func=list_versions)

develop_parser = command_parser.add_parser('develop')
develop_parser.add_argument('develop_path')
develop_parser.set_defaults(func=develop)

def main():
    args = parser.parse_args()
    env = pkg_resources.Environment(search_path=[args.packages_dir])
    if hasattr(args, 'func'):
        args.func(args, env)

