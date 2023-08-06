from __future__ import annotations
from typing import List
from datetime import datetime
import os
import time
from .constants import DOWNLOAD_COOLDOWN

import dateutil.parser

from . import htb
from .errors import IncorrectFlagException, IncorrectArgumentException, NoDockerException,\
    NoDownloadException, RateLimitException


class Challenge(htb.HTBObject):
    """ The class representing Hack The Box challenges

    Attributes:
        name (str): The name of the challenge
        retired: Whether the challenge is retired
        difficulty: The official difficulty of the challenge
        avg_difficulty: The average user-given difficulty
        points: The points awarded on completion
        difficulty_ratings: A dict of difficulty ratings given
        solves: The number of solves a challenge has
        likes: The number of likes a challenge has
        dislikes: The number of dislikes a challenge has
        release_date: The date the challenge was released
        solved: Whether the active user has completed the challenge
        is_liked: Whether the active user has liked the challenge
        is_disliked: Whether the active user has disliked the challenge

        description: The challenge description
        category_id: The ID of the challenge category
        category: The name of the category
        has_download: Whether the challenge has a download available
        has_docker: Whether the challenge has a remote instance available

    """
    name: str = None
    retired: bool = None
    difficulty: str = None
    avg_difficulty: int = None
    points: int = None
    difficulty_ratings = None
    solves: int = None
    likes: int = None
    dislikes: int = None
    release_date: datetime = None
    solved: bool = None
    is_liked: bool = None
    is_disliked: bool = None
    recommended: bool = None

    # noinspection PyUnresolvedReferences
    _authors: List["User"] = None
    _author_ids: List[int] = None

    _detailed_attributes = ('description', 'category', 'has_download', 'has_docker', 'instance')
    description: str
    category_id: int
    category: str
    has_download: bool
    has_docker: bool
    instance: DockerInstance

    def submit(self, flag: str, difficulty: int):
        """ Submits a flag for a Challenge

        Args:
            flag: The flag for the Challenge
            difficulty: A rating between 10 and 100 of the Challenge difficulty.
                        Must be a multiple of 10.

        """
        if difficulty < 10 or difficulty > 100 or difficulty % 10 != 0:
            raise IncorrectArgumentException(reason="Difficulty must be a multiple of 10, between 10 and 100")

        submission = self._client.do_request("challenge/own", json_data={
            "flag": flag,
            "challenge_id": self.id,
            "difficulty": difficulty
        })
        if submission['message'] == "Incorrect flag":
            raise IncorrectFlagException
        return True

    def start(self) -> DockerInstance:
        """
        Requests the challenge be started

        Returns:
            The DockerInstance that was started

        """
        if not self.has_docker:
            raise NoDockerException
        instance = self._client.do_request("challenge/start", json_data={"challenge_id": self.id})
        # TODO: Handle failure to start
        self.instance = DockerInstance(instance['ip'], instance['port'], self.id, self._client, instance['id'])
        return self.instance

    def download(self, path=None) -> str:
        """

        Args:
            path: The name of the zipfile to download to. If none is provided, it is saved to the current directory.

        Returns: The path of the file

        """
        if not self.has_download:
            raise NoDownloadException
        if self._client.challenge_cooldown > time.time():
            raise RateLimitException("Challenge download ratelimit exceeded - please do not remove this")
        if path is None:
            path = os.path.join(os.getcwd(), f"{self.name}.zip")
        data = self._client.do_request(f"challenge/download/{self.id}", download=True)
        self._client._cooldown = time.time() + DOWNLOAD_COOLDOWN
        with open(path, 'wb') as f:
            f.write(data)
        return path

    # noinspection PyUnresolvedReferences
    @property
    def authors(self) -> List["User"]:
        """Fetch the author(s) of the Challenge

        Returns: List of Users

        """
        if not self._authors:
            self._authors = []
            for uid in self._author_ids:
                self._authors.append(self._client.get_user(uid))
        return self._authors

    def __repr__(self):
        return f"<Challenge '{self.name}'>"

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary: bool = False):
        """Initialise a `Challenge` using API data"""
        self._client = client
        self._detailed_func = client.get_challenge
        self.id = data['id']
        self.name = data['name']
        self.retired = bool(data['retired'])
        self.points = int(data['points'])
        self.difficulty_ratings = data['difficulty_chart']
        self.solves = data['solves']
        self.solved = data['authUserSolve']
        self.likes = data['likes']
        self.dislikes = data['dislikes']
        self.release_date = dateutil.parser.parse(data['release_date'])
        if not summary:
            self.description = data['description']
            self.category = data['category_name']
            self._author_ids = [data['creator_id']]
            if data['creator2_id']:
                self._author_ids.append(data['creator2_id'])
            self.has_download = data['download']
            self.has_docker = data['docker']
            if data['docker_ip']:
                self.instance = DockerInstance(data['docker_ip'], data['docker_port'], self.id, self._client)
            else:
                self.instance = None
        else:
            self._is_summary = True


class DockerInstance:
    """Representation of an active Docker container instance of a Challenge

    Attributes:
        container_id: The ID of the container
        port: The port the container is listening on
        ip: The IP the instance can be reached at
        chall_id: The connected challenge
        client: The passed-through API client

    """

    id: str = None
    port: int = None
    ip: str = None
    chall_id: int = None
    client: htb.HTBClient = None

    def __init__(self, ip: str, port: int,  chall_id: int, client: htb.HTBClient, container_id: str = None):
        self.client = client
        self.id = container_id
        self.port = port
        self.ip = ip
        self.chall_id = chall_id

    def stop(self):
        """Request the instance be stopped. Zeroes out all properties"""
        self.client.do_request("challenge/stop", json_data={"challenge_id": self.chall_id})
        # TODO: Handle failures to stop

        # Can't delete referencees to the object from here so we just have
        # to set everything to None and prevent further usage
        self.id = None
        self.port = None
        self.ip = None
