import logging

from skippy.data.minio import upload_file, download_files


def consume(urns=None):
    def wrapper(func):
        level = logging.DEBUG

        # Set the log level
        logging.getLogger().setLevel(level)
        logging.info('Consume.wrapper(%s)' % func)

        def call(*args, **kwargs):
            logging.info('Consume.call(%s,%s,%s)' % (func, args, kwargs))
            artifact = download_files(urns)
            kwargs['data'] = artifact
            return func(*args, **kwargs)

        logging.debug('Consume.wrapper over')
        return call

    return wrapper


def produce(urn=None):
    def wrapper(func):
        level = logging.DEBUG

        # Set the log level
        logging.getLogger().setLevel(level)
        logging.info('Produce.wrapper(%s)' % func)

        def call(*args, **kwargs):
#            logging.info('Produce.call (%s,%s,%s)' % (func, args, kwargs))
            logging.info('Produce.call')
            response = func(*args, **kwargs)
            upload_file(response, urn)
#            logging.debug('Produce.store(%s)' % response)
            return response

        logging.debug('Produce.wrapper over')
        return call

    return wrapper


