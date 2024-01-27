
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageFilter

images = [
    'img_1.jpg',
    'img_2.jpg',
    'img_3.jpg',
    'img_4.jpg',
    'img_5.jpg',
    'img_6.jpg',
    'img_7.jpg',
    'img_8.jpg',
    'img_8.jpg',
    'img_9.jpg',
    'img_10.jpg',
    'img_11.jpg',
    'img_12.jpg',
]


def cpu_heavy(img_name: str) -> None:
    img = Image.open('./images/input/' + img_name)
    img = img.filter(ImageFilter.GaussianBlur(50))
    img.save(f'./images/output/{img_name}')
    print(f"{img_name} was processed.")


if __name__ == '__main__':
    t1 = time.perf_counter()
    images *= 10
    # for img in images:
    #      cpu_heavy(img)
    # processes = []
    # for img in images:
    #     process = multiprocessing.Process(target=cpu_heavy, args=(img,))
    #     process.start()
    #     processes.append(process)
    
    # for p in processes:
    #     p.join()
    # with multiprocessing.Pool() as pool:
    #     pool.map(cpu_heavy, images)
    
    with ProcessPoolExecutor() as exe:
        [exe.submit(cpu_heavy, img) for img in images]
        
    t2 = time.perf_counter()

    print(f'Finished in {t2-t1:.3f} seconds')
