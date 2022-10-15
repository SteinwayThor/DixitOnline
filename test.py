from time import sleep

from stablediffusion_dixit.image_generation.local_generation.local_image_generator import LocalImageGenerator

if __name__ == '__main__':
    l = LocalImageGenerator()
    l.request_generation("an astronaut riding a horse", lambda idx, path1, path2: print(f"{idx}: {path1}, {path2}"))
    l.request_generation("a photograph of a dragon", lambda idx, path1, path2: print(f"{idx}: {path1}, {path2}"))

    print("blah blah")

    sleep(300)