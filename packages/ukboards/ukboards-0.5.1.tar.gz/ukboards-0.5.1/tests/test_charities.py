#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test querying Charities Commision API."""

from typing import Final
from xml.etree import ElementTree

import pytest
from networkx import is_connected
from networkx.algorithms import bipartite
from requests import Response
from zeep import Client
from zeep.plugins import HistoryPlugin

from ukboards.charities import (
    CHARITY_COMMISSION_WSDL,
    CharitiesAuthPlugin,
    CharityIDType,
    check_registered_charity_number,
    get_charity_network,
    get_client,
)
from ukboards.utils import CharityAPIKeyType

CHARITY_COMMISSION_API: Final[str] = CHARITY_COMMISSION_WSDL.split("?")[0]

TEST_PHOTOGRAPHERS_GALLERY_NAME: Final[str] = (
    "THE PHOTOGRAPHERS' GALLERY LTD                    "
    "                                                  "
    "                                                  "
)

TEST_TAG_NS: Final[str] = "http://www.charitycommission.gov.uk/"

TEST_PHOTOGRAPHERS_CHARITY_NUMBER: Final[int] = 262548

TEST_API_KEY: Final[str] = "A-fake-test-key"

TATE_FOUNDATION_ID: Final[CharityIDType] = 1085314
TATE_FOUNDATION_NAME: Final[str] = "TATE FOUNDATION"


@pytest.fixture
def test_client(requests_mock, maxlen: int = 20):
    """A mock test client using the 19/12/2019 Charties Commission API."""
    history: HistoryPlugin = HistoryPlugin(maxlen=maxlen)
    auth: CharityAPIKeyType = CharitiesAuthPlugin(api_key_value=TEST_API_KEY)
    with open("tests/charities_api.wsdl", "r") as charities_api:
        requests_mock.get(CHARITY_COMMISSION_WSDL, text=charities_api.read())
        client: Client = get_client(plugins=[history, auth])
        assert hasattr(client.service, "GetCharitiesByName")
        return client


@pytest.fixture
@pytest.mark.remote_data
def history_client(maxlen: int = 20):
    """A client with a history plugin, requires a real api key in a .env."""
    history: HistoryPlugin = HistoryPlugin(maxlen=maxlen)
    client: Client = get_client(plugins=[history, CharitiesAuthPlugin()])
    assert hasattr(client.service, "GetCharitiesByName")
    return client


