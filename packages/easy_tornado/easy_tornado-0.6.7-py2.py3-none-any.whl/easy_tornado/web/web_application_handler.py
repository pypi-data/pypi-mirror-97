# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
import json
import time

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPResponse
from tornado.web import RequestHandler

from ..compat import C_StandardError
from ..compat import utf8decode
from ..utils.httpclient import json_print
from ..utils.logging import it_print
from ..utils.stringext import to_json
from ..utils.timeext import current_datetime


class WebApplicationHandler(RequestHandler):
  # 全局信息
  global_map = dict()

  # 错误信息
  error_mapper = dict()

  # 正常响应
  none = 0
  error_mapper[none] = 'none'

  # 无效请求(参数错误)
  invalid_request = 1001
  error_mapper[invalid_request] = 'request param is invalid'

  # 数据未找到
  not_found = 4004
  error_mapper[not_found] = 'not found'

  # 操作不支持
  not_support = 5001
  error_mapper[not_support] = 'not support'

  # 本系统错误
  system_error = 5002
  error_mapper[system_error] = 'system error'

  # 内部服务器错误
  internal_server = 5003
  error_mapper[internal_server] = 'internal server'

  # 调试模式
  debug = False

  # 开发模式
  devel = True

  # 作为后台进程运行
  daemon = True

  @staticmethod
  def setup_config(**kwargs):
    self = WebApplicationHandler
    self.debug = kwargs.pop('debug', self.debug)
    self.devel = kwargs.pop('devel', self.devel)
    self.daemon = kwargs.pop('daemon', self.daemon)

  @staticmethod
  def persist(**kwargs):
    pass

  @staticmethod
  def restore(**kwargs):
    self = WebApplicationHandler
    self.global_map.update(kwargs)

  # 加载为json数据
  def load_request_data(self):
    try:
      if self.debug:
        it_print(self.request.body)
      body = utf8decode(self.request.body)
      params = json.loads(body) if body != '' else dict()
      # 加入私有属性作为数据，否则params为空，被if not判断为真
      params['_uri'] = self.request.uri
      if self.debug:
        params['request_time'] = current_datetime()
        self.pretty_it_print(params)
    except ValueError:
      return False
    return params

  # 加载query数据
  def load_query_data(self):
    try:
      if self.debug:
        it_print(self.request.query)
      params = {
        k: [utf8decode(x) for x in v]
        for k, v in self.request.query_arguments.items()
      }
    except ValueError:
      return False
    return params

  # 异步转发请求
  @staticmethod
  def async_forward(url, data=None, callback=None,
                    method='POST', timeout=3600):
    if callback is None:
      def empty_fn(_):
        pass

      callback = empty_fn

    _data = dict()
    if data is not None:
      assert isinstance(data, dict)
      _data.update(data)

    json_data = to_json(_data)
    client = AsyncHTTPClient()
    future = client.fetch(
      url, body=json_data, method=method, request_timeout=timeout
    )

    def handle_future(_future):
      exc = future.exception()
      if isinstance(exc, HTTPError) and exc.response is not None:
        response = exc.response
      elif exc is not None:
        request = HTTPRequest(url)
        response = HTTPResponse(
          request, 599, error=exc,
          request_time=time.time() - request.start_time)
      else:
        response = _future.result()
      client.io_loop.add_callback(callback, response)

    future.add_done_callback(handle_future)

  # 同步转发请求
  async def forward(self, url, data=None, callback=None,
                    method='POST', timeout=3600):
    if callback is None:
      callback = self.response

    _data = dict()
    if data is not None:
      assert isinstance(data, dict)
      _data.update(data)

    json_data = to_json(_data)
    client = AsyncHTTPClient()
    response = await client.fetch(
      url, body=json_data, method=method, request_timeout=timeout
    )
    return callback(response)

  def success_response(self, data=None):
    self.error_response(self.none, self.error_mapper[self.none], data)

  def error_response(self, error_no=invalid_request,
                     error_desc=None, data=None):
    res = dict()
    if data is not None:
      assert isinstance(data, dict)
      res.update(data)
    res['errno'] = error_no
    if error_desc is None:
      error_desc = self.error_mapper[error_no]
    res['error'] = error_desc
    self.__json_response(res)

  def text_response(self, text):
    self.__output_response(text)

  def json_response(self, data):
    self.__json_response(data)

  def __json_response(self, data):
    if self.debug:
      data['response_time'] = current_datetime()
      self.pretty_it_print(data)
    self.__output_response(to_json(data, sort_keys=True))

  def __output_response(self, data):
    self.write(data)
    self.finish()

  # 默认响应处理器
  def response(self, response):
    try:
      if self.debug:
        it_print(response.body)
      result = json.loads(response.body)
    except ValueError:
      return self.error_response(error_no=self.system_error)
    return self.success_response(result)

  def data_received(self, chunk):
    pass

  @staticmethod
  def pretty_it_print(data):
    json_print(data)

  @staticmethod
  def exists(key):
    return key in WebApplicationHandler.global_map

  @staticmethod
  def store(key, value):
    self = WebApplicationHandler
    self.global_map[key] = value

  @staticmethod
  def release(key):
    self = WebApplicationHandler
    if self.exists(key):
      self.global_map.pop(key)

  @staticmethod
  def retrieve(key, default=None):
    self = WebApplicationHandler
    if self.exists(key):
      return self.global_map[key]
    return default

  @staticmethod
  def p(key, params, **kwargs):
    if key in params:
      return params[key]
    if 'default' in kwargs:
      return kwargs['default']
    raise C_StandardError(
      'parameter [{}] does not present'.format(key)
    )

  def q(self, key, params=None, multiple=False, type_fn=str, **kwargs):
    if params is None:
      params = self.load_query_data()

    if key not in params:
      if 'default' in kwargs:
        return kwargs['default']
      return C_StandardError(
        'query parameter [{}] does not present'.format(key)
      )

    values = params[key]
    if multiple:
      return [type_fn(x) for x in values]
    return type_fn(values[0])
