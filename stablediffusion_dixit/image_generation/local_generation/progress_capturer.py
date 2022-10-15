import torch
from diffusers import StableDiffusionPipeline


class ProgressCapturer:
    def __init__(self, pipe: StableDiffusionPipeline):
        self.latents = []
        self.pipe = pipe

    def __call__(self, i, n, latent):
        self.latents.append(latent[0])

    def get_images(self):
        with torch.no_grad():
            latents = torch.stack(self.latents)
            latents = 1 / 0.18215 * latents
            images = self.pipe.vae.decode(latents).sample

            images = (images / 2 + 0.5).clamp(0, 1)

            # we always cast to float32 as this does not cause significant overhead and is compatible with bfloa16
            images = images.cpu().permute(0, 2, 3, 1).float().numpy()
            return self.pipe.numpy_to_pil(images)

