#!/usr/bin/env bash
# Download and install requirements for documentation auto-deployment.
#
# This script does the following:
#
# - Installs mkdocs under the current user.
# - Installs pymdown-extensions under the current user.
# - If the documentation-theme is not present under the current directory, downloads
#   and installs the latest tarball.
#
# In order to work, it needs the following environment variables defined:
#
# This script should be fetched from the master branch by any project opting
# into the documentation auto-deployment workflow.
#
# @license   http://opensource.org/licenses/BSD-3-Clause BSD-3-Clause
# @copyright Copyright (c) 2019-2020 Laminas Project (https://getlaminas.org)

SCRIPT_PATH="$(pwd)"

# Install mkdocs and required extensions.
pip install --user mkdocs
pip install --user pymdown-extensions

# Conditionally install documentation-theme.
if [[ ! -d "dotkernel-mkdoc-theme/theme" ]];then
    echo "Downloading documentation-theme..." ;
    mkdir -p dotkernel-mkdoc-theme ;
    curl -s -L https://github.com/dotkernel/documentation-theme/releases/latest |
        egrep -o '/dotkernel/documentation-theme/archive/[0-9]*\.[0-9]*\.[0-9]*\.tar\.gz' |
        head -n1 |
        wget -O documentation-theme.tgz --base=https://github.com/ -i - ;
    (
        cd dotkernel-mkdoc-theme ;
        tar xzf ../documentation-theme.tgz --strip-components=1 ;
    );
    echo "Finished downloading and installing documentation-theme" ;
fi

exit 0;
