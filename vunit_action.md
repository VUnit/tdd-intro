# Continuous Integration with VUnit Action (Part 1/2)

The other week, [semiengineering.com](https://semiengineering.com) published an [article](https://semiengineering.com/open-source-verification/) on open-source verification. It had one, rather obvious, conclusion.

> Verification is required to answer the question, 'Do you trust the piece of hardware you received?'
>
> -- <cite>Neil Hand, director of marketing for design verification technology at Mentor, a Siemens Business</cite>

Despite being obvious, IP providers often make it hard to gain that trust.

> When you buy IP, you usually get a very simple verification environment. This enables you to run a few demo tests or check configurations. You do not usually get the entire verification environment.
>
> -- <cite>Olivera Stojanovic, senior verification manager for Vtool</cite>

This is not unique to commercial IPs. Our [study](https://larsasplund.github.io/github-facts/index.html) of VHDL projects on GitHub shows that less than half of all projects provide tests at all, and the trend is declining (see Figure 1).

<p align="center">
<img src="img/repositories_providing_tests.png"/>
<br>
<span class="caption">Figure 1. Repositories providing tests.</span>
</p>

So, what are the reasons for not providing tests with the IPs?

> With complex IPs, they don’t want to provide you with the verification environment, which is too complicated and potentially may provide insights that they might want to keep from you.
>
> -- <cite>Olivera Stojanovic, senior verification manager for Vtool</cite>

Keeping secrets is not a reason for not providing tests with public projects on GitHub, as everything is open/public. However, it can be complex to create a user-friendy online verification environment that clearly shows what has been tested and the status those tests. Thanks to [VUnit Action](https://github.com/marketplace/actions/vunit-action) this is now much simpler, as it provides a continuous integration flow with just 8 lines of code.

If you're not familiar with VUnit, the following reading will set you up for the VUnit Action described in the next section.

1. [Installing VUnit in 1 minute](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-lars-asplund/)
2. [Compiling your project in 1 minute](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-part-2-lars-asplund/)
3. [Fully automating your testbench with 5 lines of code](https://www.linkedin.com/pulse/vunit-best-value-initial-effort-part-3-lars-asplund/)

> NOTE: [VUnit Action](https://github.com/marketplace/actions/vunit-action) was donated to the VUnit organisation by [Marco Ieni](https://www.linkedin.com/in/marcoieni) and later enhanced by [Unai Martinez-Corral](https://github.com/umarcor).

See [vunit.github.io/vunit/ci: GitHub Actions](https://vunit.github.io/vunit/ci.html#github-actions).

# Continuous Integration with VUnit Action (Part 2/2)

The simple solution presented in Part 1 will get you started. Once you have that working there are a number of extra steps you can take to address the following issues:

* Improve the HTML visualization of the logs by using group/block decorators.
* Use a custom Docker image, to have additional dependencies pre-installed.
* Use a pytest script to handle multiple run.py scripts.
* Run the tests natively on the CI/CD environment (Ubuntu, Windows and/or macOS), instead of using a Docker container.

In this second post on continuous integration with VUnit, we will focus on other alternatives that allow more detailed customization.
