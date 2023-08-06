from odoo.tests import TransactionCase
from mock import Mock, patch
import mock
import factory
from ...opencell_services.crm_account_hierarchy_service import \
    CRMAccountHierarchyFromContractService

from ..factories import ContractFactory
from pyopencell.exceptions import PyOpenCellAPIException


class OpenCellConfigurationFake:
    seller_code = 'SC'
    customer_category_code = 'CLIENT'


class OpenCellCustomerResource:
    """
    Represents an OpenCell Customer Resource.
    """

    def __init__(self, code, email=None, iban=None):
        self.code = code
        self.email = email or factory.Faker("email")
        self.iban = iban or factory.Faker("iban")

    @property
    def customerAccounts(self):
        return {
            "customerAccount": [{
                "code": self.code,
                "contactInformation": {
                    "email": self.email,
                },
                "methodOfPayment": [{
                    "bankCoordinates": {
                        "iban": self.iban
                    }
                }]
            }]}


class CRMAccountHierarchyFromContractServiceTests(TransactionCase):

    def setUp(self):
        super().setUp()
        self.contract = ContractFactory()
        self.opencell_configuration = OpenCellConfigurationFake()

    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionService',  # noqa
        return_value=Mock(spec=['subscription'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.ServicesFromContract',  # noqa
        return_value=Mock(spec=['services_to_activate'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_strategies.Customer',  # noqa
        spec=['get']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Access',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.AccessFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Subscription',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.CRMAccountHierarchy',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.CRMAccountHierarchyFromContract',  # noqa
        return_value=Mock(spec=['to_dict', 'code'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Customer',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.CustomerFromPartner',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    def test_create_customer_hierarchy_in_opencell(
        self,
        MockCustomerFromPartner,
        MockCustomer,
        MockCRMAccountHierarchyFromContract,
        MockCRMAccountHierarchy,
        MockSubscriptionFromContract,
        MockSubscription,
        MockAccessFromContract,
        MockAccess,
        MockCustomerInStrategies,
        MockServicesFromContract,
        MockSubscriptionService,
    ):

        MockCustomerFromPartner.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockAccessFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockCustomerInStrategies.get.side_effect = PyOpenCellAPIException(
            verb=mock.ANY, url=mock.ANY, status=400, body=mock.ANY
        )

        services_to_activate = {"services": "EXAMPLE_SERVICE"}
        one_shots_to_activate = []
        MockServicesFromContract.return_value.services_to_activate.return_value = services_to_activate, one_shots_to_activate  # noqa
        MockSubscriptionService.return_value.subscription = Mock(
            spec=['activate']
        )

        CRMAccountHierarchyFromContractService(
            self.contract,
            self.opencell_configuration
        ).run()

        MockCustomerFromPartner.assert_called_with(
            self.contract.partner_id,
            self.opencell_configuration
        )
        MockCustomer.create.assert_called_with(
            **MockCustomerFromPartner.return_value.to_dict.return_value
        )
        MockCRMAccountHierarchyFromContract.assert_called_with(
            self.contract,
            str(self.contract.partner_id.id)+"_0"
        )
        MockCRMAccountHierarchy.create.assert_called_with(
            **MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionFromContract.assert_called_with(
            self.contract,
            MockCRMAccountHierarchyFromContract.return_value.code
        )
        MockSubscription.create.assert_called_with(
            **MockSubscriptionFromContract.return_value.to_dict.return_value
        )
        MockAccessFromContract.assert_called_with(
            self.contract
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionService.return_value.subscription.activate.assert_called_with(  # noqa
            services_to_activate
        )

    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionService',  # noqa
        return_value=Mock(spec=['subscription'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.ServicesFromContract',  # noqa
        return_value=Mock(spec=['services_to_activate'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_strategies.Customer',  # noqa
        spec=['get']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Access',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.AccessFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Subscription',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.CRMAccountHierarchy',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.CRMAccountHierarchyFromContract',  # noqa
        return_value=Mock(spec=['to_dict', 'code'])
    )
    def test_create_customer_account_hierarchy_in_opencell(
        self,
        MockCRMAccountHierarchyFromContract,
        MockCRMAccountHierarchy,
        MockSubscriptionFromContract,
        MockSubscription,
        MockAccessFromContract,
        MockAccess,
        MockCustomerInStrategies,
        MockServicesFromContract,
        MockSubscriptionService,
    ):

        MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockAccessFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionService.return_value.subscription = Mock(
            spec=['activate']
        )
        services_to_activate = {"services": "EXAMPLE_SERVICE"}
        one_shots_to_activate = []
        MockServicesFromContract.return_value.services_to_activate.return_value = services_to_activate, one_shots_to_activate  # noqa

        expected_email = "expeceted@email.com"
        customer = OpenCellCustomerResource(
            code="{}_0".format(self.contract.partner_id.id),
            email=expected_email
        )
        MockCustomerInStrategies.get.return_value.customer = customer

        CRMAccountHierarchyFromContractService(
            self.contract,
            self.opencell_configuration
        ).run()

        MockCRMAccountHierarchyFromContract.assert_called_with(
            self.contract,
            str(self.contract.partner_id.id)+"_0_1"
        )
        MockCRMAccountHierarchy.create.assert_called_with(
            **MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionFromContract.assert_called_with(
            self.contract,
            MockCRMAccountHierarchyFromContract.return_value.code
        )
        MockSubscription.create.assert_called_with(
            **MockSubscriptionFromContract.return_value.to_dict.return_value
        )
        MockAccessFromContract.assert_called_with(
            self.contract
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionService.return_value.subscription.activate.assert_called_with(  # noqa
            services_to_activate
        )

    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionService',  # noqa
        return_value=Mock(spec=['subscription'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.ServicesFromContract',  # noqa
        return_value=Mock(spec=['services_to_activate'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_strategies.Customer',  # noqa
        spec=['get']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Access',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.AccessFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Subscription',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    def test_create_subscription_in_opencell(
        self,
        MockSubscriptionFromContract,
        MockSubscription,
        MockAccessFromContract,
        MockAccess,
        MockCustomerInStrategies,
        MockServicesFromContract,
        MockSubscriptionService,
    ):
        MockSubscriptionFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockAccessFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionService.return_value.subscription = Mock(
            spec=['activate']
        )
        services_to_activate = {"services": "EXAMPLE_SERVICE"}
        one_shots_to_activate = []
        MockServicesFromContract.return_value.services_to_activate.return_value = services_to_activate, one_shots_to_activate  # noqa

        expected_email = "expected@email.com"
        self.contract.invoice_partner_id.email = expected_email
        expected_iban = "ES00 0000 0000 0000 0000"
        self.contract.mandate_id.partner_bank_id.sanitized_acc_number = expected_iban
        expected_customer_code = "{}_0_1".format(self.contract.partner_id.id)
        customer = OpenCellCustomerResource(
            code=expected_customer_code, email=expected_email, iban=expected_iban
        )
        MockCustomerInStrategies.get.return_value.customer = customer

        CRMAccountHierarchyFromContractService(
            self.contract,
            self.opencell_configuration
        ).run()

        MockSubscriptionFromContract.assert_called_with(
            self.contract,
            expected_customer_code
        )
        MockSubscription.create.assert_called_with(
            **MockSubscriptionFromContract.return_value.to_dict.return_value
        )
        MockAccessFromContract.assert_called_with(
            self.contract
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionService.return_value.subscription.activate.assert_called_with(  # noqa
            services_to_activate
        )

    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionService',  # noqa
        return_value=Mock(spec=['subscription', 'create_one_shot'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.ServicesFromContract',  # noqa
        return_value=Mock(spec=['services_to_activate'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_strategies.Customer',  # noqa
        spec=['get']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Access',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.AccessFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.Subscription',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy_service.SubscriptionFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    def test_create_subscription_in_opencell_with_one_shots(
        self,
        MockSubscriptionFromContract,
        MockSubscription,
        MockAccessFromContract,
        MockAccess,
        MockCustomerInStrategies,
        MockServicesFromContract,
        MockSubscriptionService,
    ):
        MockSubscriptionFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockAccessFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionService.return_value.subscription = Mock(
            spec=['activate']
        )
        services_to_activate = {"services": "EXAMPLE_SERVICE"}
        one_shots_to_activate = ['ONE_SHOT_PRODUCT']
        MockServicesFromContract.return_value.services_to_activate.return_value = services_to_activate, one_shots_to_activate  # noqa

        expected_email = "expected@email.com"
        self.contract.invoice_partner_id.email = expected_email
        expected_iban = "ES00 0000 0000 0000 0000"
        self.contract.mandate_id.partner_bank_id.sanitized_acc_number = expected_iban
        expected_customer_code = "{}_0_1".format(self.contract.partner_id.id)
        customer = OpenCellCustomerResource(
            code=expected_customer_code, email=expected_email, iban=expected_iban
        )
        MockCustomerInStrategies.get.return_value.customer = customer

        CRMAccountHierarchyFromContractService(
            self.contract,
            self.opencell_configuration
        ).run()

        MockSubscriptionFromContract.assert_called_with(
            self.contract,
            expected_customer_code
        )
        MockSubscription.create.assert_called_with(
            **MockSubscriptionFromContract.return_value.to_dict.return_value
        )
        MockAccessFromContract.assert_called_with(
            self.contract
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionService.return_value.subscription.activate.assert_called_with(  # noqa
            services_to_activate
        )
        MockSubscriptionService.return_value.create_one_shot.assert_called_with(  # noqa
            one_shots_to_activate[0]
        )
