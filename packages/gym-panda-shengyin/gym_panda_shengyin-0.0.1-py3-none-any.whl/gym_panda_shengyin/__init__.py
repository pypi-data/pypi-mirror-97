from gym.envs.registration import register

register(
    id='panda-v0',
    entry_point='gym_panda_shengyin.envs:PandaEnv',
)