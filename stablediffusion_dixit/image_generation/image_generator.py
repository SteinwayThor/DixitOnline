import abc
from typing import Optional, Callable


class ImageGenerator(abc.ABC):
    @abc.abstractmethod
    def request_generation(self, prompt: str, callback: Optional[Callable[[int, str], None]] = None) -> int:
        pass

    @abc.abstractmethod
    def get_image(self, image_num) -> Optional[str]:
        """
        :return: Path to image if it exists, or None if it is still being generated
        """
        pass