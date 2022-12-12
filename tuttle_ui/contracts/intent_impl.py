import datetime

from typing import Optional, Mapping
from core.models import Cycle, TimeUnit


from clients.client_model import Client
from core.abstractions import ClientStorage
from core.models import IntentResult

from .contract_model import Contract
from .data_source_impl import ContractDataSourceImpl
from clients.data_source_impl import ClientDataSourceImpl
from contacts.data_source_impl import ContactDataSourceImpl
from contacts.contact_model import Contact


class ContractsIntentImpl:
    def __init__(self, local_storage: ClientStorage):
        self.clients_data_source = ClientDataSourceImpl()
        self.contacts_data_source = ContactDataSourceImpl()
        self.data_source = ContractDataSourceImpl()
        self.local_storage = local_storage

        self.all_contracts_cache: Mapping[str, Contract] = None
        self.completed_conracts_cache: Mapping[str, Contract] = None
        self.active_contracts_cache: Mapping[str, Contract] = None
        self.upcoming_contracts_cache: Mapping[str, Contract] = None

    def get_contract_by_id(self, contractId) -> IntentResult:
        result = self.data_source.get_contract_by_id(contractId)
        if not result.was_intent_successful:
            result.error_msg = "TODO -- error message"
        return result

    def get_all_clients_as_map(self) -> Mapping[int, Client]:
        result = self.clients_data_source.get_all_clients_as_map()
        if result.was_intent_successful:
            return result.data
        else:
            return {}

    def get_all_contacts_as_map(self) -> Mapping[int, Contact]:
        result = self.contacts_data_source.get_all_contacts_as_map()
        if result.was_intent_successful:
            return result.data
        else:
            return {}

    def save_client(self, client: Client) -> IntentResult:
        return self.clients_data_source.save_client(client=client)

    def save_contract(
        self,
        title: str,
        signature_date: datetime.date,
        start_date: datetime.date,
        end_date: Optional[datetime.date],
        client: Client,
        rate: str,
        currency: str,
        VAT_rate: str,
        unit: TimeUnit,
        units_per_workday: str,
        volume: Optional[str],
        term_of_payment: Optional[str],
        billing_cycle: Cycle = Cycle.hourly,
        is_completed: bool = False,
        contract: Optional[Contract] = None,
    ) -> IntentResult:
        return self.data_source.save_contract(
            title=title,
            signature_date=signature_date,
            start_date=start_date,
            end_date=end_date,
            client=client,
            rate=rate,
            currency=currency,
            VAT_rate=VAT_rate,
            unit=unit,
            units_per_workday=units_per_workday,
            volume=volume,
            term_of_payment=term_of_payment,
            billing_cycle=billing_cycle,
            is_completed=is_completed,
            contract=contract,
        )

    def get_all_contracts_as_map(self) -> Mapping[int, Contract]:
        if self.all_contracts_cache:
            # return cached results
            return self.all_contracts_cache
        self._clear_cached_results()
        result = self.data_source.get_all_contracts_as_map()
        if result.was_intent_successful:
            self.all_contracts_cache = result.data
        else:
            self.all_contracts_cache = {}
        return self.all_contracts_cache

    def get_completed_contracts(self) -> Mapping[str, Contract]:
        if not self.completed_conracts_cache:
            self.completed_conracts_cache = {}
            for key in self.all_contracts_cache:
                c = self.all_contracts_cache[key]
                if c.is_completed:
                    self.completed_conracts_cache[key] = c
        return self.completed_conracts_cache

    def get_active_contracts(self):
        if not self.active_contracts_cache:
            self.active_contracts_cache = {}
            for key in self.all_contracts_cache:
                c = self.all_contracts_cache[key]
                if c.is_active():
                    self.active_contracts_cache[key] = c
        return self.active_contracts_cache

    def get_upcoming_contracts(self):
        if not self.upcoming_contracts_cache:
            self.upcoming_contracts_cache = {}
            for key in self.all_contracts_cache:
                c = self.all_contracts_cache[key]
                if c.is_upcoming():
                    self.upcoming_contracts_cache[key] = c
        return self.upcoming_contracts_cache

    def _clear_cached_results(self):
        self.all_contracts_cache = None
        self.completed_conracts_cache = None
        self.active_contracts_cache = None
        self.upcoming_contracts_cache = None
