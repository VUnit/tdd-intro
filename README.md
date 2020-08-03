<p align="center">
  <a title="Site" href="https://vunit.github.io"><img src="https://img.shields.io/website.svg?label=vunit.github.io&longCache=true&style=flat-square&url=http%3A%2F%2Fvunit.github.io%2Findex.html"></a><!--
  -->
  <a title="Join the chat at https://gitter.im/VUnit/vunit" href="https://gitter.im/VUnit/vunit"><img src="https://img.shields.io/badge/chat-on%20gitter-4db797.svg?longCache=true&style=flat-square&logo=gitter&logoColor=e8ecef"></a><!--
  -->
  <a title="'test' workflow status" href="https://github.com/VUnit/tdd-intro/actions?query=workflow%3Atest"><img alt="'test' workflow status" src="https://img.shields.io/github/workflow/status/VUnit/tdd-intro/test?longCache=true&style=flat-square&label=test&logo=github"></a>
</p>

# Introduction to test-driven development (TDD) for HDL designs

## Plain `run.py`

*TBW*

## Handling multiple `run.py` scripts with [pytest](https://pytest.org)

Ref [VUnit/vunit#663](https://github.com/VUnit/vunit/issues/663).

## Continuous Integration

### Procedures

Workflow [test.yml](.github/workflows/tests.yml) is a showcase of procedures to setup continuous integration using [GHDL](https://github.com/ghdl/ghdl) and [VUnit](https://github.com/VUnit/vunit) as a regression framework.

The entrypoint to all the jobs is the same pytest script ([test.py](test.py)), thus, all jobs are equivalent solutions. Tests called through pytest can be defined in any language: VUnit run.py scripts, bash/shell scripts, makefiles, etc.

NOTE: GitHub Actions workflows/jobs support two types of Actions: JavaScript (Linux, MacOS and/or Windows) and Docker (Linux only). See [docs.github.com: Actions > Creating actions > About-actions > Types of actions](https://docs.github.com/en/actions/creating-actions/about-actions#types-of-actions) for further info.

It is suggested for new users to clone/fork this template repository, and then remove the jobs they don't want to use. Since all are equivalent, using a single job is enough to have HDL designs tested. However, it might be useful to have designs tested on multiple different platforms.

#### lin-vunit

Uses Action [VUnit/vunit_action](https://github.com/VUnit/vunit_action), which is of type Docker, based on image `ghdl/vunit:llvm` (see [ghdl/docker](https://github.com/ghdl/docker#-vunit-1-job-6-images-triggered-after-workflow-buster)). It takes a single optional argument: the path to the `run.py`. See [VUnit/vunit_action: README.md](https://github.com/VUnit/vunit_action/blob/master/README.md) for further info.

This is the most straightforward solution, and the one with fastest startup.

#### lin-docker

Docker based job, which can be used in any CI system. An (optional) [Dockerfile](.github/Dockerfile) is used to add some packages on top of image `ghdl/vunit:llvm`. However, the same procedure can be used with any other image directly.

This is equivalent to *lin-vunit*, but it is slightly more verbose.

#### lin-setup

Uses Action [ghdl/setup-ghdl-ci](https://github.com/ghdl/setup-ghdl-ci) to install GHDL on the Ubuntu host/VM. Then, additional system packages and Python packages are installed explicitly.

Compared to previous approaches, in this case runtime dependencies are not pre-installed. As a result, startup is slightly slower.

#### win-setup

Uses Actions [ghdl/setup-ghdl-ci](https://github.com/ghdl/setup-ghdl-ci) and [msys2/setup-msys2](https://github.com/msys2/setup-msys2) to install latest *nightly* GHDL, other MSYS2 packages and Python packages in a *clean* MINGW64 environment.

This is the recommended approach to run tests on Windows. Action setup-msys2 caches installed packages/dependencies automatically.

#### win-stable

The *traditional* procedure of downloading a tarball/zipfile from GHDL's latest *stable* release. Additional Python packages are installed explicitly.

This is more verbose than the previous approach, but it's currently the only solution to use latest *stable* GHDL without building it from sources.

### Non-FLOSS simulators

*TBW*

## Repositories using VUnit for TDD

This is a non-exhaustive list of projects where VUnit is used for testing non-trivial HDL designs:

- [VUnit/vunit](https://github.com/VUnit/vunit)
- [ghdl/ghdl-cosim](https://github.com/ghdl/ghdl-cosim)
