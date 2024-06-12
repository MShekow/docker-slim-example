# Docker Slim example

Demonstrates how the [Slim toolkit](https://github.com/slimtoolkit/slim) can be used in GitHub Actions to make images more secure and reduce their size.
See [this blog post](https://www.augmentedmind.de/2024/06/11/optimize-docker-image-size/) for more details.

This example consists of a simple dockerized Python web server (see code in the `service` folder). It uses the rather large `python:3.x` (_non_-slim) image, to better illustrate how many unused files an image can contain.

In the pipeline, the `Build slim image` step of the first job prints how much the image was optimized, e.g.:
`cmd=build info=results size.original='1.1 GB' size.optimized='104 MB' status='MINIFIED' by='10.73X' `

The `Print removed files` step of the first job prints which files were removed in the slim image, compared to the fat image. It is a very long list, which is why it is put into a file that you can download as job artefact.
