import os
import random

from hook import Hook

Hook.hook_all()

seed = 7
random.seed(seed)
import numpy as np

np.random.seed(seed)
import torch as th

th.manual_seed(seed)
th.cuda.manual_seed(seed)
th.cuda.manual_seed_all(seed)

# th.backends.cudnn.

from experiment.oyebolu2019.standard_self_attention.elsp_callback import CustomCallback
from experiment.oyebolu2019.standard_self_attention.module.set_transformer import CustomActorCriticPolicy
from stable_baselines3.ppo import PPO

from stable_baselines3.common.vec_env import SubprocVecEnv

cpu_num = 32
total_steps = int(11e6)
n_steps = 200
batch_size = cpu_num * n_steps
n_epochs = 50
lr = 0.001
gamma = 0.96


# env = make_vec_env(env_id, n_envs=cpu_num,
#                   env_kwargs={'ep_log': False, 'planning_year': 1, 'max_product_times': None})

def train(env, path=None):
    model = PPO(CustomActorCriticPolicy, env, verbose=0, learning_rate=lr,
                n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, gamma=gamma)
    setattr(model, 'total_steps', total_steps)
    setattr(model, 'env_root_path', env.get_attr("env_path")[0])
    setattr(model, 'cfg_root_path', env.get_attr("cfg_path")[0])
    setattr(model, 'env_path', os.path.basename(env.get_attr("env_path")[0]))
    setattr(model, 'cfg_path', os.path.basename(env.get_attr("cfg_path")[0]))
    callback = CustomCallback(env, model,
                              eval_th={'elsp_env_00105': 19.55e4 - 0.5e4,
                                       'elsp_env_00108': 24.1e4 - 0.5e4,
                                       'elsp_env_00111': 33.3e4 - 0.5e4,
                                       'elsp_env_00112': 26.9e4 - 0.5e4,
                                       'elsp_env_00114': 32.2e4 - 0.5e4,
                                       'elsp_env_00130': 19.6e4 - 0.5e4}[os.path.basename(env.get_attr("env_path")[0])])
    import atexit
    def at_exit():
        callback.on_training_end()
        pass

    atexit.register(at_exit)

    model.learn(total_timesteps=total_steps, callback=callback)


if __name__ == '__main__':
    from experiment.oyebolu2019.env_create import env_creator
    env = SubprocVecEnv([env_creator for i in range(cpu_num)])
    train(env,
          None if True else "result/algorithm_<class 'stable_baselines3.ppo.ppo.PPO'>/reward_type_profit_delta_per_day")
