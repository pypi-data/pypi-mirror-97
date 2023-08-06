from pyopencell.resources.crm_account_hierarchy import CRMAccountHierarchy
from .subscription_service import SubscriptionService
from ..opencell_models.crm_account_hierarchy import CRMAccountHierarchyFromContract


class ContractService:
    """
    Manage the Open Cell synchronization of the Contract model of Odoo.
    """

    def __init__(self, contract):
        self.contract = contract

    def update(self):
        subscription = SubscriptionService(self.contract).subscription
        crm_account_hierarchy_from_contract = CRMAccountHierarchyFromContract(
            self.contract, subscription.userAccount
        )
        CRMAccountHierarchy.update(**crm_account_hierarchy_from_contract.to_dict())
