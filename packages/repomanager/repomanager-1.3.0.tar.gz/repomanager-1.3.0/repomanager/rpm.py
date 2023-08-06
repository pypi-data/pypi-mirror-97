import logging
import repomanager.utils as utils
import shutil
import sys
from repomanager.constants import *
from ruamel.yaml import YAML
from cerberus import Validator

yaml = YAML(typ="rt")
yaml.default_flow_style = False
yaml.allow_unicode = True
yaml.compact(seq_seq=False, seq_map=False)

logger = logging.getLogger(__name__)

schema_syn= """\
url:
    type: string
    required: True
    nullable: False
checkout:
    type: string
    required: True
    nullable: False
    default: master
recursive:
    type: boolean
    default: False
patch:
    type: list
    schema:
        type: list
        items: 
            - type: string
            - type: string
    default:
    nullable: True
sparse:
    type: list
    schema:
        type: string
    default:
    nullable: True
"""

class YamlValidator(Validator):
    def _check_with_filecheck(self, field, value):
        file_check = pwd + '/' + value
        if not os.path.isfile(file_check):
            self._error(field, 'File {0} not found'.format(file_check))
    def _check_with_dircheck(self, field, file_check):
        if not os.path.isdir(value):
            self._error(field, 'Dir {0} not found'.format(value))

def repoman(yaml_str, clean, update, patch, unpatch, work_dir):

    repo_yaml = yaml.load(yaml_str)

    schema = yaml.load(schema_syn)
    validator = YamlValidator(schema)
    validator.allow_unknown = False   

    cwd = os.getcwd()
    workdir = os.path.abspath(work_dir)
    os.makedirs(workdir, exist_ok=True)

    for name,field in repo_yaml.items():
        valid = validator.validate(field)
        if not valid:
            error_list = validator.errors
            for x in error_list:
                print('{0} [ {1} ] : {2}'.format(name,x, error_list[x]))
                exit(1)
        field = validator.normalized(field, schema)
        repo_path = workdir+'/'+name
        repo_url = field['url']
        repo_checkout = field['checkout']
        recursive = field['recursive']
        if recursive:
            recurse_cmd = '--recursive'
        else:
            recurse_cmd = ''

        if clean:
            shutil.rmtree(repo_path, ignore_errors=True, onerror=None)
            logger.info('Repo Path "{0}" Deleted'.format(name))

        if update:
            if os.path.isdir(repo_path):
                logger.info('Repo "{0}" already exists @ "{1}"'.format(name, repo_path))
                curr_commit, x = utils.shellCommand(r_currcommit).run(cwd=repo_path)
                exp_commit, x = utils.shellCommand(r_branchcommit.format(repo_checkout)).run(cwd=repo_path)
                # when we need to change commitid/branch/tags/release we first fetch everything
                # from the remote, reset the local copy and then checkout
                if curr_commit != exp_commit:
                    logger.info('Checking out "{0}" for Repo: "{1}"'.format(repo_checkout, name))
                    utils.shellCommand(r_fetch).run(cwd=repo_path) 
                    utils.shellCommand(r_reset).run(cwd=repo_path) 
                    utils.shellCommand(r_checkout.format(repo_checkout)).run(cwd=repo_path) 
                    if recursive:
                        utils.shellCommand('git submodule update --init --recursive').run(cwd=repo_path)
                else:
                    logger.info('Required Commit/Branch/Release already checked out')
            elif field['sparse'] is None:
                logger.info('Cloning "{0}" from URL "{1}"'.format(name, repo_url))
                utils.shellCommand(r_clone.format(repo_url, name, recurse_cmd, repo_checkout))\
                    .run(cwd=workdir)
            else:
                logger.info('Performing Sparse checkout')
                files = "\n".join(field['sparse'])
                cmd = r_sparseconfig.format(repo_url, files ,repo_checkout)
                os.makedirs(repo_path, exist_ok=True)
                utils.shellCommand(cmd).run(cwd=repo_path)


        if patch:
            if field['patch'] is not None:
                for p in field['patch']:
                    sm_path = os.path.join(repo_path,p[0])
                    pfile = os.path.abspath(p[1])
                    check, x = utils.shellCommand(r_checkpatch.format(pfile)).run(cwd=sm_path,
                            logging=False)
                    if check == '' and x == 0:
                        logger.info('Applying Patch "{0}" to "{0}"'.format(pfile, sm_path))
                        utils.shellCommand(r_applypatch.format(pfile)).run(cwd=sm_path, logging=False)
                    else:
                        logger.info('Patch "{0}" already applied or Cannot be applied to "{1}"'.format(pfile,sm_path))
        elif unpatch:
            if field['patch'] is not None:
                for p in field['patch']:
                    sm_path = os.path.join(repo_path,p[0])
                    pfile = os.path.abspath(p[1])
                    check, x = utils.shellCommand(r_checkunpatch.format(pfile)).run(cwd=sm_path)
                    if check == '' and x == 0:
                        logger.info('Reversing Patch "{0}" to "{0}"'.format(pfile, sm_path))
                        utils.shellCommand(r_applyunpatch.format(pfile)).run(cwd=sm_path)
                    else:
                        logger.info('Patch "{0}" already reversed or Cannot be reversed to "{1}"'.format(pfile,sm_path))


