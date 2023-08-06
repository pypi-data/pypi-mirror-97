import asyncio
import json
import logging
from typing import Optional

import aiohttp

from discovery.abc import BaseClient
from discovery.exceptions import ServiceNotFoundException
from discovery.filter import Filter
from discovery.service import service
from discovery.utils import select_one_rr

logging.getLogger(__name__).addHandler(logging.NullHandler())


class AioClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.managed_services = {}
        self._leader_id = None

    async def reconnect(self):
        # await self.agent.service.deregister(self.service.identifier)
        for key, value in self.managed_services.items():
            await self.service.deregister(value.get('id'))            
            svc = service(key, value.get('port'), check=value.get('check'))
            await self.service.register(svc)

        self.__id = await self.leader_current_id()

        logging.debug(f"Consul ID: {self.__id}")
        logging.info("Service successfully re-registered")

    async def leader_ip(self):
        leader_response = await self.status.leader()
        leader_response = await leader_response.json()
        consul_leader, _ = leader_response.split(":")
        return consul_leader

    async def get_consul_health(self):
        health_response = await self.health.service("consul")
        consul_instances = await health_response.json()
        return consul_instances

    async def leader_current_id(self):
        consul_leader = await self.leader_ip()
        consul_instances = await self.get_consul_health()

        current_id = [
            instance.get("Node").get("ID")
            for instance in consul_instances
            if instance.get("Node").get("Address") == consul_leader
        ]

        if current_id is not None:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id

    async def check_consul_health(self):
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    await self.reconnect()

            except aiohttp.ClientConnectorError:
                logging.error("failed to connect to discovery service...")
                logging.error(f"reconnect will occur in {self.timeout} seconds.")
#                await self.check_consul_health(self.service)
                await asyncio.sleep(self.timeout)
                await self.check_consul_health()

            except aiohttp.ServerDisconnectedError:
                logging.error(
                    "temporary loss of communication with the discovery server."
                )
                await asyncio.sleep(self.timeout)
#                await self.check_consul_health(self.service)
                await self.check_consul_health()

    async def find_service(self, name, fn=select_one_rr):
        response = await self.find_services(name)
        if not response:
            raise ServiceNotFoundException
        services = await response.json()
        return fn(services)

    async def find_services(self, name):
        services = await self.catalog.service(name)
        return services

    async def deregister(self, service_name) -> Optional[int]:
        status = None
        service = self.managed_services.get(service_name)
        if not service:
            # alterar para servicenotmanaged
            raise ServiceNotFoundException
        logging.info(service.get('id'))
        resp = await self.service.deregister(service.get('id'))
        self.managed_services.pop(service_name)
        if resp:
            status = resp.status
        return status

    async def register(self, service_name, service_port, check=None) -> Optional[int]:
        status = None
        svc = service(service_name, service_port, check=check)
        try:
            resp = await self.service.register(svc)
            status = resp.status
            data = await resp.text()
            logging.debug(data)
            self.managed_services[service_name] = {
                "id": f"{json.loads(svc).get('id')}",
                "port": service_port,
                "check": check
            }
            self.__id = await self.leader_current_id()
            logging.debug(f"Consul ID: {self.__id}")

        except aiohttp.ClientConnectorError:
            logging.error("Failed to connect to discovery...")

        return status


#    async def register_additional_check(self, check):
#        if not isinstance(check, Check):
#            raise TypeError("check must be Check instance.")
#
#        self.__discovery.agent.check.register(
#            check.name, check.value, service_id=self.service.identifier
#        )
#
#    async def deregister_additional_check(self, check):
#        if not isinstance(check, Check):
#            raise TypeError("check must be Check instance.")
#
#        self.__discovery.agent.check.deregister(check.identifier)
