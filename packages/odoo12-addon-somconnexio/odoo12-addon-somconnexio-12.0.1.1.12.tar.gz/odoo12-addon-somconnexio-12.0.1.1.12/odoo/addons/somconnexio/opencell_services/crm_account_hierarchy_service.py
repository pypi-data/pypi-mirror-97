from pyopencell.resources.customer import Customer
from pyopencell.resources.crm_account_hierarchy import CRMAccountHierarchy
from pyopencell.resources.subscription import Subscription
from pyopencell.resources.access import Access

from ..opencell_models.customer import CustomerFromPartner
from ..opencell_models.crm_account_hierarchy import CRMAccountHierarchyFromContract
from ..opencell_models.subscription import SubscriptionFromContract
from ..opencell_models.access import AccessFromContract
from ..opencell_models.services import ServicesFromContract

from .opencell_exceptions import PyOpenCellException
from .crm_account_hierarchy_strategies import CRMAccountHierarchyStrategies
from .subscription_service import SubscriptionService


class CRMAccountHierarchyFromContractService(object):
    def __init__(self, contract, opencell_configuration):
        self.contract = contract
        self.partner = contract.partner_id
        self.strategy_actions = {
            'customer_hierarchy': self._create_customer_subscription,
            'customer_account_hierarchy': (
                self._create_subscription_from_crm_account_hierarchy
            ),
            "subscription": self._create_subscription
        }
        self.opencell_configuration = opencell_configuration

    def run(self):
        strategy, kwargs = CRMAccountHierarchyStrategies(self.contract).strategies()
        try:
            self.strategy_actions[strategy](**kwargs)
        except Exception as e:
            raise PyOpenCellException(str(e))

    def _create_customer_subscription(self, crm_account_hierarchy_code):
        self._create_customer()
        self._create_subscription_from_crm_account_hierarchy(crm_account_hierarchy_code)

    def _create_subscription_from_crm_account_hierarchy(
            self, crm_account_hierarchy_code):
        crm_account_hierarchy_code = self._create_crm_account_hierarchy(
            crm_account_hierarchy_code)
        self._create_subscription(crm_account_hierarchy_code=crm_account_hierarchy_code)

    def _create_customer(self):
        customer_from_partner = CustomerFromPartner(
            self.partner,
            self.opencell_configuration
        )
        Customer.create(**customer_from_partner.to_dict())

    def _create_crm_account_hierarchy(self, crm_account_hierarchy_code):
        crm_account_hierarchy_from_contract = CRMAccountHierarchyFromContract(
            self.contract,
            crm_account_hierarchy_code)
        CRMAccountHierarchy.create(**crm_account_hierarchy_from_contract.to_dict())
        return crm_account_hierarchy_from_contract.code

    def _create_subscription(self, crm_account_hierarchy_code):
        subscription_from_contract = SubscriptionFromContract(
            self.contract,
            crm_account_hierarchy_code)
        Subscription.create(**subscription_from_contract.to_dict())

        self._create_access()
        self._activate_services()

    def _create_access(self):
        access_from_contract = AccessFromContract(self.contract)
        Access.create(**access_from_contract.to_dict())

    def _activate_services(self):
        services_to_activate, one_shots_to_activate = ServicesFromContract(
            self.contract
        ).services_to_activate()
        if not services_to_activate:
            return

        subscription_service = SubscriptionService(
            self.contract
        )
        subscription_service.subscription.activate(services_to_activate)

        for one_shot in one_shots_to_activate:
            subscription_service.create_one_shot(one_shot)
