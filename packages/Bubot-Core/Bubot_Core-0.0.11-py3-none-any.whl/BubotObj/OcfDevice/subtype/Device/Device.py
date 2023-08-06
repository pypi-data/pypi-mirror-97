"""
TODO Проверка смены IP адреса и автоматическая замена на актуальный

"""

from .MainLoopMixin import MainLoopMixin
from Bubot.Helpers.ExtException import ExtException, ExtTimeoutError
# from .QueueMixin import QueueMixin
from Bubot.Core.OcfMessage import OcfRequest
from Bubot.Helpers.Helper import Helper
from .__init__ import __version__ as device_version
from os import path
import os
import json
import asyncio
import logging
import re


# _logger = logging.getLogger('OcfDevice')


class Device(MainLoopMixin):
    scheme = {}
    cache = {}
    file = __file__
    version = device_version
    platform_version = device_version
    template = True

    def __init__(self, **kwargs):
        MainLoopMixin.__init__(self, **kwargs)
        self.loop = kwargs.get('loop', asyncio.get_event_loop())

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.task = self.loop.create_task(self.main())
        self.loop.run_forever()

    @classmethod
    def find_first_config(cls, config_path, class_name):
        _list = os.listdir(config_path)
        pattern = re.compile('{0}.+.json'.format(class_name))
        for _file in _list:
            if os.path.isfile('{0}/{1}'.format(config_path, _file)):
                if pattern.match(_file):
                    return _file.split('.')[1]
        return None

    @classmethod
    def init_from_file(cls, **kwargs):
        kwargs['path'] = os.path.abspath(kwargs.get('path', './'))
        kwargs['log'] = kwargs['log'] if kwargs.get('log') else logging.getLogger()
        class_name = kwargs.get('class_name', cls.__name__)
        di = kwargs.get('di')
        config = {}
        if di is None:
            di = cls.find_first_config('{}'.format(kwargs['path']), class_name)
        if di:
            config_path = path.normpath('{0}/{1}.{2}.json'.format(kwargs['path'], class_name, di))
            try:
                with open(config_path, encoding='utf-8') as file:
                    config = json.load(file)
                    kwargs['log'].info('OcfDevice.init_from_file {0}.{1}'.format(class_name, di))
            except FileNotFoundError:
                kwargs['log'].warning('OcfDevice config not found {0}'.format(config_path))
            except Exception as e:
                raise ExtException(
                    7004,
                    detail='{0} {1}'.format(str(e), config_path),
                    action='OcfDevice.init_from_config',
                    dump=dict(
                        class_name=class_name,
                        di=di,
                    )
                )
        kwargs['class_name'] = class_name
        kwargs['di'] = di
        return cls.init_from_config(config, **kwargs)

    @classmethod
    def init_from_config(cls, config=None, **kwargs):
        cache = kwargs.get('cache', cls.cache)
        class_name = cls.__name__
        try:
            if config:
                class_name = config['/oic/d']['dmno']
        except KeyError:
            pass
        class_name = kwargs.get('class_name', class_name)
        try:
            self = cls.get_device_class(class_name)
            self = self(**kwargs)
        except Exception as err:
            raise ExtException(
                'Bad driver',
                detail=class_name,
                action='OcfDevice.init_from_config',
                parent=err,
                dump=dict(
                    config=config,
                    kwargs=kwargs
                )
            )
        try:
            self.data = self.get_default_config(self.__class__, Device, cache)
            if config:
                Helper.update_dict(self.data, config)
            if not self.get_device_id():
                self.set_device_id(kwargs.get('di'))

            # self.log = Logger(
            #     self,
            #     level=self.get_param('/oic/con', 'logLevel', 'error'),
            #     name='{0}:{1}'.format(self.__class__.__name__, self.get_device_id()[-5:]),
            #     log=kwargs.get('log')
            # )
            self.log = logging.getLogger('{0}:{1}'.format(self.__class__.__name__, self.get_device_id()[-5:]))
            self.log.setLevel(getattr(logging, self.get_param('/oic/con', 'logLevel', 'error').upper()))
            return self
        except Exception as e:
            raise ExtException(
                'Bad driver config',
                detail=class_name,
                action='OcfDevice.init_from_config',
                dump=dict(
                    config=config,
                    kwargs=kwargs
                )
            ) from e

    def get_default_config(self, current_class, root_class, cache):
        data = Helper.get_default_config(current_class, root_class, cache)
        data['/oic/d']['dmno'] = current_class.__name__
        data['/oic/d']['sv'] = self.version
        data['/oic/p']['mnpv'] = current_class.platform_version
        return data

    def save_config(self):
        def_data = self.get_default_config(self.__class__, Device, self.cache)
        data = Helper.compare(def_data, self.data)
        try:
            data[1].pop('/oic/mnt')
        except KeyError:
            pass

        try:
            with open(self.get_config_path(), 'w', encoding='utf-8') as file:
                json.dump(data[1], file, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            return {}
        return data

    async def request(self, operation, to, data=None, **kwargs):
        try:
            msg = OcfRequest(
                to=to,
                fr=self.link,
                op=operation,
                cn=data,
                # uri_path=link['href'],
                # operation=operation,
                # data=data,
                # code=kwargs.pop('code', 1),
                token=self.coap.token,
                mid=self.coap.mid,
                **kwargs
            )
            coap_msg, remote = msg.encode_to_coap()
            result = await self.coap.send_request(coap_msg, remote)
            return result
        except TimeoutError:
            raise ExtTimeoutError(action='request', dump=dict(op=operation, to=to, data=data, kwargs=kwargs)) from None
        except ExtException as err:
            raise ExtException(parent=err,
                               action='{}.request()'.format(self.__class__.__name__),
                               dump=dict(op=operation, to=to, data=data, kwargs=kwargs)) from None
        except Exception as err:
            raise ExtException(parent=err,
                               action='{}.request()'.format(self.__class__.__name__),
                               dump=dict(op=operation, to=to, data=data, kwargs=kwargs)) from None

    async def observe(self, to, callback=None):
        try:
            token = self.coap.token
            msg = OcfRequest(
                to=to,
                fr=self.link,
                op='retrieve',
                token=token,
                mid=self.coap.mid,
                obs=1 if callback is None else 0
            )
            coap_msg, remote = msg.encode_to_coap()
            await self.coap.send_multi_answer_request(coap_msg, remote, callback)
            if callback is None:
                del self.coap.answer[token]
        except TimeoutError as e:
            raise ExtTimeoutError(action='request',
                                  dump=dict(op='observe', to=to)) from None
        except ExtException as e:
            raise ExtException(parent=e,
                               action='{}.request()'.format(self.__class__.__name__),
                               dump=dict(op='observe', to=to)) from None
        except Exception as e:
            raise ExtException(parent=e,
                               action='{}.request()'.format(self.__class__.__name__),
                               dump=dict(op='observe', to=to)) from None

    async def discovery_resource(self, **kwargs):
        try:
            token = self.coap.token
            result = {}
            msg = OcfRequest(
                to=dict(href='/oic/res'),
                fr=self.link,
                op='retrieve',
                token=token,
                mid=self.coap.mid,
                multicast=True,
                **kwargs
            )
            coap_msg, remote = msg.encode_to_coap()
            if self.coap.ipv6:
                await self.coap.send_multi_answer_request(
                    coap_msg,
                    (self.coap.coap_discovery_ipv6[0], self.coap.multicast_port),
                    self.on_response_oic_res,
                    result
                )
            if self.coap.ipv4:
                await self.coap.send_multi_answer_request(
                    coap_msg,
                    (self.coap.coap_discovery_ipv4[0], self.coap.multicast_port),
                    self.on_response_oic_res,
                    result
                )
            await asyncio.sleep(2)
            result = self.coap.answer[token]['result']
            # del (self.coap.answer[token])
            return result

        except ExtException as e:
            raise Exception(e)
        except Exception as e:
            raise ExtException(e)

    async def find_resource_by_link(self, link):
        self.log.debug('find resource by di {0} href {1}'.format(link.di, link.href))

        links = await self.discovery_resource(
            query=dict(di=[link.di], href=[link.href]))
        if isinstance(links, dict):
            for di in links:
                if di == link.di:
                    for ref in links[di].links:
                        if ref == link.href:
                            return links[di].links[ref]
        return None
