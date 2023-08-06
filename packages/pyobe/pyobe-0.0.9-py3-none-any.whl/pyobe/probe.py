from .logger import get_logger
from .__VERSION__ import VERSION
import aiohttp
import asyncio
from datetime import datetime
import uuid
from enum import Enum


class ProbeStatus(Enum):
  STARTING = 0
  PROBING = 1
  FINISHED = 2
  FAILED = 3


class ProbeOptions():
  name = 'Probe'
  token = ''
  interval = 0
  concurrency = 128
  timeout = 10
  log_level = 'INFO'
  console_output = 5
  upload_data = False
  upload_interval = 60
  user_agent = f'Pyobe ver.{VERSION}'
  centre_url = 'http://localhost:8080'


class Probe():

  def __init__(self, options: ProbeOptions = ProbeOptions()):
    self.interval = options.interval
    self.concurrency = options.concurrency
    self.timeout = options.timeout
    self.name = options.name
    self.log_level = options.log_level
    self.console_output = options.console_output
    self.upload_data = options.upload_data
    self.upload_interval = options.upload_interval
    self.user_agent = options.user_agent
    self.token = options.token
    self.centre_url = options.centre_url

    self.logger = get_logger(self.name, self.log_level)
    self.version = VERSION

  async def gen_url(self):
    for _ in range(100):
      yield 'https://www.google.com'

  async def on_url(self, url: str) -> aiohttp.ClientResponse:
    return await self.session.get(url)

  async def on_response(self, res: aiohttp.ClientResponse):
    pass

  def start(self):
    self.logger.info(f'>> Probe ver.{VERSION} <<')
    self.logger.info(f'Using User-Agent: {self.user_agent}')
    self.logger.info(f'Download Interval: {self.interval}')
    self.logger.info(f'Download Concurrency: {self.concurrency}')
    self.logger.info(f'Request timeout: {self.timeout} second(s)')
    self.logger.info(f'Console stats output per {self.timeout} second(s)')
    self.logger.info(f'Probe is starting...')
    self.loop = asyncio.get_event_loop()
    self.loop.set_debug(False)
    self.loop.run_until_complete(self._run())

  async def _init(self):
    self.logger.info(f'Probe is initializing...')
    timeout = aiohttp.ClientTimeout(total=self.timeout)
    self.session = aiohttp.ClientSession(timeout=timeout)
    self.start_time = datetime.now()
    self.stats = {
        'UUID': str(uuid.uuid4()),
        'Name': self.name,
        'UrlCount': 0,
        'ErrCount': 0,
        'ResCount': 0,
        'Status': ProbeStatus.STARTING.value,
    }
    await self._upload_data()

  async def _run(self):
    self.logger.info(f'Probe is running...')
    await self._init()
    self.logger.info(f'Generating URL...')
    self.logger.info(f'Start Logger...')
    record_task = asyncio.create_task(self._record_stats())
    url_generator = self.gen_url()
    sem = asyncio.Semaphore(self.concurrency)
    self.logger.info(f'Start Probing...')
    self.stats['Status'] = ProbeStatus.PROBING.value
    await self._upload_data()
    async for url in url_generator:
      try:
        self.stats['UrlCount'] += 1
        await sem.acquire()
        self.loop.create_task(self._request(url, sem))
      except Exception as e:
        self.logger.exception(e)
      finally:
        await asyncio.sleep(self.interval)
    while sem._value != self.concurrency:
      await asyncio.sleep(0.1)
    self._print_finish_log()
    self.stats['Status'] = ProbeStatus.FINISHED.value
    await record_task
    await self._upload_data()
    await self.session.close()

  async def _record_stats(self):
    count = 0
    while self.stats['Status'] != ProbeStatus.FINISHED.value:
      count += 1
      await asyncio.sleep(1)
      if self.stats['Status'] == ProbeStatus.FINISHED.value:
        return
      if self.console_output > 0 and count % self.console_output == 0:
        end_time = datetime.now()
        time_delta = end_time - self.start_time
        total_seconds = time_delta.total_seconds()
        self.logger.info(
            f"URL Count: {self.stats['UrlCount']} [{int(self.stats['UrlCount'] / total_seconds * 60)}/min], "
            +
            f"Res Count: {self.stats['ResCount']} [{int(self.stats['ResCount'] / total_seconds * 60)}/min]"
        )
      if count % self.upload_interval == 0:
        await self._upload_data()

  def _print_finish_log(self):
    end_time = datetime.now()
    time_delta = end_time - self.start_time
    total_seconds = time_delta.total_seconds()
    minutes = int(total_seconds / 60 % 60)
    hours = int(total_seconds / 60 / 60)
    self.logger.info('Probe Task Finished!')
    self.logger.info(
        f"URL Count: {self.stats['UrlCount']} [{int(self.stats['UrlCount'] / total_seconds * 60)}/min]"
    )
    self.logger.info(
        f"Res Count: {self.stats['ResCount']} [{int(self.stats['ResCount'] / total_seconds * 60)}/min]"
    )
    self.logger.info(f"From: {self.start_time}")
    self.logger.info(f"To  : {end_time}")
    self.logger.info(f"Time Delta: {hours}h, {minutes}min ")

  async def _request(self, url: str, sem: asyncio.Semaphore):
    try:
      res = None
      self.logger.debug(f'Probing {url}')
      res = await self.on_url(url)
      self.stats['ResCount'] += 1
      self.logger.debug(f'Analyzing {url}')
      await self.on_response(res)
    except Exception as e:
      self.logger.exception(e)
    finally:
      sem.release()
      if res is not None:
        res.close()

  async def _upload_data(self):
    if self.upload_data:
      _ = await self.session.post(f'{self.centre_url}/stat',
                                  data=self.stats,
                                  headers={
                                      "token": self.token,
                                      "User-Agent": self.user_agent
                                  })


if __name__ == '__main__':
  options = ProbeOptions()
  options.token = '6a3b04b5-7ff6-11eb-b579-00ff73dc4525'
  options.name = 'test'
  options.upload_data = True
  p = Probe(options)
  p.start()