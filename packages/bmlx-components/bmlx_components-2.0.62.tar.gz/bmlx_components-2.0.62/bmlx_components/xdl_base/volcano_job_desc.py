import logging


class VolcanoJobDescRender:
    def __init__(
        self,
        image,
        namespace,
        job_name,
        launch_time,
        runtime_configs,
        command_generator,
        dns_policy,
        dns_config,
        labels,
        need_ps,
        passive_quit,
    ):
        self._namespace = namespace
        (self._image, self._image_secret, self._image_policy) = image
        self._job_name = job_name
        self._launch_time = launch_time
        self._runtime_configs = runtime_configs
        self._command_generator = command_generator
        self._dns_policy = dns_policy
        self._dns_config = dns_config
        self._labels = labels
        self._need_ps = need_ps
        self._passive_quit = passive_quit

    def _node_selector(self):
        n = self._runtime_configs["node_selector"]
        return {k: n[k].as_str() for k in n.keys()}

    def _hostname_env(self):
        return [
            {
                "name": "HOSTNAME",
                "valueFrom": {"fieldRef": {"fieldPath": "metadata.name"}},
            }
        ]

    def _nvidia_env(self, visable=False):
        ret = []
        if not visable:
            ret.append(
                {"name": "NVIDIA_VISIBLE_DEVICES", "value": "void",}
            )
        return ret

    def _worker_env(self):
        return (
            self._nvidia_env(
                self._runtime_configs["resources"]["worker"]["gpu"].as_number(0)
                != 0
            )
            + self._hostname_env()
        )

    def _scheduler_ps_env(self):
        return self._nvidia_env(False) + self._hostname_env()

    def _volume_mounts(self):
        return [
            {"name": "lxcfs-cpuinfo", "mountPath": "/proc/cpuinfo",},
            {"name": "lxcfs-meminfo", "mountPath": "/proc/meminfo",},
            {"name": "lxcfs-stat", "mountPath": "/proc/stat",},
            {
                "name": "lxcfs-cpu-online",
                "mountPath": "/sys/devices/system/cpu/online",
            },
            {"name": "corefiles", "mountPath": "/data/corefiles",},
            {"name": "podinfo", "mountPath": "/etc/podinfo",},
        ]

    def _volumes(self):
        return [
            {
                "name": "lxcfs-cpuinfo",
                "hostPath": {"path": "/var/lib/lxcfs/proc/cpuinfo",},
            },
            {
                "name": "lxcfs-meminfo",
                "hostPath": {"path": "/var/lib/lxcfs/proc/meminfo",},
            },
            {
                "name": "lxcfs-stat",
                "hostPath": {"path": "/var/lib/lxcfs/proc/stat",},
            },
            {
                "name": "lxcfs-cpu-online",
                "hostPath": {
                    "path": "/var/lib/lxcfs/sys/devices/system/cpu/online",
                },
            },
            {"name": "corefiles", "hostPath": {"path": "/data/corefiles",},},
            {
                "name": "podinfo",
                "downwardAPI": {
                    "items": [
                        {
                            "path": "labels",
                            "fieldRef": {"fieldPath": "metadata.labels",},
                        },
                        {
                            "path": "name",
                            "fieldRef": {"fieldPath": "metadata.name",},
                        },
                    ]
                },
            },
        ]

    def _worker_resource(self, role):
        memory = self._runtime_configs["resources"]["worker"][
            "memory"
        ].as_sunit()
        if role == "worker_master":
            memory += self._runtime_configs["resources"]["worker"][
                "master_extra_memory"
            ].as_sunit()

        return {
            "limits": {
                "nvidia.com/gpu": self._runtime_configs["resources"]["worker"][
                    "gpu"
                ].as_number(0),
                "memory": memory.to_mega_i_str(),
                "cpu": self._runtime_configs["resources"]["worker"][
                    "cpu"
                ].as_number(),
            },
        }

    def _scheduler_resource(self):
        return {
            "requests": {
                "cpu": self._runtime_configs["resources"]["scheduler"][
                    "cpu"
                ].as_number(),
                "memory": self._runtime_configs["resources"]["scheduler"][
                    "memory"
                ]
                .as_sunit()
                .to_mega_i_str(),
            },
        }

    def _ps_resource(self):
        return {
            "limits": {
                "cpu": self._runtime_configs["resources"]["ps"][
                    "cpu"
                ].as_number(),
                "memory": self._runtime_configs["resources"]["ps"]["memory"]
                .as_sunit()
                .to_mega_i_str(),
            }
        }

    def _create_worker_pod(self, role):
        worker_command = self._command_generator(
            cluster_role=role,
            task_num=self._runtime_configs["resources"]["worker"][
                "instances"
            ].as_number(1),
            job_id=self._job_name,
            launch_time=self._launch_time,
        )

        logging.debug("start worker by command %s" % (worker_command))

        return {
            "metadata": {"labels": self._labels,},
            "spec": {
                "restartPolicy": "OnFailure",
                "imagePullSecrets": [
                    {"name": secret} for secret in self._image_secret or []
                ],
                "securityContext": {"runAsUser": 0, "runAsGroup": 0,},
                "nodeSelector": self._node_selector(),
                "containers": [
                    {
                        "command": worker_command,
                        "image": self._image,
                        "name": "xdl-worker-master"
                        if role == "worker_master"
                        else "xdl-worker-slave",  # do not change this name, it's useful for distinguish role in upper level
                        "env": self._worker_env(),
                        "workingDir": self._runtime_configs["working_dir"].get(
                            "/xdl"
                        ),
                        "imagePullPolicy": self._image_policy,
                        "resources": self._worker_resource(role),
                        "volumeMounts": self._volume_mounts(),
                        # "securityContext": {"privileged": True},
                    }
                ],
                "volumes": self._volumes(),
                "hostIPC": True,
                "hostNetwork": True,
            },
        }

    def _create_ps_pod(self):
        ps_command = self._command_generator(
            cluster_role="ps",
            task_num=self._runtime_configs["resources"]["ps"][
                "instances"
            ].as_number(1),
            job_id=self._job_name,
            launch_time=self._launch_time,
        )
        logging.debug("start scheduler with command %s" % ps_command)

        return {
            "metadata": {"labels": self._labels,},
            "spec": {
                "restartPolicy": "OnFailure",
                "imagePullSecrets": [
                    {"name": secret} for secret in self._image_secret or []
                ],
                "securityContext": {"runAsUser": 0, "runAsGroup": 0,},
                "nodeSelector": self._node_selector(),
                "containers": [
                    {
                        "command": ps_command,
                        "image": self._image,
                        "name": "xdl-ps",
                        "env": self._scheduler_ps_env(),
                        "workingDir": self._runtime_configs["working_dir"].get(
                            "/xdl"
                        ),
                        "imagePullPolicy": self._image_policy,
                        "resources": self._ps_resource(),
                        "volumeMounts": self._volume_mounts(),
                    }
                ],
                "volumes": self._volumes(),
                "hostIPC": True,
                "hostNetwork": True,
            },
        }

    def _create_scheduler_pod(self):
        scheduler_command = self._command_generator(
            cluster_role="scheduler",
            task_num=self._runtime_configs["resources"]["scheduler"][
                "instances"
            ].as_number(1),
            job_id=self._job_name,
            launch_time=self._launch_time,
        )
        logging.debug("start scheduler with command %s" % scheduler_command)

        return {
            "metadata": {"labels": self._labels,},
            "spec": {
                "restartPolicy": "OnFailure",
                "imagePullSecrets": [
                    {"name": secret} for secret in self._image_secret or []
                ],
                "securityContext": {"runAsUser": 0, "runAsGroup": 0,},
                "nodeSelector": self._node_selector(),
                "containers": [
                    {
                        "command": scheduler_command,
                        "image": self._image,
                        "name": "xdl-scheduler",
                        "env": self._scheduler_ps_env(),
                        "workingDir": self._runtime_configs["working_dir"].get(
                            "/xdl"
                        ),
                        "imagePullPolicy": self._image_policy,
                        "resources": self._scheduler_resource(),
                        "volumeMounts": self._volume_mounts(),
                    }
                ],
                "volumes": self._volumes(),
                "hostIPC": True,
                "hostNetwork": True,
            },
        }

    def _create_worker_task(self, role):
        task_spec = {
            "replicas": 1
            if role == "worker_master"
            else self._runtime_configs["resources"]["worker"][
                "instances"
            ].as_number()
            - 1,
            "name": "wm" if role == "worker_master" else "wc",
            "namespace": self._namespace,
            "maxRetry": 3 if role == "worker_master" else 20,
            "template": self._create_worker_pod(role),
        }

        if role == "worker_slave" and self._passive_quit:
            task_spec["passiveQuit"] = True
        return task_spec

    def _create_ps_task(self):
        task_spec = {
            "replicas": self._runtime_configs["resources"]["ps"][
                "instances"
            ].as_number(),
            "name": "ps",
            "namespace": self._namespace,
            "maxRetry": 20,
            "passiveQuit": True,
            "template": self._create_ps_pod(),
        }
        return task_spec

    def _create_scheduler_task(self):
        task_spec = {
            "replicas": 1,
            "name": "sc",
            "namespace": self._namespace,
            "maxRetry": 1,
            "passiveQuit": True,
            "template": self._create_scheduler_pod(),
        }

        return task_spec

    def spec(self):
        min_avaliable = self._runtime_configs["resources"]["worker"][
            "instances"
        ].as_number()
        if self._need_ps:
            min_avaliable += (
                self._runtime_configs["resources"]["ps"][
                    "instances"
                ].as_number()
                + 1
            )

        try:
            job_spec = {
                "apiVersion": "batch.volcano.sh/v1alpha1",
                "kind": "Job",
                "metadata": {"name": self._job_name, "labels": self._labels,},
                "spec": {
                    "schedulerName": "volcano",
                    "minAvailable": min_avaliable,
                    "queue": self._runtime_configs["queue"].as_str("default"),
                    "plugins": {"svc": [], "env": [],},
                    "tasks": [
                        self._create_worker_task("worker_master"),
                        self._create_worker_task("worker_slave"),
                    ]
                    if self._runtime_configs["resources"]["worker"][
                        "instances"
                    ].as_number()
                    > 1
                    else [self._create_worker_task("worker_master"),],
                },
            }

            if self._need_ps:
                job_spec["spec"]["tasks"].extend(
                    [self._create_ps_task(), self._create_scheduler_task()]
                )

        except KeyError as e:
            logging.exception("")
            raise RuntimeError(
                "Config Error happens: %s, please check your config" % e
            )

        return job_spec
