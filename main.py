from threading import Thread, Timer, current_thread
from loguru import logger
from src.core.services.image_service import ImageService
from src.service_provider import get_image_service


def get_images(image_service: ImageService):
    thread_name = current_thread().name

    try:
        logger.debug(f"Start {thread_name} thread")
        image_service.get_images()
        logger.debug(f"Complete {thread_name} task")
    except Exception as e:
        logger.error(f"Error in {thread_name}: {e}")


def fetch_images(image_service: ImageService):
    thread_name = current_thread().name
    try:
        logger.debug(f"Start {thread_name} thread")
        image_service.fetch_images()
        logger.debug("Complete {thread_name} task")
    except Exception as e:
        logger.error(f"Error in {thread_name}: {e}")


def main(func1, func2):
    image_service = get_image_service()
    thr_1 = Thread(target=func1, args=(image_service,), name='fetch_images')
    thr_2 = Timer(1, func2, args=(image_service,))
    get_images.name = 'get_images'
    thr_1.start()
    thr_2.start()


if __name__ == '__main__':
    main(fetch_images, get_images)
