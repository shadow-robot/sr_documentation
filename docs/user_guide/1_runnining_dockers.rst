Running dockers
================

Our Docker images have some Shadow-specific configurations to allow running with Nvidia, access to host-connected hardware etc.; this page is intended to record the Shadow Docker container create/run procedure.

In all of the examples given below, docker create is interchangeable with docker run; the latter will simple create and then start a container.

Prerequisites
---------------------
Our images have been migrated to AWS ECR therefore they require authentication with AWS server before pulling them. In order to authenticate you need to install AWS CLI v2. You can find instructions here: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

After installation you have to run (once): ``aws configure`` to setup your credentials. You can find your credentials from the Google apps AWS SSO icon if you select ```Command line or programmatic access``.

To authenticate for Public ECR repos such as dexterous hand images just run this command (it last 12 hours): ```aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/shadowrobot```

To authenticate for private repos: ```aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 080653068785.dkr.ecr.eu-west-2.amazonaws.com```



Common Arguments
---------------------
The first set of arguments is common to all scenarios:

.. prompt:: bash $

   docker run -it --security-opt seccomp=unconfined --network=host --pid=host --privileged -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -e XDG_RUNTIME_DIR=/run/user/1000 -v /tmp/.X11-unix:/tmp/.X11-unix:rw [docker_repository]/[docker_image]:[docker_image_tag] [your_command]

Where ``[your_command]`` is optional, but most likely terminator.

There arguments, environment variables and volumes enable things like graphical interfaces, and ensure normal ROS communication within a docker container.

Nvidia GPU Specific Arguments
---------------------

If you are using an Nvidia GPU, you need these additional arguments. Note “are using” an Nvidia GPU, not just “have” one; check by running nvidia-smi on your host. If it tells you about a GPU, you need these arguments. If it throws an error or doesn’t exist, you don’t.

.. prompt:: bash $

   --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all -e NVIDIA_VISIBLE_DEVICES=all

You must also specify the following custom command:

.. prompt:: bash $

   bash -c "echo /usr/local/lib/x86_64-linux-gnu | sudo tee /etc/ld.so.conf.d/glvnd.conf && sudo ldconfig && [your_command]"

Where ``[your_command]`` is optional, but most likely terminator.

Use-Case Specific Parameters
---------------------

Arguments
`````````````
The following argument sets and unlimited core dump file size, and is used whenever a container may be saving ROS logs for further analysis (including dump files):

.. prompt:: bash $

   --ulimit core=-1

Environment Variables
`````````````

Many of our images are intended for use with an ethercat interface, and allow the user to specify which host ethernet adaptor should be used as an ethercat interface via the following environment variable:

.. prompt:: bash $

   -e interface=enx5647929203

You may also wish to specify the ROS master URI, if using a multi-machine ROS setup:

.. prompt:: bash $

   -e ROS_MASTER_URI=http://localhost:11311

Volumes
`````````````

The following maps volumes to the container that allows input devices to be accessed from within the container, e.g. teleoperation control pedals:

.. prompt:: bash $

   -v /dev/input:/dev/input:rw -v /run/udev/data:/run/udev/data:rw

Examples
---------------------

Teleop
`````````````
For each of the below examples, shadow-teleop-cyberglove may be substituted with shadow-teleop-polhemus or shadow-teleop-haptx.

* Non-Nvidia:

.. prompt:: bash $

   docker run --name teleop_manual -it --security-opt seccomp=unconfined --network=host --pid=host --privileged --ulimit core=-1 -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -e XDG_RUNTIME_DIR=/run/user/1000 -e interface=enx5647929203 -e ROS_MASTER_URI=http://localhost:11311 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /dev/input:/dev/input:rw -v /run/udev/data:/run/udev/data:rw 080653068785.dkr.ecr.eu-west-2.amazonaws.com/shadow-teleop-cyberglove:noetic-night-build bash -c "terminator -T 'Teleop Server Container'"

* Nvidia:

.. prompt:: bash $

   docker run --name teleop_manual -it --security-opt seccomp=unconfined --network=host --pid=host --privileged --ulimit core=-1 --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all -e NVIDIA_VISIBLE_DEVICES=all -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -e XDG_RUNTIME_DIR=/run/user/1000 -e interface=enx5647929203 -e ROS_MASTER_URI=http://localhost:11311 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /dev/input:/dev/input:rw -v /run/udev/data:/run/udev/data:rw 080653068785.dkr.ecr.eu-west-2.amazonaws.com/shadow-teleop-cyberglove:noetic-night-build bash -c "echo /usr/local/lib/x86_64-linux-gnu | sudo tee /etc/ld.so.conf.d/glvnd.conf && sudo ldconfig && terminator -T 'Teleop Server Container'"

Dexterous Hand
`````````````

* Non-Nvidia:

.. prompt:: bash $

   docker run --name dexterous_hand -it --security-opt seccomp=unconfined --network=host --pid=host --privileged -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -e XDG_RUNTIME_DIR=/run/user/1000 -e interface=enx5647929203 -v /tmp/.X11-unix:/tmp/.X11-unix:rw public.ecr.aws/shadowrobot/dexterous-hand:noetic-night-build bash -c "terminator -T 'Dexterous Hand Container'"

* Nvidia:

.. prompt:: bash $

   docker run --name dexterous_hand -it --security-opt seccomp=unconfined --network=host --pid=host --privileged --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all -e NVIDIA_VISIBLE_DEVICES=all -e DISPLAY -e QT_X11_NO_MITSHM=1 -e LOCAL_USER_ID=$(id -u) -e XDG_RUNTIME_DIR=/run/user/1000 -e interface=enx5647929203 -v /tmp/.X11-unix:/tmp/.X11-unix:rw public.ecr.aws/shadowrobot/dexterous-hand:noetic-night-build bash -c "echo /usr/local/lib/x86_64-linux-gnu | sudo tee /etc/ld.so.conf.d/glvnd.conf && sudo ldconfig && terminator -T 'Dexterous Hand Container'"
