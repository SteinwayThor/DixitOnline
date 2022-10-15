import torch
from diffusers import StableDiffusionPipeline


class ProgressCapturer:
    def __init__(self, pipe: StableDiffusionPipeline):
        self.latents = []
        self.pipe = pipe

    def __call__(self, i, n, latent):
        self.latents.append(latent)

    def get_images(self):
        images = []
        with torch.no_grad():
            for l in self.latents:
                latents = 1 / 0.18215 * l
                image = self.pipe.vae.decode(latents).sample

                image = (image / 2 + 0.5).clamp(0, 1)

                # we always cast to float32 as this does not cause significant overhead and is compatible with bfloa16
                image = image.cpu().permute(0, 2, 3, 1).float().numpy()
                images.append(self.pipe.numpy_to_pil(image)[0])

        return images

