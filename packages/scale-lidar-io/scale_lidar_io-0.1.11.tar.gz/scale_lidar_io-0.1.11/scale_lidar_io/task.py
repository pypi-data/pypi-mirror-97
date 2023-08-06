import os

import numpy as np
import requests
import ujson
from scaleapi import ScaleClient, Task

from .scene import LidarScene
from .helper import parse_xyz, parse_cuboid_frame, read_cuboid_points, get_api_client, get_default_template

class LidarAnnotationTask(Task):
    """Lidar annotation Task object
    """
    scene: LidarScene = None

    def __init__(self, param_dict, client):
        super(LidarAnnotationTask, self).__init__(param_dict, client)

    @staticmethod
    def from_scene(scene: LidarScene, template=None, client=None):
        """Load scene data and convert it into a LidarAnnotation Task format

        :param scene: Scene to load
        :type scene: LidarScene
        :param template: Template/payload to use get fetch the Scale API
        :type template: dict
        :param client: ScaleClient object, by default it will load your SCALE_API_KEY from you env vars and set a client automatically.
        :type client: scaleapi.ScaleClient
        :returns: LidarAnnotationTask object
        :rtype: LidarAnnotationTask

        """
        assert scene.public_url, 'No public URL on scene, please upload or save the scene first'

        # Get client using environ api key
        if client is None:
            client = get_api_client()

        # Starting with default template as params
        param_dict = get_default_template()

        # Load scene params
        scene_dict = scene.to_dict(scene.public_url)
        param_dict['attachments'] = scene_dict['frames']
        param_dict['attachment_type'] = 'json'

        if isinstance(template, dict):
            param_dict.update(template)

        elif isinstance(template, str):
            param_dict.update(ujson.load(open(template)))

        elif template is not None:
            raise AttributeError('Template error')

        return LidarAnnotationTask(param_dict, client)

    @staticmethod
    def from_id(task_id:str):
        """Get LidarAnnotation task from a task id

        :param task_id: Task id
        :type task_id: str
        :returns: LidarAnnotationTask object created based on the task id data
        :rtype: LidarAnnotationTask

        """
        task = get_api_client().fetch_task(task_id)
        return LidarAnnotationTask(task.param_dict, task.client)

    def get_annotations(self):
        """Get annotations/response from a completed LidarAnnotation task

        :returns: Annotations
        :rtype: dict

        """
        assert 'response' in self.param_dict, 'Task without response'
        url = self.param_dict['response']['annotations']['url']
        response = requests.get(url)
        return ujson.loads(response.text)

    def get_cuboid_positions_by_frame(self):
        """Get a list of each cuboid position in each frames (from a completed task)

        :returns: List of cuboids positions
        :rtype: list

        """
        annotations = self.get_annotations()
        return np.array([
            np.array([
                parse_xyz(p)
                for p in [c['position'] for c in frame['cuboids']]
            ])
            for frame in annotations
        ])

    def publish(self, task_type: str='lidarannotation'):
        """Publish/create a task, request Scale API with the LidarAnnotation data

        :param task_type: Task type to create, default ``lidarannotation``
        :type task_type: str
        :returns: Task object creation from the response of the API call
        :rtype: scaleapi.Task

        """
        task = self.client.create_task('lidarannotation', **self.param_dict)
        print('Task created: %s' % task)
        return task


class LidarTopDownTask(Task):
    scene: LidarScene = None

    def __init__(self, param_dict, client):
        super(LidarTopDownTask, self).__init__(param_dict, client)

    @staticmethod
    def from_scene(scene: LidarScene, template=None, client=None):
        """Load scene data and convert it into a LidarTopDown Task format

        :param scene: Scene to load
        :type scene: LidarScene
        :param template: Template/payload to use get fetch the Scale API
        :type template: dict
        :param client: ScaleClient object, by default it will load your SCALE_API_KEY from you env vars and set a client automatically.
        :type client: scaleapi.ScaleClient
        :returns: LidarTopDownTask object
        :rtype: LidarTopDownTask

        """
        assert scene.public_url, 'No public URL on scene, please upload or save the scene first'

        # Get client using environ api key
        if client is None:
            client = get_api_client()

        # Starting with default template as params
        param_dict = get_default_template()

        # Load scene params
        scene_dict = scene.to_dict(scene.public_url)
        param_dict['attachments'] = scene_dict['frames']
        param_dict['attachment_type'] = 'json'

        if isinstance(template, dict):
            param_dict.update(template)

        elif isinstance(template, str):
            param_dict.update(ujson.load(open(template)))

        elif template is not None:
            raise AttributeError('Template error')

        return LidarTopDownTask(param_dict, client)

    @staticmethod
    def from_id(task_id:str):
        """Get LidarTopDown task from a task id

        :param task_id: Task id
        :type task_id: str
        :returns: LidarTopDownTask object created based on the task id data
        :rtype: LidarTopDownTask

        """
        task = get_api_client().fetch_task(task_id)
        return LidarTopDownTask(task.param_dict, task.client)

    def publish(self, task_type: str='lidartopdown'):
        """Publish/create a task, request Scale API with the LidarTopDown data

        :param task_type: Task type to create, default ``lidartopdown``
        :type task_type: str
        :returns: Task object creation from the response of the API call
        :rtype: scaleapi.Task

        """
        task = self.client.create_task('lidartopdown', **self.param_dict)
        print('Task created: %s' % task)
        return task

class LidarSegmentationTask(Task):
    scene: LidarScene = None

    def __init__(self, param_dict, client):
        super(LidarSegmentation, self).__init__(param_dict, client)

    @staticmethod
    def from_scene(scene: LidarScene, template=None, client=None):
        """Load scene data and convert it into a LidarSegmentation Task format

        :param scene: Scene to load
        :type scene: LidarScene
        :param template: Template/payload to use get fetch the Scale API
        :type template: dict
        :param client: ScaleClient object, by default it will load your SCALE_API_KEY from you env vars and set a client automatically.
        :type client: scaleapi.ScaleClient
        :returns: LidarSegmentationTask object
        :rtype: LidarSegmentationTask

        """
        assert scene.public_url, 'No public URL on scene, please upload or save the scene first'

        # Get client using environ api key
        if client is None:
            client = get_api_client()

        # Starting with default template as params
        param_dict = get_default_template()

        # Load scene params
        scene_dict = scene.to_dict(scene.public_url)
        param_dict['attachments'] = scene_dict['frames']
        param_dict['attachment_type'] = 'json'

        if isinstance(template, dict):
            param_dict.update(template)

        elif isinstance(template, str):
            param_dict.update(ujson.load(open(template)))

        elif template is not None:
            raise AttributeError('Template error')

        return LidarSegmentation(param_dict, client)

    @staticmethod
    def from_id(task_id:str):
        """Get LidarSegmentation task from a task id

        :param task_id: Task id
        :type task_id: str
        :returns: LidarSegmentationTask object created based on the task id data
        :rtype: LidarSegmentationTask

        """
        task = get_api_client().fetch_task(task_id)
        return LidarSegmentation(task.param_dict, task.client)

    def publish(self, task_type: str='lidarsegmentation'):
        """Publish/create a task, request Scale API with the LidarSegmentation data

        :param task_type: Task type to create, default ``lidarsegmentation``
        :type task_type: str
        :returns: Task object creation from the response of the API call
        :rtype: scaleapi.Task

        """
        task = self.client.create_task('lidarsegmentation', **self.param_dict)
        print('Task created: %s' % task)
        return task
