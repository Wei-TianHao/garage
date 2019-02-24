"""
An example to train a task with DQN algorithm.

Here it creates a gym environment CartPole. And uses a DQN with
1M steps.
"""
import gym

from garage.envs import normalize
from garage.experiment import run_experiment
from garage.replay_buffer import SimpleReplayBuffer
from garage.tf.algos import DQN
from garage.tf.envs import TfEnv
from garage.tf.exploration_strategies import EpsilonGreedyStrategy
from garage.tf.policies import DiscreteQfDerivedPolicy
from garage.tf.q_functions import DiscreteMLPQFunction


def run_task(*_):
    """Run task."""
    max_path_length = 200
    n_epochs = 50

    env = TfEnv(normalize(gym.make("CartPole-v0")))

    replay_buffer = SimpleReplayBuffer(
        env_spec=env.spec,
        size_in_transitions=int(20000),
        time_horizon=max_path_length)

    qf = DiscreteMLPQFunction(
        env_spec=env.spec, hidden_sizes=(64, 64), dueling=False)

    policy = DiscreteQfDerivedPolicy(env_spec=env, qf=qf)

    epilson_greedy_strategy = EpsilonGreedyStrategy(
        env_spec=env.spec,
        total_step=max_path_length * n_epochs,
        max_epsilon=1.0,
        min_epsilon=0.02,
        decay_ratio=0.5)

    algo = DQN(
        env=env,
        policy=policy,
        qf=qf,
        exploration_strategy=epilson_greedy_strategy,
        replay_buffer=replay_buffer,
        max_path_length=max_path_length,
        n_epochs=n_epochs,
        qf_lr=1e-3,
        discount=1.0,
        min_buffer_size=1e4,
        n_train_steps=500,
        smooth_return=False,
        target_network_update_freq=2,
        buffer_batch_size=32)

    algo.train()


run_experiment(
    run_task,
    n_parallel=1,
    snapshot_mode="last",
    seed=1,
    plot=False,
)
