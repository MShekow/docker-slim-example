# Docker Slim example

Demonstrates how docker-slim can be used in GitLab CI to make images more secure and reduce their size.
See [this blog post](https://www.augmentedmind.de/2022/02/06/reduce-docker-image-size/) for more details.

This example consists of a simple dockerized Python web server (see code in the `service` folder). It uses the rather
large `python:3.x` (_non_-slim) image, to better illustrate how many unused files an image can contain.

In the pipeline, the `test-diagnostic-output` job prints how much the image was optimized, and which files were thrown
away. The latter is a very long list, which is why it is put into a file that you can download as job artefact.
