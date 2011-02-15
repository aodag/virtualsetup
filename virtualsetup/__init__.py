import pkg_resources
import site
import os
import tempfile
import shutil
import sys

def easy_install(project_name, dest):
    results = []
    tmp = tempfile.mkdtemp()
    try:
        args = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'easy_install'), '-mUNxd', tmp, project_name
        args += (dict(os.environ, PYTHONPATH=tmp),)
        os.spawnle(os.P_WAIT, sys.executable, sys.executable, *args)
        env = pkg_resources.Environment([tmp])
        for d in env:
            dist = env[d][0]
            newloc = os.path.join(dest, os.path.basename(dist.location))
            print 'move %s to %s' % (dist.location, newloc)
            if os.path.isdir(newloc):
                shutil.rmtree(newloc)
            os.rename(dist.location, newloc)
            results.append(pkg_resources.Environment([newloc])[dist.project_name][0])
        return results
    finally:
        shutil.rmtree(tmp)
    

    

def develop(packages_dir, env):
    if 'VIRTUAL_ENV' not in os.environ:
        print >> os.stderr, "use virtualenv"
        sys.exit()
    ws = pkg_resources.WorkingSet()

    if not os.path.isdir(packages_dir):
        os.mkdir(packages_dir)

    pth = os.path.join(os.environ['VIRTUAL_ENV'], 'lib', 'python2.6', 'site-packages', 'flexenv.pth')

    develop_path = os.getcwd()
    develop_env = pkg_resources.Environment(search_path=[develop_path])

    dists = []
    for x in develop_env:
        for dist in develop_env[x]:
            dists.extend(_resolve_requires(dist, env, packages_dir, ws))

    print 'create pth : %s ' % pth
    with open(pth, "wb") as f:
        for dist in dists:
            if dist is None:
                continue 
            f.write(dist.location)
            f.write('\n')

def _resolve_requires(dist, env, packagesdir, ws):
    results = []
    for req in dist.requires():
        exists_dist = ws.find(req)
        if exists_dist:
            print '%s is already exists %s' % (exists_dist.project_name, exists_dist.location)
            for exists_req in exists_dist.requires():
                exists_req_dist = ws.find(exists_req)
                if exists_req_dist is None:
                    results.extend(easy_install(exists_req.project_name, packagesdir))

                results.append(exists_req_dist)
            results.append(exists_dist)
            continue

        req_dists = env[req.project_name]
        if len(req_dists) == 0:
            print "%s needs %s" % (dist.project_name, req.project_name,)
            if req.project_name not in ('distribute', 'setuptools'):
                results.extend(easy_install(req.project_name, packagesdir))
                env.scan()
            req_dists = env[req.project_name]
        for req_dist in req_dists:
            results.extend(_resolve_requires(req_dist, env, packagesdir, ws))
            results.append(req_dist)

    return results
    


PACKAGES_DIR = '.virtualsetup'

def main():
    env = pkg_resources.Environment(search_path=[PACKAGES_DIR])
    develop(PACKAGES_DIR, env)

