
import time
import logging
import threading
from queue import Queue
from queue import Empty
from . import funcutils
from . import sysutils

logger = logging.getLogger(__name__)
get_ident = threading.get_ident

class StartOnTerminatedService(RuntimeError):
    pass

class ServiceStop(RuntimeError):
    pass

class ServiceTerminate(RuntimeError):
    pass

class LoopIdle(RuntimeError):
    pass

class ProduceIdle(LoopIdle):
    pass

class ConsumeIdle(LoopIdle):
    pass


class ServiceBase(object):

    def __init__(self):
        self.work_thread_starting_lock = threading.Lock()
        self.work_thread = None
        self.terminate_flag = False
        self.terminate_time = None
        self.terminated = False
        self.terminated_time = None
        self.is_running = False

    def start(self):
        if self.terminated:
            raise StartOnTerminatedService()
        self.start_time = time.time()
        self.stop_flag = False
        self.stop_time = None
        self.stopped = False
        self.stopped_time = None
        with self.work_thread_starting_lock:
            if self.work_thread is None:
                self.work_thread = threading.Thread(target=self.main)
                self.work_thread.setDaemon(True)
                self.work_thread.start()
    
    def stop(self, wait=True, wait_timeout=-1):
        self.stop_flag = True
        self.stop_time = time.time()
        return self.join(wait, wait_timeout)

    def terminate(self, wait=True, wait_timeout=-1):
        self.terminate_flag = True
        self.terminate_time = time.time()
        return self.stop(wait, wait_timeout)

    def join(self, wait=True, wait_timeout=-1):
        """Return True means service stopped, False means not stopped and timeout, None means no waiting...
        """
        if not wait:
            return not self.is_running
        stime = time.time()
        while self.is_running:
            if wait_timeout >= 0 and time.time() - stime >= wait_timeout:
                return False
            time.sleep(1)
        return True

    def main(self):
        while not self.terminate_flag:
            if self.stop_flag:
                self.is_running = False
                if self.stopped_time is None:
                    self.stopped_time = time.time()
                self.stopped = True
                time.sleep(1)
                continue
            self.is_running = True
            try:
                try:
                    self.service_loop()
                except LoopIdle:
                    self.on_loop_idle()
                except ServiceStop:
                    self.stop(wait=False)
                except InterruptedError:
                    self.terminate(wait=False)
                except ServiceTerminate:
                    self.terminate(wait=False)
                except Exception as error:
                    self.on_loop_error(error)
                self.on_loop_finished()
            except ServiceStop:
                self.stop(wait=False)
            except InterruptedError:
                self.terminate(wait=False)
            except ServiceTerminate:
                self.terminate(wait=False)
            except Exception as error:
                logger.exception("Service main got unknown error.")
        self.terminated_time = time.time()
        self.terminated = True
        self.is_running = False

    def service_loop(self):
        raise NotImplementedError()

    def on_loop_idle(self):
        pass

    def on_loop_error(self, error):
        pass

    def on_loop_finished(self):
        pass


class Service(ServiceBase):

    def __init__(self, service_loop, kwargs=None, loop_interval=0, server=None, name=None, on_loop_error=None, on_loop_idle=None, on_loop_finished=None):
        self.service_loop_callback = service_loop
        self.kwargs = kwargs or {}
        self.server = server
        self.name = name or service_loop.__name__
        self.on_loop_error_callback = on_loop_error
        self.on_loop_idle_callback = on_loop_idle
        self.on_loop_finished_callback = on_loop_finished
        self.loop_interval = loop_interval
        super().__init__()

    def service_loop(self):
        self.service_loop_callback(**self.kwargs)
        if self.loop_interval and isinstance(self.loop_interval, (int, float)):
            time.sleep(self.loop_interval)

    def on_loop_idle(self):
        if callable(self.on_loop_idle_callback):
            self.on_loop_idle_callback()

    def on_loop_error(self, error):
        if callable(self.on_loop_error_callback):
            self.on_loop_error_callback(error)

    def on_loop_finished(self):
        if callable(self.on_loop_finished_callback):
            self.on_loop_finished_callback()


