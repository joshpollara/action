import os
import subprocess

import repo_config as rc
import workflow_step_run


def run(state, config):
    args = config['args']

    terraform_version = state.workflow['terraform_version']

    terraform_bin_path = os.path.join('/usr', 'local', 'tf', 'versions', terraform_version, 'terraform')

    subprocess.check_call(['/install-terraform-version', terraform_version])

    env = config.get('env', {})

    if state.workflow['terragrunt']:
        cmd = ['terragrunt']
        env = env.copy()
        env['TERRAGRUNT_TFPATH'] = terraform_bin_path
    else:
        cmd = [terraform_bin_path]

    extra_args = config.get('extra_args', [])
    config = {
        'cmd': cmd + args + extra_args,
        'output_key': config.get('output_key'),
        'env': env,
        'realtime_logs': rc.get_realtime_logs(state.repo_config)
    }
    return workflow_step_run.run(state, config)
