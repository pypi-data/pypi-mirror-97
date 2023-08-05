====================
Images API Reference
====================


.. currentmodule:: neuro_sdk


Images
======

.. class:: Images

   Docker image subsystem.

   Used for pushing docker images onto Neuro docker registry for later usage by
   :meth:`Jobs.run` and pulling these images back to local docker.

   .. comethod:: push(local: LocalImage, \
                      remote: Optional[RemoteImage] = None, \
                      *, \
                      progress: Optional[AbstractDockerImageProgress] = None, \
                 ) -> RemoteImage


      Push *local* docker image to *remote* side.

      :param LocalImage local: a spec of local docker image (e.g. created by ``docker
                               build``) for pushing on Neuro Registry.

      :param RemoteImage remote: a spec for remote image on Neuro
                                 Registry. Calculated from *local* image automatically
                                 if ``None`` (default).

      :param AbstractDockerImageProgress progress:

         a callback interface for reporting pushing progress, ``None`` for no progress
         report (default).

      :return: *remote* image if explicitly specified, calculated remote image if
               *remote* is ``None`` (:class:`RemoteImage`)


   .. comethod:: pull(remote: Optional[RemoteImage] = None, \
                      local: LocalImage, \
                      *, \
                      progress: Optional[AbstractDockerImageProgress] = None, \
                 ) -> RemoteImage


      Pull *remote* image from Neuro registry to *local* docker side.

      :param RemoteImage remote: a spec for remote image on Neuro
                                 registry.

      :param LocalImage local: a spec of local docker image to pull. Calculated from
                                 *remote* image automatically if ``None`` (default).


      :param AbstractDockerImageProgress progress:

         a callback interface for reporting pulling progress, ``None`` for no progress
         report (default).

      :return: *local* image if explicitly specified, calculated remote image if
               *local* is ``None`` (:class:`LocalImage`)

   .. comethod:: digest(image: RemoteImage) -> str

      Get digest of an image in Neuro registry.

      :param RemoteImage image: a spec for remote image on Neuro
                                 registry.


      :return: string representing image digest

   .. comethod:: rm(image: RemoteImage, digest: str) -> str

      Delete remote image specified by given reference and digest from Neuro registry.

      :param RemoteImage image: a spec for remote image on Neuro
                                 registry.

      :param str digest: remote image digest, which can be obtained via `digest` method.



   .. comethod:: ls() -> List[RemoteImage]

      List images on Neuro registry available to the user.

      :return: list of remote images not including tags
               (:class:`List[RemoteImage]`)


   .. comethod:: tags(image: RemoteImage) -> List[RemoteImage]

      List image references with tags for the specified remote *image*.

      :param RemoteImage image: a spec for remote image without tag on Neuro
                                registry.

      :return: list of remote images with tags (:class:`List[RemoteImage]`)


   .. comethod:: size(image: RemoteImage) -> int

      Return image size.

      :param RemoteImage image: a spec for remote image with tag on Neuro
                                registry.

      :return: remote image size in bytes


   .. comethod:: tag_info(image: RemoteImage) -> Tag

      Return info about specified tag.

      :param RemoteImage image: a spec for remote image with tag on Neuro
                                registry.

      :return: tag information (name and size) (:class:`Tag`)


AbstractDockerImageProgress
===========================

.. class:: AbstractDockerImageProgress

   Base class for image operations progress, e.g. :meth:`Images.pull` and
   :meth:`Images.push`. Inherited from :class:`abc.ABC`.

   .. method:: pull(data: ImageProgressPull) -> None

      Pulling image from remote Neuro registry to local Docker is started.

      :param ImageProgressPull data: additional data, e.g. local and remote image
                                     objects.


   .. method:: push(data: ImageProgressPush) -> None

      Pushing image from local Docker to remote Neuro registry is started.

      :param ImageProgressPush data: additional data, e.g. local and remote image
                                     objects.

   .. method:: step(data: ImageProgressStep) -> None

      Next step in image transfer is performed.

      :param ImageProgressStep data: additional data, e.g. image layer id and progress
                                     report.

ImageProgressPull
=================

.. class:: ImageProgressPull

   *Read-only* :class:`~dataclasses.dataclass` for pulling operation report.

   .. attribute:: src

      Source image, :class:`RemoteImage` instance.

   .. attribute:: dst

      Destination image, :class:`LocalImage` instance.


.. class:: ImageProgressPush

   *Read-only* :class:`~dataclasses.dataclass` for pulling operation report.

   .. attribute:: src

      Source image, :class:`LocalImage` instance.

   .. attribute:: dst

      Destination image, :class:`RemoteImage` instance.


.. class:: ImageProgressStep

   *Read-only* :class:`~dataclasses.dataclass` for push/pull progress step.

   .. attribute:: layer_id

      Image layer, :class:`str`.

   .. attribute:: message

      Progress message, :class:`str`.


LocalImage
==========

.. class:: LocalImage

   *Read-only* :class:`~dataclasses.dataclass` for describing *image* in local Docker
   system.

   .. attribute:: name

      Image name, :class:`str`.

   .. attribute:: tag

      Image tag (:class:`str`), ``None`` if the tag is omitted (implicit ``latest``
      tag).


RemoteImage
===========

.. class:: RemoteImage

   *Read-only* :class:`~dataclasses.dataclass` for describing *image* in remote
   registry (Neuro Platform hosted or other registries like DockerHub_).

   .. attribute:: name

      Image name, :class:`str`.

   .. attribute:: tag

      Image tag (:class:`str`), ``None`` if the tag is omitted (implicit ``latest``
      tag).

   .. attribute:: owner

      User name (:class:`str`) of a person who manages this image.

      Public DockerHub_ images (e.g. ``"ubuntu:latest"``) have no *owner*, the attribute
      is ``None``.

   .. attribute:: registry

      Host name for images hosted on Neuro Registry (:class:`str`), ``None`` for
      other registries like DockerHub_.

    .. method:: as_docker_url(with_scheme: bool = False) -> str

      URL that can be used to reference this image with Docker.

      :param bool with_scheme: if set to True, returned URL includes scheme (`https://`), otherwise (default behavior) - scheme is omitted.

    .. method:: with_tag(tag: bool) -> RemoteImage

       Creates a new reference to remote image with *tag*.

       :param str tag: new tag

       :return: remote image with *tag*

    .. py:classmethod:: new_neuro_image(name: str, registry: str, *, owner: str, cluster_name: str, tag: Optional[str] = None) -> RemoteImage

        Create a new instance referring to an image hosted on Neuro Platform.

      :param str name: name of the image

      :param str registry: registry where the image is located

      :param str owner: image owner name

      :param str cluster_name: name of the cluster

      :param str tag: image tag

    .. py:classmethod:: new_external_image(name: str, registry: Optional[str] = None, *, tag: Optional[str] = None) -> RemoteImage

        Create a new instance referring to an image hosted on an external registry (e.g. DockerHub_).

      :param str name: name of the image

      :param str registry: registry where the image is located

      :param str tag: image tag


.. class:: Tag

   *Read-only* :class:`~dataclasses.dataclass` for tag information.

   .. attribute:: name

      Tag name, :class:`str`.

   .. attribute:: size

      Tag size in bytes, :class:`int`.


.. _DockerHub: https://hub.docker.com
