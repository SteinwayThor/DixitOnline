from typing import Optional, Callable, Tuple
import multiprocessing
from multiprocessing import Queue

import threading

import torch
from diffusers import StableDiffusionPipeline

from stablediffusion_dixit.image_generation.image_generator import ImageGenerator
from stablediffusion_dixit.image_generation.local_generation.progress_capturer import ProgressCapturer


IMAGE_FOLDER = "images"
ANIMATION_FOLDER = "animations"
NUM_INFERENCE_STEPS = 10

def image_generation_process(queue: Queue):
    if not torch.cuda.is_available():
        gen_pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", safety_checker=None)
        if torch.backends.mps.is_available():
            gen_pipeline = gen_pipeline.to("mps")
    else:
        gen_pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16",
                                                       torch_dtype=torch.float16, safety_checker=None).to("cuda:0")


    print("initialized")
    while True:
        prompt, index, result_pipeline = queue.get()
        pc = ProgressCapturer(gen_pipeline)
        image = gen_pipeline(prompt, num_inference_steps=NUM_INFERENCE_STEPS, width=384, height=512,
                 callback=pc).images[0]
        image_path = f"{IMAGE_FOLDER}/{index}.png"
        image.save(image_path, format="png")
        pci = pc.get_images()

        anim_path = f"{ANIMATION_FOLDER}/{index}.gif"
        pci[2].save(anim_path, format='GIF',
                    append_images=pci[3:], save_all=True, duration=300, loop=0)
        print(f"generated image {index}")

        result_pipeline.send((image_path, anim_path))


class LocalImageGenerator(ImageGenerator):
    def __init__(self):
        self.task_queue = Queue()
        self.proc = multiprocessing.Process(
            target=image_generation_process,
            kwargs={
                "queue": self.task_queue
            },
            daemon=True
        )
        self.proc.start()
        self.generated_images = []

    def request_generation(self, prompt: str, callback: Optional[Callable[[int, str, str], None]] = None) -> int:
        index = len(self.generated_images)
        self.generated_images.append(None)

        def generation_waiting_thread():
            (recv, send) = multiprocessing.Pipe(duplex=False)
            self.task_queue.put((prompt, index, send))
            image_path, anim_path = recv.recv()
            self.generated_images[index] = image_path, anim_path
            if callback is not None:
                callback(index, image_path, anim_path)

        thread = threading.Thread(target=generation_waiting_thread)
        thread.start()

        return index

    def get_image_and_anim(self, image_num) -> Optional[Tuple[str, str]]:
        return self.generated_images[image_num]