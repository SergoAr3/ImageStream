from threading import Thread, Timer

from app.fetch_service.app import fetch_and_enqueue_images
from app.storage_service.app import dequeue_and_save_images


def main(func1, func2):
    func1_thr1 = Thread(target=func1, name=func1.__name__)
    func1_thr2 = Thread(target=func1, name=func1.__name__)

    func2_thr1 = Timer(1, func2)
    func2_thr2 = Timer(1, func2)
    func2_thr1.name = func2.__name__
    func2_thr2.name = func2.__name__

    func1_thr1.start()
    func1_thr2.start()

    func2_thr1.start()
    func2_thr2.start()


if __name__ == '__main__':
    main(fetch_and_enqueue_images, dequeue_and_save_images)
