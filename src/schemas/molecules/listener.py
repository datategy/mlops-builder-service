from typing import Annotated

from pydantic import BaseModel, SecretStr, StringConstraints

from src.models.listener_broker import ListenerBroker as ListenerBrokerDB
from src.models.listener_http import ApiKey as ApiKeyDB
from src.models.listener_http import ListenerHttp as ListenerHttpDB


class ApiKey(BaseModel):
    friendly_name: Annotated[str, StringConstraints(max_length=100)]
    token: str
    can_create_new_api_keys: bool
    store_inference_data: bool

    def create_db_model(self):
        return ApiKeyDB(
            friendly_name=self.friendly_name,
            token=self.token,
            can_create_new_api_keys=self.can_create_new_api_keys,
            store_inference_data=self.store_inference_data,
        )


class ListenerHTTP(BaseModel):
    n_workers: int
    n_threads: int
    api_keys: list[ApiKey]

    def create_db_model(self):
        api_keys = [api_key.create_db_model() for api_key in self.api_keys]
        listener = ListenerHttpDB(
            n_workers=self.n_workers, n_threads=self.n_threads, api_keys=api_keys
        )

        return listener


class ListenerBroker(BaseModel):
    broker_host: str
    broker_port: int
    broker_username: str
    broker_password: SecretStr
    broker_topic: str

    def create_db_model(self):
        return ListenerBrokerDB(
            broker_host=self.broker_host,
            broker_port=self.broker_port,
            broker_username=self.broker_username,
            broker_password=self.broker_password.get_secret_value(),
            broker_topic=self.broker_topic,
        )


type Listener = ListenerHTTP | ListenerBroker
