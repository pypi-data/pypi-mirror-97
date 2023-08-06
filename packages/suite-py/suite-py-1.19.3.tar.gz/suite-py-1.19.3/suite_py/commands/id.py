# -*- coding: utf-8 -*-
import re

from pptree import Node, print_tree
from suite_py.lib.handler import aws_handler as aws
from suite_py.lib import logger


class ID:
    def __init__(self, project, env):
        self._project = project
        self._env = env

    def run(self):

        clusters_names = aws.get_ecs_clusters(self._env)
        n_services = Node("services")

        projects = {"prima": ["web", "consumer-api"], "ab_normal": ["abnormal"]}
        project_names = projects.get(self._project, [self._project])

        for cluster_name in clusters_names:

            services = []
            all_services = aws.get_ecs_services(cluster_name)

            for service in all_services:
                if service["status"] == "ACTIVE":
                    for prj in project_names:
                        if prj in service["serviceName"]:
                            services.append(service["serviceName"])

            for service in services:
                container_instances = []
                container_instances = aws.get_container_instances_arn_from_service(
                    cluster_name, service
                )
                if container_instances:
                    ids = aws.get_ids_from_container_instances(
                        cluster_name, container_instances
                    )

                    m = re.search(f"ecs-task-.*-{self._env}-ECSService(.*)-.*", service)
                    if m:
                        n_service = Node(m.group(1), n_services)
                        for _id in ids:
                            Node(_id, n_service)

        if n_services.children:
            print_tree(n_services, horizontal=True)
        else:
            logger.info(
                f"No active tasks for {self._project} in environment {self._env}"
            )
        logger.info("Done!")
