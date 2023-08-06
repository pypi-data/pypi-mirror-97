from otrs_somconnexio.otrs_models.customer_data import CustomerData


class CustomerDataFromResPartner:

    def __init__(self, partner):
        self.partner = partner

    def build(self):
        address = self._address()
        return CustomerData(
            id=self.partner.ref,
            vat_number=self.partner.vat,
            email=self.partner.email,
            phone=self.partner.mobile or self.partner.phone,
            name=self.partner.lastname,
            first_name=self.partner.firstname,
            street=address.full_street,
            zip=address.zip,
            city=address.city,
            subdivision="{}-{}".format(
                address.country_id.code,
                address.state_id.code
            ),
        )

    def _address(self):
        for address in self.partner.child_ids:
            if address.type == "invoice":
                return address
        return self.partner
