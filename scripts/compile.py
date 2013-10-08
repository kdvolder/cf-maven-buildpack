#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from build_pack_utils import Builder


def maven_command(cfg):
    mvnCmd = cfg.get('MAVEN_BUILD_COMMAND', 'package')
    mvn = os.path.join(cfg['BUILD_DIR'], 'bin', 'mvn')
    return [mvn, mvnCmd]

def log_run(cmd, retcode, stdout, stderr):
    print 'Comand [%s] failed with [%d]' % (' '.join(cmd), retcode)
    print 'STDOUT:'
    print stdout
    print 'STDERR:'
    print stderr
    raise RuntimeError('Script Failure')


if __name__ == '__main__':
    (Builder()
        .configure()
            .default_config()
            .user_config()
            .done()
        .install()
            .package('JAVA')
            .package('MAVEN')
            .done()
        .run()
            .command(maven_command)
            .environment_variable()
                .name('JAVA_HOME')
                .value('JAVA_INSTALL_PATH')
            .with_shell()
            .on_finish(log_run)
            .done()
        .create_start_script()
            .environment_variable()
                .export()
                .name('JAVA_HOME')
                .value('JAVA_INSTALL_PATH')
            .environment_variable()
                .export()
                .name('M2_HOME')
                .value('MAVEN_INSTALL_PATH')
            .command()
                .run('mvn')
                .with_argument('tomcat:run')
            .write())
