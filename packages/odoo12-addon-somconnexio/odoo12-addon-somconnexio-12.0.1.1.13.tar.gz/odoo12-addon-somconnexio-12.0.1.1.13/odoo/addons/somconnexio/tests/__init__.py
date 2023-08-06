from .models import test_subscription_request
from .models import test_product_category_technology_supplier
from .models import test_broadband_isp_info
from .models import test_contract
from .models import test_coop_agreement
from .models import test_service_supplier
from .models import test_crm_lead
from .models import test_crm_lead_line
from .models import test_mobile_isp_info
from .models import test_res_partner
from .models import test_res_partner_bank
from .models import test_production_lot
from .models import test_stock_move_line
from .models import test_opencell_configuration_wrapper
from .models import test_account_invoice
from .models import test_account_move_line

from .services import test_account_invoice_service
from .services import test_contract_contract_service
from .services import test_crm_lead_service
from .services import test_subscription_request_service
from .services import test_provider_service
from .services import test_res_partner_service
from .services import test_discovery_channel_service
from .services import test_vat_normalizer

from .opencell_models import test_crm_account_hierarchy
from .opencell_models import test_address
from .opencell_models import test_description
from .opencell_models import test_customer
from .opencell_models import test_subscription
from .opencell_models import test_opencell_service_codes

from .opencell_services import test_crm_account_hierarchy_service
from .opencell_services import test_crm_account_hierarchy_strategy
from .opencell_services import test_subscription_service
from .opencell_services import test_contract_service

from .otrs_factories import test_customer_data_from_res_partner
from .otrs_factories import test_adsl_data_from_crm_lead_line
from .otrs_factories import test_fiber_data_from_crm_lead_line
from .otrs_factories import test_mobile_data_from_crm_lead_line

from .wizards import test_crm_leads_validate_wizard
from .wizards import test_crm_lead_lines_validate_wizard
from .wizards import test_contract_iban_change_wizard
from .wizards import test_contract_holder_change
from .wizards import test_contract_email_change_wizard
from .wizards import test_contract_address_change_wizard
from .wizards import test_contract_one_shot_request_wizard
from .wizards import test_contract_tariff_change_wizard
from .wizards import test_contract_invoice_payment_wizard
from .wizards import test_create_subscription_from_partner
from .wizards import test_create_lead_from_partner_wizard

from .listeners import test_partner_bank_listener

from .somoffice import test_user
