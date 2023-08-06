# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def get_pipeline_options(job_name, runner='PortableRunner', max_num_workers=1):
    """Build dispatcher options for profile_api."""
    project = 'LanGauge-INTERNAL'
    pipe_options = [
        '--project=' + project,
        '--runner=' + runner,
        "--job_endpoint=localhost:8099",
        '--environment_type=LOOPBACK',
        '--job_name=' + '%s-%s' % (project, job_name),
        '--max_num_workers=' + str(max_num_workers)
    ]
    return pipe_options