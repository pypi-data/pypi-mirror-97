# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raylab',
 'raylab.agents',
 'raylab.agents.acktr',
 'raylab.agents.mage',
 'raylab.agents.mbpo',
 'raylab.agents.naf',
 'raylab.agents.sac',
 'raylab.agents.sop',
 'raylab.agents.svg',
 'raylab.agents.svg.inf',
 'raylab.agents.svg.one',
 'raylab.agents.svg.soft',
 'raylab.agents.td3',
 'raylab.agents.trpo',
 'raylab.cli',
 'raylab.envs',
 'raylab.envs.environments',
 'raylab.envs.environments.lqr',
 'raylab.envs.wrappers',
 'raylab.execution',
 'raylab.logger',
 'raylab.policy',
 'raylab.policy.losses',
 'raylab.policy.model_based',
 'raylab.policy.modules',
 'raylab.policy.modules.actor',
 'raylab.policy.modules.actor.policy',
 'raylab.policy.modules.critic',
 'raylab.policy.modules.model',
 'raylab.policy.modules.model.stochastic',
 'raylab.policy.modules.networks',
 'raylab.torch',
 'raylab.torch.distributions',
 'raylab.torch.nn',
 'raylab.torch.nn.distributions',
 'raylab.torch.nn.distributions.flows',
 'raylab.torch.nn.modules',
 'raylab.torch.optim',
 'raylab.tune',
 'raylab.utils',
 'raylab.utils.exploration']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.1.0,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'dataclasses-json>=0.5.1,<0.6.0',
 'dm-tree>=0.1.5,<0.2.0',
 'opencv-contrib-python>=4.4.0,<5.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'poetry-version>=0.1.5,<0.2.0',
 'pytorch-lightning>=1.0,<2.0',
 'ray[tune,rllib]>=1.0.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'streamlit>=0.62,<0.79',
 'tabulate>=0.8.7,<0.9.0',
 'torch>=1.5.1,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0"': ['cachetools>=4.1.0,<5.0.0'],
 'wandb': ['wandb>=0.10,<0.11']}

entry_points = \
{'console_scripts': ['raylab = raylab.cli:raylab']}

