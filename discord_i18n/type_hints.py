from typing import Dict, Union, Callable, Coroutine

__all__ = ('JSON', 'TOML', 'CoroutineFunction')


JSON = TOML = Dict[str, Union[str, int, float, bool, list, dict, None]]
CoroutineFunction = Callable[..., Coroutine]
