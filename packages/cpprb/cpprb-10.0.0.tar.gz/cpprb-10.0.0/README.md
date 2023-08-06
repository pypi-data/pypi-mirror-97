![img](https://img.shields.io/gitlab/pipeline/ymd_h/cpprb.svg)
![img](https://img.shields.io/pypi/v/cpprb.svg)
![img](https://img.shields.io/pypi/l/cpprb.svg)
![img](https://img.shields.io/pypi/status/cpprb.svg)
[![img](https://gitlab.com/ymd_h/cpprb/badges/master/coverage.svg)](https://ymd_h.gitlab.io/cpprb/coverage/)

![img](./site/static/images/favicon.png)


# Overview

cpprb is a python ([CPython](https://github.com/python/cpython/tree/master/Python)) module providing replay buffer classes for
reinforcement learning.

Major target users are researchers and library developers.

You can build your own reinforcement learning algorithms together with
your favorite deep learning library (e.g. [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/)).

cpprb forcuses speed, flexibility, and memory efficiency.

By utilizing [Cython](https://cython.org/), complicated calculations (e.g. segment tree for
prioritized experience replay) are offloaded onto C++.
(The name cpprb comes from "C++ Replay Buffer".)

In terms of API, initially cpprb referred to [OpenAI Baselines](https://github.com/openai/baselines)'
implementation. In the current version, cpprb has much more
flexibility. Any [NumPy](https://numpy.org/) compatible types of any numbers of values can
be stored (as long as memory capacity is sufficient). For example, you
can store the next action and the next next observation, too.


# Installation

cpprb requires following softwares before installation.

-   C++17 compiler (for installation from source)
    -   [GCC](https://gcc.gnu.org/) (maybe 7.2 and newer)
    -   [Visual Studio](https://visualstudio.microsoft.com/) (2017 Enterprise is fine)
-   Python 3
-   pip

Cuurently, [clang](https://clang.llvm.org/), which is a default Xcode C/C++ compiler at Apple macOS,
cannot compile cpprb.

If you are macOS user, you need to install GCC and set environment values
of `CC` and `CXX` to `g++`, or just use virtual environment (e.g. [Docker](https://www.docker.com/)).

Step by step installation is described [here](https://ymd_h.gitlab.io/cpprb/installation/install_on_macos/).

Additionally, here are user's good feedbacks for installation at [macOS](https://github.com/keiohta/tf2rl/issues/75) and [Ubuntu](https://gitlab.com/ymd_h/cpprb/issues/73).
(Thanks!)


## Install from [PyPI](https://pypi.org/) (Recommended)

The following command installs cpprb together with other dependancies.

    pip install cpprb

Depending on your environment, you might need `sudo` or `--user` flag
for installation.

On supported platflorms (Linux x86-64 and Windows amd64), binary
packages are hosted on PyPI can be used, so that you don't need C++ compiler.

If you have trouble to install from binary, you can fall back to
source installation to passk `--no-binary` option to the above pip command.

Currently, no other platforms, such as macOS, and 32bit or
arm-architectured Linux and Windows, cannot install from binary, and
need to compile by yourself. Please be patient, we will plan to
support wider platforms in future.


## Install from source code

First, download source code manually or clone the repository;

    git clone https://gitlab.com/ymd_h/cpprb.git

Then you can install same way;

    cd cpprb
    pip install .

For this installation, you need to convert extended Python (.pyx) to
C++ (.cpp) during installation, it takes longer time than installation
from PyPI.


# Usage


## Basic Usage

Basic usage is following step;

1.  Create replay buffer (`ReplayBuffer.__init__`)
2.  Add transitions (`ReplayBuffer.add`)
    1.  Reset at episode end (`ReplayBuffer.on_episode_end`)
3.  Sample transitions (`ReplayBuffer.sample`)


## Example Code

Here is a simple example for storing standard environment (aka. `"obs"`,
`"act"`, `"rew"`, `"next_obs"`, and `"done"`).

    from cpprb import ReplayBuffer
    
    buffer_size = 256
    obs_shape = 3
    act_dim = 1
    rb = ReplayBuffer(buffer_size,
    		  env_dict ={"obs": {"shape": obs_shape},
    			     "act": {"shape": act_dim},
    			     "rew": {},
    			     "next_obs": {"shape": obs_shape},
    			     "done": {}})
    
    obs = np.ones(shape=(obs_shape))
    act = np.ones(shape=(act_dim))
    rew = 0
    next_obs = np.ones(shape=(obs_shape))
    done = 0
    
    for i in range(500):
        rb.add(obs=obs,act=act,rew=rew,next_obs=next_obs,done=done)
    
        if done:
    	# Together with resetting environment, call ReplayBuffer.on_episode_end()
    	rb.on_episode_end()
    
    batch_size = 32
    sample = rb.sample(batch_size)
    # sample is a dictionary whose keys are 'obs', 'act', 'rew', 'next_obs', and 'done'


## Construction Parameters

(See also [API reference](https://ymd_h.gitlab.io/cpprb/api/api/cpprb.ReplayBuffer.html))

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Name</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Optional</th>
<th scope="col" class="org-left">Discription</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">`size`</td>
<td class="org-left">`int`</td>
<td class="org-left">No</td>
<td class="org-left">Buffer size</td>
</tr>


<tr>
<td class="org-left">`env_dict`</td>
<td class="org-left">`dict`</td>
<td class="org-left">Yes (but unusable)</td>
<td class="org-left">Environment definition (See [here](https://ymd_h.gitlab.io/cpprb/features/flexible_environment/))</td>
</tr>


<tr>
<td class="org-left">`next_of`</td>
<td class="org-left">`str` or array-like of `str`</td>
<td class="org-left">Yes</td>
<td class="org-left">Memory compression (See [here](https://ymd_h.gitlab.io/cpprb/features/memory_compression/))</td>
</tr>


<tr>
<td class="org-left">`stack_compress`</td>
<td class="org-left">`str` or array-like of `str`</td>
<td class="org-left">Yes</td>
<td class="org-left">Memory compression (See [here](https://ymd_h.gitlab.io/cpprb/features/memory_compression/))</td>
</tr>


<tr>
<td class="org-left">`default_dtype`</td>
<td class="org-left">`numpy.dtype`</td>
<td class="org-left">Yes</td>
<td class="org-left">Fall back data type</td>
</tr>


<tr>
<td class="org-left">`Nstep`</td>
<td class="org-left">`dict`</td>
<td class="org-left">Yes</td>
<td class="org-left">Nstep configuration (See [here](https://ymd_h.gitlab.io/cpprb/features/nstep/))</td>
</tr>


<tr>
<td class="org-left">`mmap_prefix`</td>
<td class="org-left">`str`</td>
<td class="org-left">Yes</td>
<td class="org-left">mmap file prefix (See [here](https://ymd_h.gitlab.io/cpprb/features/mmap/))</td>
</tr>
</tbody>
</table>


## Notes

Flexible environment values are defined by `env_dict` when buffer
creation. The detail is described at [document](https://ymd_h.gitlab.io/cpprb/features/flexible_environment/).

Since stored values have flexible name, you have to pass to
`ReplayBuffer.add` member by keyword.


# Features

cpprb provides buffer classes for building following algorithms.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Algorithms</th>
<th scope="col" class="org-left">cpprb class</th>
<th scope="col" class="org-left">Paper</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Experience Replay</td>
<td class="org-left">`ReplayBuffer`</td>
<td class="org-left">[L. J. Lin](https://link.springer.com/article/10.1007/BF00992699)</td>
</tr>


<tr>
<td class="org-left">[Prioritized Experience Replay](https://ymd_h.gitlab.io/cpprb/features/per/)</td>
<td class="org-left">`PrioritizedReplayBuffer`</td>
<td class="org-left">[T. Schaul et. al.](https://arxiv.org/abs/1511.05952)</td>
</tr>


<tr>
<td class="org-left">[Multi-step (Nstep) Learning](https://ymd_h.gitlab.io/cpprb/features/nstep/)</td>
<td class="org-left">`ReplayBuffer`, `PrioritizedReplayBuffer`</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">[Multiprocess Learning (Ape-X)](https://ymd_h.gitlab.io/cpprb/features/ape-x/)</td>
<td class="org-left">`MPReplayBuffer` `MPPrioritizedReplayBuffer`</td>
<td class="org-left">[D. Horgan et. al.](https://arxiv.org/abs/1803.00933)</td>
</tr>
</tbody>
</table>

cpprb features and its usage are described at following pages:

-   [Flexible Environment](https://ymd_h.gitlab.io/cpprb/features/flexible_environment/)
-   [Multi-step add](https://ymd_h.gitlab.io/cpprb/features/multistep_add/)
-   [Prioritized Experience Replay](https://ymd_h.gitlab.io/cpprb/features/per/)
-   [Nstep Experience Replay](https://ymd_h.gitlab.io/cpprb/features/nstep/)
-   [Memory Compression](https://ymd_h.gitlab.io/cpprb/features/memory_compression/)
-   [Map Large Data on File](https://ymd_h.gitlab.io/cpprb/features/mmap/)
-   [Multiprocess Learning (Ape-X)](https://ymd_h.gitlab.io/cpprb/features/ape-x/)


# Contributing to cpprb

Any contribution are very welcome!


## Making Community Larger

Bigger commumity makes development more active and improve cpprb.

-   Star [GitLab repository](https://gitlab.com/ymd_h/cpprb) (and/or [GitHub Mirror](https://github.com/ymd-h/cpprb))
-   Publish your code using cpprb
-   Share this repository to your friend and/or followers.


## Q & A at Forum

When you have any problems or requests, you can check [Discussions on
GitHub.com](https://github.com/ymd-h/cpprb/discussions). If you still cannot find any information, you can post
your own.

We keep [issues on GitLab.com](https://gitlab.com/ymd_h/cpprb/issues) and users are still allowed to open
issues, however, we mainly use the place as development issue tracker.


## Merge Request (Pull Request)

cpprb follows local rules:

-   Branch Name
    -   "HotFix<sub>\*</sub>\*\*" for bug fix
    -   "Feature<sub>\*</sub>\*\*" for new feature implementation
-   docstring
    -   Must for external API
    -   [Numpy Style](https://numpydoc.readthedocs.io/en/latest/format.html)
-   Unit Test
    -   Put test code under "test/" directory
    -   Can test by `python -m unittest <Your Test Code>` command
    -   Continuous Integration on GitLab CI configured by `.gitlab-ci.yaml`
-   Open an issue and associate it to Merge Request

Step by step instruction for beginners is described at [here](https://ymd_h.gitlab.io/cpprb/contributing/merge_request).


# Links


## cpprb sites

-   [Project Site](https://ymd_h.gitlab.io/cpprb/)
    -   [Class Reference](https://ymd_h.gitlab.io/cpprb/api/)
    -   [Unit Test Coverage](https://ymd_h.gitlab.io/cpprb/coverage/)
-   [Main Repository](https://gitlab.com/ymd_h/cpprb)
-   [GitHub Mirror](https://github.com/ymd-h/cpprb)
-   [cpprb on PyPI](https://pypi.org/project/cpprb/)


## cpprb users' repositories

-   **[keiohta/TF2RL](https://github.com/keiohta/tf2rl):** TensorFlow2.x Reinforcement Learning


# Lisence

cpprb is available under MIT lisence.

    MIT License
    
    Copyright (c) 2020 Yamada Hiroyuki
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

