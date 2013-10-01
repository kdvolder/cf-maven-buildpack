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

from build_pack_utils import CloudFoundryUtil
from build_pack_utils import CloudFoundryInstaller

if __name__ == '__main__':
    # Do this first.  Sets up STDOUT and gives us access to basic info
    #  like build directory, cache directory, memory limit, temp dir,
    #  and build pack directory.  Also has utilities for loading JSON
    #  configuration files.
    cf = CloudFoundryUtil()

    # Load default and user config, merge the two
    default_cfg = cf.load_json_config_file_from(cf.BP_DIR, 'defaults.json')
    user_cfg = cf.load_json_config_file_from(cf.BUILD_DIR, 'config.json')
    if user_cfg:
        print 'Custom configuration found, overriding default options'
        cfg = dict(default_cfg.items() + user_config.items())
    else:
        cfg = default_cfg
   
    # Create our installer.  This is a utility that helps us download
    #  install required packages.  In addition, it performs basic caching
    #  and attempts to be smart about downloading a file or using the
    #  cached version.
    installer = CloudFoundryInstaller(cf, cfg)

    # Download & Install Java.  By default, installed to the build pack
    #  directory, but can be customized by setting '_PACKAGE_INSTALL_DIR'
    #  key in the configuration.
    java_install_dir = installer.install_binary('JAVA')

    # Download & Install Maven.  Same as Java.
    maven_install_dir = installer.install_binary('MAVEN')

    # Run Maven to compile and build
    #  Run default command 'mvn package' or custom command
    if 'MAVEN_BUILD_COMMAND' in cfg.keys():
        parts = cfg['MAVEN_BUILD_COMMAND'].split(' ')
        command = parts[0]
        args = parts[1:]
    else:
        command = 'mvn'
        args = ('package',)
    CloudFoundryRunner.run_from_directory(maven_install_dir, 
                                          command, args)

    # Create Run Script
    #  Default -> Look at command in manifest
    #  Config -> MVN_RUN_COMMAND

