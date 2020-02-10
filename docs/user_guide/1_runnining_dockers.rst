Running dockers
================

Our Docker images have some Shadow-specific configurations to allow running with Nvidia, access to host-connected hardware etc.; this page is intended to record the Shadow Docker container create/run procedure.

In all of the examples given below, docker create is interchangeable with docker run; the latter will simple create and then start a container.

Common Arguments
---------------------
The first set of arguments is common to all scenarios:

.. prompt:: bash $

   docker run -it --security-opt seccomp=unconfined --network=host --pid=host --privileged -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -v /tmp/.X11-unix:/tmp/.X11-unix:rw [docker_repository]/[docker_image]:[docker_image_tag] [your_command]