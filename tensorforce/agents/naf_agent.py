# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Agent using Normalized Advantage Functions.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from tensorforce.agents import MemoryAgent
from tensorforce.models import NAFModel


class NAFAgent(MemoryAgent):
    """
    Normalized Advantage Functions (NAF) agent ([Gu et al., 2016](https://arxiv.org/pdf/1603.00748.pdf)), a.k.a.
    DQN for continuous actions.

    Configuration:

    Each agent requires the following configuration parameters:

    * `states`: dict containing one or more state definitions.
    * `actions`: dict containing one or more action definitions.
    * `preprocessing`: dict or list containing state preprocessing configuration.
    * `exploration`: dict containing action exploration configuration.

    The `MemoryAgent` class additionally requires the following parameters:

    * `batch_size`: integer of the batch size.
    * `memory_capacity`: integer of maximum experiences to store.
    * `memory`: string indicating memory type ('replay' or 'prioritized_replay').
    * `memory_args`: list of arguments to pass to replay memory constructor.
    * `memory_kwargs`: list of keyword arguments to pass to replay memory constructor.
    * `update_frequency`: integer indicating the number of steps between model updates.
    * `first_update`: integer indicating the number of steps to pass before the first update.
    * `repeat_update`: integer indicating how often to repeat the model update.

    Each model requires the following configuration parameters:

    * `discount`: float of discount factor (gamma).
    * `learning_rate`: float of learning rate (alpha).
    * `optimizer`: string of optimizer to use (e.g. 'adam').
    * `optimizer_args`: list of arguments for optimizer.
    * `optimizer_kwargs`: dict of keyword arguments for optimizer.
    * `device`: string of tensorflow device name.
    * `tf_saver`: boolean whether to save model parameters.
    * `tf_summary`: boolean indicating whether to use tensorflow summary file writer.
    * `log_level`: string containing logleve (e.g. 'info').
    * `distributed`: boolean indicating whether to use distributed tensorflow.
    * `global_model`: global model.
    * `session`: session to use.

    The NAF agent expects the following additional configuration parameters:

    * `target_update_frequency`: int of states between updates of the target network.
    * `update_target_weight`: float of update target weight (tau parameter).
    * `clip_gradients`: float of maximum values for gradients before clipping.

    """

    name = 'NAFAgent'
    model = NAFModel
    default_config = dict(
        target_update_frequency=10000
    )

    def __init__(self, config):
        config.default(MemoryAgent.default_config)
        super(NAFAgent, self).__init__(config)
        self.target_update_frequency = config.target_update_frequency

    def observe(self, reward, terminal):
        super(NAFAgent, self).observe(reward=reward, terminal=terminal)

        if self.timestep >= self.first_update and self.timestep % self.target_update_frequency == 0:
            self.model.update_target()
