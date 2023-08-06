.. See LICENSE for details

Command Line Usage
==================

.. code-block:: bash

  $ repomanager --help
  usage: repomanager [-h] [--dir PATH] [--clean] [--yaml YAML] [--update]
                     [--patch] [--unpatch] [--verbose]
  
  Repository Manager
  
  optional arguments:
    --clean, -c           Removes all the repositories listed in repolist
    --dir PATH, -d PATH   PATH of the working directory
    --patch, -p           Applies patches to repositories which have their patch
                          field defined in repolist
    --unpatch, -r         Removes patches to repositories which have their patch
                          field defined in repolist
    --update, -u          Updates/Clones all the listed repositories in the
                          repolist
    --verbose             debug | info | warning | error
    --yaml YAML, -y YAML  A YAML file containing list of the repos
    -h, --help            show this help message and exit


.. code-block:: yaml

   
  <repo name>:
    url: <git patch>
    checkout: <branch/commitid/tag name>
    recursive: <boolean>
    patch:
      - ['path to root/submodule', 'path to patch1']
      - ['path to root/submodule', 'path to patch2']
    sparse: ['folder1', 'folder2', ... ]



Example yaml with checking out a particular commitid 
####################################################

.. code-block:: yaml

  caches_mmu:
    url: https://gitlab.com/shaktiproject/uncore/caches_mmu.git
    checkout: ade16d068b4b9bfe9392db9b5edafed4d78147ec
    recursive: False
    sparse: ['src/dcache', 'src/icache_1rw', 'LICENSE.iitm', 'README.md']

Example yaml with checking out a particular tag
################################################
.. code-block:: yaml

  caches_mmu:
    url: https://gitlab.com/shaktiproject/uncore/caches_mmu.git
    checkout: 8.2.0
    recursive: False
    sparse: ['src/dcache', 'src/icache_1rw', 'LICENSE.iitm', 'README.md']

Run repomanager
########################

.. code-block:: bash

  $ repomanager -y repolist.yaml -cup