setup_kwargs = {
    'name': 'raylab',
    'version': '0.15.1',
    'description': 'Reinforcement learning algorithms in RLlib and PyTorch.',
    'long_description': '======\nraylab\n======\n\n|PyPI| |Tests| |Dependabot| |License| |CodeStyle|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/raylab?logo=PyPi&logoColor=white&color=blue\n\t  :alt: PyPI\n\n.. |Tests| image:: https://img.shields.io/github/workflow/status/angelolovatto/raylab/Poetry%20package?label=tests&logo=GitHub\n\t   :alt: GitHub Workflow Status\n\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=angelolovatto/raylab\n\t\t:target: https://dependabot.com\n\n.. |License| image:: https://img.shields.io/github/license/angelolovatto/raylab?color=blueviolet&logo=github\n\t     :alt: GitHub\n\n.. |CodeStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n\t       :target: https://github.com/psf/black\n\n\nReinforcement learning algorithms in `RLlib <https://github.com/ray-project/ray/tree/master/rllib>`_ and `PyTorch <https://pytorch.org>`_.\n\n\nIntroduction\n------------\n\nRaylab provides agents and environments to be used with a normal RLlib/Tune setup.\n\n.. code-block:: python\n\n             import ray\n             from ray import tune\n             import raylab\n\n             def main():\n                 raylab.register_all_agents()\n                 raylab.register_all_environments()\n                 ray.init()\n                 tune.run(\n                     "NAF",\n                     local_dir=...,\n                     stop={"timesteps_total": 100000},\n                     config={\n                         "env": "CartPoleSwingUp-v0",\n                         "exploration_config": {\n                             "type": tune.grid_search([\n                                 "raylab.utils.exploration.GaussianNoise",\n                                 "raylab.utils.exploration.ParameterNoise"\n                             ])\n                         }\n                         ...\n                     },\n                 )\n\n             if __name__ == "__main__":\n                 main()\n\n\nOne can then visualize the results using `raylab dashboard`\n\n.. image:: https://i.imgur.com/bVc6WC5.png\n        :align: center\n\n\nInstallation\n------------\n\n.. code:: bash\n\n          pip install raylab\n\n\nAlgorithms\n----------\n\n+--------------------------------------------------------+-------------------------+\n| Paper                                                  | Agent Name              |\n+--------------------------------------------------------+-------------------------+\n| `Actor Critic using Kronecker-factored Trust Region`_  | ACKTR                   |\n+--------------------------------------------------------+-------------------------+\n| `Trust Region Policy Optimization`_                    | TRPO                    |\n+--------------------------------------------------------+-------------------------+\n| `Normalized Advantage Function`_                       | NAF                     |\n+--------------------------------------------------------+-------------------------+\n| `Stochastic Value Gradients`_                          | SVG(inf)/SVG(1)/SoftSVG |\n+--------------------------------------------------------+-------------------------+\n| `Soft Actor-Critic`_                                   | SoftAC                  |\n+--------------------------------------------------------+-------------------------+\n| `Streamlined Off-Policy`_ (DDPG)                       | SOP                     |\n+--------------------------------------------------------+-------------------------+\n| `Model-Based Policy Optimization`_                     | MBPO                    |\n+--------------------------------------------------------+-------------------------+\n| `Model-based Action-Gradient-Estimator`_               | MAGE                    |\n+--------------------------------------------------------+-------------------------+\n\n\n.. _`Actor Critic using Kronecker-factored Trust Region`: https://arxiv.org/abs/1708.05144\n.. _`Trust Region Policy Optimization`: http://proceedings.mlr.press/v37/schulman15.html\n.. _`Normalized Advantage Function`: http://proceedings.mlr.press/v48/gu16.html\n.. _`Stochastic Value Gradients`: http://papers.nips.cc/paper/5796-learning-continuous-control-policies-by-stochastic-value-gradients\n.. _`Soft Actor-Critic`: http://proceedings.mlr.press/v80/haarnoja18b.html\n.. _`Model-Based Policy Optimization`: http://arxiv.org/abs/1906.08253\n.. _`Streamlined Off-Policy`: https://arxiv.org/abs/1910.02208\n.. _`Model-based Action-Gradient-Estimator`: https://arxiv.org/abs/2004.14309\n\n\nCommand-line interface\n----------------------\n\n.. role:: bash(code)\n   :language: bash\n\nFor a high-level description of the available utilities, run :bash:`raylab --help`\n\n.. code:: bash\n\n\tUsage: raylab [OPTIONS] COMMAND [ARGS]...\n\n\t  RayLab: Reinforcement learning algorithms in RLlib.\n\n\tOptions:\n\t  --help  Show this message and exit.\n\n\tCommands:\n\t  dashboard    Launch the experiment dashboard to monitor training progress.\n\t  episodes     Launch the episode dashboard to monitor state and action...\n\t  experiment   Launch a Tune experiment from a config file.\n\t  find-best    Find the best experiment checkpoint as measured by a metric.\n\t  info         View information about an agent\'s config parameters.\n\t  rollout      Wrap `rllib rollout` with customized options.\n\t  test-module  Launch dashboard to test generative models from a checkpoint.\n\n\nPackages\n--------\n\nThe project is structured as follows\n::\n\n    raylab\n    |-- agents            # Trainer and Policy classes\n    |-- cli               # Command line utilities\n    |-- envs              # Gym environment registry and utilities\n    |-- logger            # Tune loggers\n    |-- policy            # Extensions and customizations of RLlib\'s policy API\n    |   |-- losses        # RL loss functions\n    |   |-- modules       # PyTorch neural network modules for TorchPolicy\n    |-- pytorch           # PyTorch extensions\n    |-- utils             # miscellaneous utilities\n',
    'author': 'Ângelo Gregório Lovatto',
    'author_email': 'angelolovatto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/angelolovatto/raylab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
