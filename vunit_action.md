# Continuous Integration with VUnit Action

The other week [semiengineering.com](https://semiengineering.com) published an [article](https://semiengineering.com/open-source-verification/) on open-source verification. It had one, rather obvious, conclusion.

> Verification is required to answer the question, 'Do you trust the piece of hardware you received?'
>
> -- <cite>Neil Hand, director of marketing for design verification technology at Mentor, a Siemens Business</cite>

Despite being obvious, IP providers often make it hard to gain that trust.

> When you buy IP, you usually get a very simple verification environment. This enables you to run a few demo tests or check configurations. You do not usually get the entire verification environment.
>
> -- <cite>Olivera Stojanovic, senior verification manager for Vtool</cite>

This is not unique to commercial IPs. Our [study](https://larsasplund.github.io/github-facts/index.html) of VHDL projects on GitHub shows that less than half of all projects provide tests at all and the trend is declining (see Figure 1).

<p align="center">
<img src="img/repositories_providing_tests.png"/>
<br>
<span class="caption">Figure 1. Repositories providing tests.</span>
</p>

So what are the reasons for not providing tests with the IPs?

> With complex IPs, they don’t want to provide you with the verification environment, which is too complicated and potentially may provide insights that they might want to keep from you.
>
> -- <cite>Olivera Stojanovic, senior verification manager for Vtool</cite>

Keeping secrets is not a reason for not providing tests with public projects on GitHub as everything is in the open. However, creating a user-friendy online verification environment that clearly shows what has been tested and the status those test can be complicated. Thanks to [VUnit Action](https://github.com/marketplace/actions/vunit-action) this is now much simpler. It was donated to the VUnit organisation by [Marco Ieni](https://www.linkedin.com/in/marcoieni) and provides a continuous integration flow with just 8 lines of code.

If you're not familiar with VUnit, the following reading will set you up for the VUnit Action described in the next section.

1. [Installing VUnit in 1 minute](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-lars-asplund/)
2. [Compiling your project in 1 minute](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-part-2-lars-asplund/)
3. [Fully automating your testbench with 5 lines of code](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-part-3-lars-asplund/)

# VUnit Action

GitHub allows you to create automated *workflows* for your repositories. These workflows consist of *actions* that you develop or reuse from the [GitHub marketplace](https://github.com/marketplace?type=actions). VUnit Action is one of those reusable actions and it helps you build a workflow for running your testbenches and presenting the result. Everything is run on GitHub's servers and the test result is continuously published on GitHub as the code evolves.

To use VUnit Action for your project you need to create a [YAML](https://en.wikipedia.org/wiki/YAML) file (some_name.yml) and place that in a directory named `.github\workflows` located directly under your project root. The YAML file contains the following piece of code.

``` yaml
name: VUnit Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: VUnit/vunit_action@v0.1.0
```

Whenever someone pushes code to the project or makes a pull request this workflow is triggered to run with Ubuntu. First, the code being pushed or provided in the pull request is checked out using the [checkout action](https://github.com/marketplace/actions/checkout). Second, the VUnit Action is triggered to run the `run.py` script located in the root of your repository. If the VUnit run script is located elsewhere you can append the following lines to the YAML file.

```yaml
with:
  run_file: path/to/vunit_run_script.py
```

To clearly show that you have tests up and running and build that trust with the user community, we recommend that you add the following line to your `README.md`. It will create a badge showing the latest status of you tests

``` markdown
[![](https://github.com/<user or organisation name>/<name of your repository>/workflows/VUnit%20Tests/badge.svg)](https://github.com/<user or organisation name>/<name of your repository>/actions)
```

Clicking that badge will take you to a list of workflow runs and then further to the results of those runs.

<p align="center">
<img src="img/flow.png"/>
<br>
<span class="caption">Figure 2. Presenting Test Results.</span>
</p>

The simple solution presented here will get you started. Once you have that working there are a number of extra steps you can take to address the following issues:

* Foo
* Bar

These issues will be the topic for our next post on continuous integration with VUnit action.