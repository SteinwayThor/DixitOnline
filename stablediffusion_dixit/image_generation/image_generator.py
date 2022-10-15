import abc
from typing import Optional, Callable, Tuple


class ImageGenerator(abc.ABC):
    @abc.abstractmethod
    def request_generation(self, prompt: str, callback: Optional[Callable[[int, str, str], None]] = None) -> int:
        pass

    @abc.abstractmethod
    def get_image_and_anim(self, image_num) -> Optional[Tuple[str, str]]:
        """
        :return: Path to image and animation if it exists, or None if it is still being generated
        """
        pass