class TestZeepCharityClient:
    """Test generating a zeep `Client` object for Charity Commision API."""

    def test_specify_config(self, requests_mock):
        """Basic test of generating correct Client configuration."""
        TEST_WSDL_CODE: str = "http://a-test-api-code.uk/apiTest.asmx?wsdl"

        TEST_SOAP_ENV: str = """\
        <soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:v1="http://schemas.conversesolutions.com/xsd/dmticta/v1">
        <soapenv:Header/>
        <soapenv:Body>
        <v1:GetVehicleLimitedInfo>
        <v1:vehicleNo>?</v1:vehicleNo>
        <v1:phoneNo>?</v1:phoneNo>
        </v1:GetVehicleLimitedInfo>
        </soapenv:Body>
        </soapenv:Envelope>"""

        requests_mock.get(TEST_WSDL_CODE, text=TEST_SOAP_ENV)
        test_client: Client = get_client(TEST_WSDL_CODE)
        assert test_client.wsdl.location == TEST_WSDL_CODE
        assert test_client.settings.strict is False
        assert test_client.settings.xml_huge_tree is True

    def test_mock_get_charity_by_name(self, requests_mock, test_client):
        """Test mock query of GetCharitiesByName."""
        TEST_EMAIL: str = "an.email@test.org.uk"
        TEST_PHONE_NUMBER: str = "02075555555"

        TEST_SOAP_RESPONSE: str = f"""\
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <GetCharitiesByNameResponse xmlns="{TEST_TAG_NS}">
              <GetCharitiesByNameResult>
                <CharityList>
                  <RegisteredCharityNumber>
                    {TEST_PHOTOGRAPHERS_CHARITY_NUMBER}
                  </RegisteredCharityNumber>
                  <SubsidiaryNumber>
                    0
                  </SubsidiaryNumber>
                  <CharityName>
                    {TEST_PHOTOGRAPHERS_GALLERY_NAME}
                  </CharityName>
                  <MainCharityName>
                    {TEST_PHOTOGRAPHERS_GALLERY_NAME}
                  </MainCharityName>
                  <RegistrationStatus>
                    Registered
                  </RegistrationStatus>
                  <PublicEmailAddress>
                    {TEST_EMAIL}
                  </PublicEmailAddress>
                  <MainPhoneNumber>
                    {TEST_PHONE_NUMBER}
                  </MainPhoneNumber>
                </CharityList>
              </GetCharitiesByNameResult>
            </GetCharitiesByNameResponse>
          </soap:Body>
        </soap:Envelope>"""

        requests_mock.post(CHARITY_COMMISSION_API, text=TEST_SOAP_RESPONSE)
        response: Response = test_client.service.GetCharitiesByName(
            strSearch=TEST_PHOTOGRAPHERS_GALLERY_NAME
        )
        assert response[0]["CharityName"].strip() == (
            TEST_PHOTOGRAPHERS_GALLERY_NAME.rstrip()
        )
        assert response[0]["RegisteredCharityNumber"] == (
            TEST_PHOTOGRAPHERS_CHARITY_NUMBER
        )
        assert response[0]["PublicEmailAddress"].strip() == TEST_EMAIL
        assert response[0]["MainPhoneNumber"].strip() == TEST_PHONE_NUMBER

        history = test_client.plugins[0]
        assert history.last_received["envelope"][0][0].tag.endswith(
            "GetCharitiesByNameResponse"
        )
        assert len(history._buffer) == 1

    @pytest.mark.remote_data
    def test_get_charity_by_name(self, history_client):
        """Test raw_response and history of GetCharitiesByName query."""
        history = history_client.plugins[0]
        with history_client.settings(raw_response=True):
            raw_response = history_client.service.GetCharitiesByName(
                strSearch="TATE GALLERY FOUNDATION"
            )
            assert raw_response.status_code == 200
            with open("tests/charity_soap.wsdl", "rb") as test_output:
                test_tree = ElementTree.fromstring(test_output.read())
                resp_tree = ElementTree.fromstring(raw_response.content)
                assert test_tree.tag == resp_tree.tag
                for test in test_tree.iter():
                    for resp in resp_tree.iter():
                        if test.tag == resp.tag:
                            break
                    if resp.text:
                        assert resp.text.strip() == test.text.strip()
        assert history.last_sent["envelope"][0][0].tag.endswith(
            "GetCharitiesByName"
        )
        assert len(history._buffer) == 1
        response = history_client.service.GetCharitiesByName(
            strSearch="TATE GALLERY FOUNDATION"
        )
        assert response[0]["CharityName"].rstrip() == (
            "THE TATE GALLERY FOUNDATION"
        )
        assert history.last_received["envelope"][0][0].tag.endswith(
            "GetCharitiesByNameResponse"
        )
        assert len(history._buffer) == 2


class TestGetCharityNumber:
    """Test querying basic charity data."""

    @pytest.mark.remote_data
    def test_check_registered_charity_number(self):
        """Test on Photography's Gallery Limited."""
        charity = check_registered_charity_number(
            TEST_PHOTOGRAPHERS_GALLERY_NAME, TEST_PHOTOGRAPHERS_CHARITY_NUMBER
        )
        # charity = check_registered_charity_number(correct_charity_name,
        #                                           correct_charity_number,
        #                                           client=history_client)
        assert charity == TEST_PHOTOGRAPHERS_CHARITY_NUMBER


class TestGetCharityNetwork:
    """Test Contructing a Charity Network."""

    @pytest.mark.remote_data
    def test_tate_foundation(self, history_client):
        """Test basic query of Tate_Foundation board members."""
        charity_network = get_charity_network(
            TATE_FOUNDATION_ID, client=history_client
        )
        assert len(charity_network) == 15
        assert is_connected(charity_network)
        tate_foundation, board_members = bipartite.sets(charity_network)
        assert len(board_members) == 14
        assert (
            charity_network.nodes[TATE_FOUNDATION_ID]["name"]
            == TATE_FOUNDATION_NAME
        )
        assert charity_network.nodes[11965582]["name"] == (
            "Dr Maria " "Jane Balshaw"
        )

    @pytest.mark.remote_data
    def test_tate_foundation_str_id(self, history_client):
        """Test basic query of Tate_Foundation board members."""
        charity_network = get_charity_network("1085314", client=history_client)
        assert len(charity_network) == 15
        assert is_connected(charity_network)
        tate_foundation, board_members = bipartite.sets(charity_network)
        assert len(board_members) == 14
        assert type(list(tate_foundation)[0]) is int

    @pytest.mark.remote_data
    def test_1hop_tate(self, history_client):
        """Test 1 hop query of Tate_Foundation board members."""
        charity_network = get_charity_network(
            1085314, branches=1, client=history_client
        )
        assert len(charity_network) == 73
        assert is_connected(charity_network)
        tate_foundation, board_members = bipartite.sets(charity_network)
        assert len(board_members) == 64