class SimpleProducerConsumerServerBase(object):
    
    default_queue_size = 0
    default_consume_pull_timeout = 5
    default_produce_loop_interval = 0
    default_producer_number = 1
    default_consumer_number = 5

    def __init__(self, server_name=None, queue_size=None, consume_pull_timeout=None, produce_loop_interval=None, producer_number=None, consumer_number=None):
        self.server_name = server_name or self.__class__.__name__
        self.queue_size = queue_size or self.default_queue_size
        self.consume_pull_timeout = consume_pull_timeout or self.default_consume_pull_timeout
        self.produce_loop_interval = produce_loop_interval or self.default_produce_loop_interval
        self.producer_number = producer_number or self.default_producer_number
        self.consumer_number = consumer_number or self.default_consumer_number
        self.queue = Queue(maxsize=self.queue_size)
        self._producers = Queue()
        self._consumers = Queue()

    @property
    def producers(self):
        return list(self._producers.queue)
    
    @property
    def consumers(self):
        return list(self._consumers.queue)

    def _produce(self):
        logger.debug("doing _produce")
        tasks = []
        try:
            tasks = self.produce()
            if not tasks:
                raise LoopIdle()
        except LoopIdle as error:
            logger.debug("doing produce got LoopIdle error.")
            self.on_produce_idle()
        except ServiceStop as error:
            raise error
        except ServiceTerminate as error:
            raise error
        except Exception as error:
            logger.exception("doing produce got unknown error.")
            self.on_produce_error(error)
        logger.debug("doing produce got tasks={0}".format(tasks))
        for task in tasks:
            self.queue.put(task, block=False)

    def produce(self):
        raise NotImplementedError()

    def _consume(self):
        logger.debug("doing _consume")
        task = None
        try:
            task = self.queue.get(timeout=self.consume_pull_timeout)
            logger.debug("doing _consume got task={}".format(task))
        except Empty as error:
            self.on_consume_idle()
        if task:
            try:
                self.consume(task)
            except ServiceStop as error:
                raise error
            except InterruptedError as error:
                raise error
            except ServiceTerminate as error:
                raise error
            except Exception as error:
                self.on_consume_error(task, error)

    def consume(self, task):
        raise NotImplementedError()

    def on_produce_error(self, error):
        pass

    def on_produce_finished(self):
        pass

    def on_produce_idle(self):
        pass

    def on_consume_error(self, task, error):
        pass

    def on_consume_finished(self):
        pass

    def on_consume_idle(self):
        pass

    def start(self):
        self.start_producers()
        self.start_consumers()

    def stop(self, wait=True, wait_timeout=-1):
        for producer in self.producers:
            producer.stop(wait=False)
        for consumer in self.consumers:
            consumer.stop(wait=False)
        self.join(wait, wait_timeout)

    def join(self, wait=True, wait_timeout=-1):
        stime = time.time()
        while True:
            living_producers = 0
            living_consumers = 0
            for service in self.producers:
                if service.is_running:
                    living_producers += 1
            for service in self.consumers:
                if service.is_running:
                    living_consumers += 1
            if living_producers == 0 and living_consumers == 0:
                return True
            if not wait:
                return False
            if wait_timeout >= 0 and time.time() - stime >= wait_timeout:
                return False
            time.sleep(1)

    def start_producers(self):
        for index in range(self.producer_number):
            name = self.server_name + ":producer#{0}".format(index+1)
            producer = Service(self._produce, server=self, name=name, loop_interval=self.produce_loop_interval, on_loop_error=self.on_produce_error, on_loop_idle=self.on_produce_idle, on_loop_finished=self.on_produce_finished)
            producer.start()
            self._producers.put(producer)
    
    def start_consumers(self):
        for index in range(self.consumer_number):
            name = self.server_name + ":consumer#{0}".format(index+1)
            consumer = Service(self._consume, server=self, name=name, on_loop_error=self.on_consume_error, on_loop_idle=self.on_consume_idle, on_loop_finished=self.on_consume_finished)
            consumer.start()
            self._consumers.put(consumer)


class SimpleProducerConsumerServer(SimpleProducerConsumerServerBase):

    def __init__(self,
            produce=None,
            consume=None,
            produce_kwargs=None,
            consume_kwargs=None,
            server_name=None,
            queue_size=None,
            consume_pull_timeout=None,
            produce_loop_interval=None,
            producer_number=None,
            consumer_number=None,
            on_produce_error=None,
            on_produce_finished=None,
            on_produce_idle=None,
            on_consume_error=None,
            on_consume_finished=None,
            on_consume_idle=None,
            ):
        self.produce_callback = produce
        self.produce_callback_kwargs = produce_kwargs or {}
        self.consume_callback = consume
        self.consume_callback_kwargs = consume_kwargs or {}
        self.on_produce_error_callback = on_produce_error
        self.on_produce_finished_callback = on_produce_finished
        self.on_produce_idle_callback = on_produce_idle
        self.on_consume_error_callback = on_consume_error
        self.on_consume_finished_callback = on_consume_finished
        self.on_consume_idle_callback = on_consume_idle
        super().__init__(server_name=server_name, queue_size=queue_size, consume_pull_timeout=consume_pull_timeout, produce_loop_interval=produce_loop_interval, producer_number=producer_number, consumer_number=consumer_number)

    def produce(self):
        if callable(self.produce_callback):
            return self.produce_callback(**self.produce_callback_kwargs)

    def consume(self, task):
        if callable(self.consume_callback):
            return self.consume_callback(task, **self.consume_callback_kwargs)

    def on_produce_error(self, error):
        if self.on_produce_error_callback:
            return self.on_produce_error_callback(error)

    def on_produce_finished(self):
        if self.on_produce_finished_callback:
            self.on_produce_finished_callback()

    def on_produce_idle(self):
        if self.on_produce_idle_callback:
            return self.on_produce_idle_callback()

    def on_consume_error(self, task, error):
        if self.on_consume_error_callback:
            return self.on_consume_error_callback(task, error)

    def on_consume_finished(self, task):
        if self.on_consume_finished_callback:
            return self.on_consume_finished_callback(task)

    def on_consume_idle(self):
        if self.on_consume_idle_callback:
            return self.on_consume_idle_callback()

