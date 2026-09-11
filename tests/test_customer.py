from app.customer import Customer
import pytest



# Reusable test fixture providing a valid Customer.
# Individual tests can modify this instance without repeating
# the standard Customer setup.


@pytest.fixture
def test_customer():
    customer = Customer(
        customer_id="PA-5054",
        customer_type="PARTNER",
        first_name="Losugan",
        last_name="Sivasuthan",
        email="test@test.no",
        phone_number="+47 21390016",
    )

    return customer


# Invalid customer types should be rejected during creation.
def test_customer_rejects_invalid_customer_type():
    with pytest.raises(ValueError):
        Customer(
            customer_id="W-1002",
            customer_type="VACATION",
            first_name="Mona",
            last_name="Lisa",
            email="test4@gmail.com",
            phone_number="+49243434324",
        )


# Customer IDs must follow the prefix convention of their customer type.
# Parametrization allows the same business rule to be tested with
# multiple invalid combinations without duplicating the test.
@pytest.mark.parametrize(
    "customer_id, customer_type",
    [("LE-5054", "PARTNER"), ("LE-5052", "BUSINESS")],
)
def test_customer_id_must_match_customer_type(customer_id, customer_type):
    with pytest.raises(ValueError):
        Customer(
            customer_id=customer_id,
            customer_type=customer_type,
            first_name="Ola",
            last_name="Normann",
            email="test3@gmail.com",
            phone_number="+4721213232",
        )


# Customer names can be updated with valid values.
def test_customer_can_edit_last_name(test_customer):
    test_customer.edit_last_name("Hansen")

    assert test_customer.last_name == "Hansen"


# Contact information can be updated as long as
# the Customer retains at least one contact method.
def test_customer_can_edit_phone_number(test_customer):
    test_customer.edit_phone_number("+47 46774925")

    assert test_customer.phone_number == "+47 46774925"


def test_customer_can_edit_first_name(test_customer):

    test_customer.edit_first_name("David")

    assert test_customer.first_name == "David"


def test_customer_can_edit_email(test_customer):

    test_customer.edit_email("outlook@outlook.com")

    assert test_customer.email == "outlook@outlook.com"


# A Customer cannot remove the phone number when no email is available.
def test_customer_cannot_remove_phone_number_without_email(test_customer):
    test_customer.email = ""
    with pytest.raises(ValueError):
        test_customer.edit_phone_number("")


# A Customer cannot remove the email when no phone number is available.
def test_customer_cannot_remove_email_without_phone_number(test_customer):
    test_customer.phone_number = ""
    with pytest.raises(ValueError):
        test_customer.edit_email("")


# First and last name are mandatory when creating a Customer.
def test_customer_must_have_valid_first_name():
    with pytest.raises(ValueError):
        Customer(
            customer_id="LE-5045",
            customer_type="LEISURE",
            first_name="",
            last_name="Normann",
            email="test@test.no",
            phone_number="+39066535332",
        )


# Required names cannot be changed to an empty value.
def test_customer_cannot_edit_first_name_to_empty(test_customer):
    with pytest.raises(ValueError):
        test_customer.edit_first_name("")


def test_customer_must_have_valid_last_name():
    with pytest.raises(ValueError):
        Customer(
            customer_id="LE-2345",
            customer_type="LEISURE",
            first_name="Michael",
            last_name="",
            email="test6@test.no",
            phone_number="+47 77494928",
        )


def test_customer_must_at_least_have_one_contact_detail():
    with pytest.raises(ValueError):
        Customer(
            customer_id="LE-5060",
            customer_type="LEISURE",
            first_name="Lars",
            last_name="Monsen",
            email="",
            phone_number="",
        )


def test_customer_cannot_edit_last_name_to_empty(test_customer):
    with pytest.raises(ValueError):
        test_customer.edit_last_name("")
