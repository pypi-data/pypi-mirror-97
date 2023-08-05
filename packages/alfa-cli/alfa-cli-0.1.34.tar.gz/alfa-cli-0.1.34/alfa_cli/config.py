from dotmap import DotMap

algorithm = DotMap(
    {
        "defaults": {
            "specification": {
                "path": "alfa.yml",
            },
        },
        "initialization": {
            "functions": {
                "invoke": {"required": True},
                "search": {"required": False},
                "score": {"required": False},
                "build": {"required": False},
                "preProcess": {"required": False},
                "postProcess": {"required": False},
            },
            "specification": {
                "regions": ["eu-central-1"],
                "runtimes": ["python", "node"],
                "architectures": {
                    "serverless": {
                        "timeout": {"max": 900},
                        "settings": {"memory": range(128, 3009, 64)},
                    },
                    "docker": {
                        "timeout": {"max": float("inf")},
                        "settings": {
                            "cpu": [256, 512, 1024, 2048, 4096],
                            "memory": {
                                "cpu==256": [512, 1024, 2048],
                                "cpu==512": range(1024, 4097, 1024),
                                "cpu==1024": range(2048, 8193, 1024),
                                "cpu==2048": range(4096, 16385, 1024),
                                "cpu==4096": range(8192, 30721, 1024),
                            },
                        },
                    },
                    "virtual-machine": {
                        "timeout": {"max": float("inf")},
                        "settings": {
                            "type": [
                                "t3.nano",
                                "t3.micro",
                                "t3.small",
                                "t3.medium",
                                "t3.large",
                                "t3.xlarge",
                                "t3.2xlarge",
                            ]
                        },
                    },
                },
                "arguments": {
                    "search": [
                        {"key": "searchOptions"},
                        {"key": "data"},
                        {"key": "scores"},
                    ],
                    "score": [
                        {"key": "data"},
                    ],
                    "build": [
                        {"key": "data"},
                    ],
                    "preProcess": [
                        {"key": "problem"},
                    ],
                    "invoke": [],
                    "postProcess": [
                        {"key": "problem"},
                        {"key": "result"},
                    ]
                }
            },
        },
    }
)

settings = DotMap({
    "reference": {
        "key": "__wb_ref",
        "compression": {"file_name": "data"},
    }
})
