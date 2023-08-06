import copy
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import (
    NoResultFound,
)
from parameterized import parameterized

from test.backendtestcase import TestCase
from test.utils import second_equals_first
from src.cs_models.resources.PTAB2Proceeding import PTAB2Proceeding
from src.cs_models.resources.Subsidiary import Subsidiary
from src.cs_models.resources.CompanySEC import CompanySEC
from src.cs_models.resources.CompanyOUS import CompanyOUS


class PTAB2ProceedingResourceTestCase(TestCase):
    def setUp(self):
        super(PTAB2ProceedingResourceTestCase, self).setUp()
        self.inst_subsidiary = Subsidiary()
        self.inst_sec_company = CompanySEC()
        self.inst_ous_company = CompanyOUS()
        self.inst = PTAB2Proceeding()

        self.company_sec1 = self.inst_sec_company.create({
            'cik_str': '200406',
            'ticker': 'JNJ',
            "title": "JOHNSON & JOHNSON",
        })

        self.company_sec2 = self.inst_sec_company.create({
            "cik_str": "816284",
            "ticker": "CELG",
            "title": "CELGENE CORP /DE/"
        })

        self.company_ous1 = self.inst_ous_company.create({
            'name': 'Aurobindo Pharma',
            'ticker': 'AUROPHARMA',
            'exchange': 'NSE',
        })

        self.subsidiary1 = self.inst_subsidiary.create({
            'name': 'Janssen Scientific Affairs, LLC',
            'company_sec_id': self.company_sec1['id'],
            'company_ous_id': None,
        })

        self.subsidiary2 = self.inst_subsidiary.create({
            'name': 'Celgene International II SARL',
            'company_sec_id': self.company_sec2['id'],
            'company_ous_id': None,
        })

        self.ptab2_proceeding1 = self.inst.create({
            'accorded_filing_date': '05-06-2013',
            'decision_date': '10-07-2014',
            'institution_decision_date': '10-08-2013',
            'petitioner_application_number_text': '-',
            'petitioner_counsel_name': 'Steven Baughman',
            'petitioner_grant_date': '-',
            'petitioner_group_art_unit_number': '-',
            'petitioner_inventor_name': '-',
            'petitioner_party_name': 'Apple Inc.',
            'petitioner_patent_number': '-',
            'petitioner_patent_owner_name': '-',
            'petitioner_technology_center_number': '-',
            'proceeding_filing_date': '05-06-2013',
            'proceeding_last_modified_date': '-',
            'proceeding_number': 'IPR-100',
            'proceeding_status_category': 'FWD Entered',
            'proceeding_type_category': 'AIA Trial',
            'respondent_application_number_text': '08471964',
            'respondent_counsel_name': 'David Marsh',
            'respondent_grant_date': '10-12-1999',
            'respondent_group_art_unit_number': '-',
            'respondent_inventor_name': 'ARTHUR HAIR',
            'respondent_party_name': 'SightSound Technologies LLC',
            'respondent_patent_number': '5966440',
            'respondent_patent_owner_name': 'SightSound Technologies LLC',
            'respondent_technology_center_number': '2100',
            'subproceeding_type_category': 'CBM',
            'respondent_subsidiary_id': None,
            'petitioner_subsidiary_id': None,
        })

        self.ptab2_proceeding2 = self.inst.create({
            'accorded_filing_date': '05-06-2013',
            'decision_date': '10-07-2014',
            'institution_decision_date': '10-08-2013',
            'petitioner_application_number_text': '-',
            'petitioner_counsel_name': 'Steven Baughman',
            'petitioner_grant_date': '-',
            'petitioner_group_art_unit_number': '-',
            'petitioner_inventor_name': '-',
            'petitioner_party_name': 'Apple Inc.',
            'petitioner_patent_number': '-',
            'petitioner_patent_owner_name': '-',
            'petitioner_technology_center_number': '-',
            'proceeding_filing_date': '05-06-2013',
            'proceeding_last_modified_date': '-',
            'proceeding_number': 'IPR-200',
            'proceeding_status_category': 'FWD Entered',
            'proceeding_type_category': 'AIA Trial',
            'respondent_application_number_text': '08471964',
            'respondent_counsel_name': 'David Marsh',
            'respondent_grant_date': '10-12-1999',
            'respondent_group_art_unit_number': '-',
            'respondent_inventor_name': 'ARTHUR HAIR',
            'respondent_party_name': 'SightSound Technologies LLC',
            'respondent_patent_number': '5966440',
            'respondent_patent_owner_name': 'SightSound Technologies LLC',
            'respondent_technology_center_number': '2100',
            'subproceeding_type_category': 'CBM',
            'proceeding_status': None,
            'respondent_subsidiary_id': self.subsidiary1['id'],
            'petitioner_subsidiary_id': self.subsidiary2['id'],
        })

        self.valid_data = {
            'accorded_filing_date': '05-06-2013',
            'decision_date': '10-07-2014',
            'institution_decision_date': '10-08-2013',
            'petitioner_application_number_text': '-',
            'petitioner_counsel_name': 'Steven Baughman',
            'petitioner_grant_date': '-',
            'petitioner_group_art_unit_number': '-',
            'petitioner_inventor_name': '-',
            'petitioner_party_name': 'Apple Inc.',
            'petitioner_patent_number': '-',
            'petitioner_patent_owner_name': '-',
            'petitioner_technology_center_number': '-',
            'proceeding_filing_date': '05-06-2013',
            'proceeding_last_modified_date': '-',
            'proceeding_number': 'IPR-300',
            'proceeding_status_category': 'FWD Entered',
            'proceeding_type_category': 'AIA Trial',
            'respondent_application_number_text': '08471964',
            'respondent_counsel_name': 'David Marsh',
            'respondent_grant_date': '10-12-1999',
            'respondent_group_art_unit_number': '-',
            'respondent_inventor_name': 'ARTHUR HAIR',
            'respondent_party_name': 'SightSound Technologies LLC',
            'respondent_patent_number': '5966440',
            'respondent_patent_owner_name': 'SightSound Technologies LLC',
            'respondent_technology_center_number': '2100',
            'subproceeding_type_category': 'CBM',
            'proceeding_status': None,
            'respondent_subsidiary_id': self.subsidiary1['id'],
            'petitioner_subsidiary_id': self.subsidiary2['id'],
        }

    def test_create_violates_unique_constraint(self):
        data = copy.copy(self.valid_data)
        data['proceeding_number'] = self.ptab2_proceeding1['proceeding_number']
        self.assertRaises(
            IntegrityError,
            self.inst.create,
            data,
        )

    def test_create(self):
        resp = self.inst.create(self.valid_data)
        expected_data = {
            **self.valid_data,
            **{
                'accorded_filing_date': '2013-05-06T00:00:00+00:00',
                'decision_date': '2014-10-07T00:00:00+00:00',
                'institution_decision_date': '2013-10-08T00:00:00+00:00',
                'petitioner_grant_date': None,
                'proceeding_filing_date': '2013-05-06T00:00:00+00:00',
                'respondent_grant_date': '1999-10-12T00:00:00+00:00',
            }
        }
        second_equals_first(expected_data, resp)

    def test_read(self):
        resp = self.inst.read({})
        self.assertEqual(len(resp), 2)

    @parameterized.expand([
        ('id', 'ptab2_proceeding1', 'id', 1),
        ('proceeding_number', 'ptab2_proceeding1', 'proceeding_number', 1),
    ])
    def test_read_w_params(
        self,
        field_name,
        attr,
        attr_field,
        expected_length,
    ):
        resp = self.inst.read({})
        self.assertEqual(len(resp), 2)

        resp = self.inst.read({
            field_name: getattr(self, attr)[attr_field],
        })
        self.assertEqual(expected_length, len(resp))

    @parameterized.expand([
        ('id', 999, NoResultFound),
    ])
    def test_one_raises_exception(self, field_name, field_value, exception):
        self.assertRaises(
            exception,
            self.inst.one,
            {
                field_name: field_value,
            },
        )

    @parameterized.expand([
        ('id',),
        ('proceeding_number',),
    ])
    def test_one(self, field_name):
        resp = self.inst.one({
            field_name: self.ptab2_proceeding1[field_name],
        })
        second_equals_first(
            self.ptab2_proceeding1,
            resp,
        )

    def test_delete_not_found(self):
        invalid_id = 99999
        self.assertRaises(
            NoResultFound,
            self.inst.delete,
            invalid_id,
        )

    def test_delete(self):
        response = self.inst.one({'id': self.ptab2_proceeding1['id']})
        self.inst.delete(id=response['id'])
        self.assertRaises(
            NoResultFound,
            self.inst.one,
            {'id': self.ptab2_proceeding1['id']},
        )

    def test_upsert_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.upsert,
            {
                'respondent_patent_number': (
                    self.valid_data['respondent_patent_number']),
            }
        )

    def test_upsert_creates_new_entry(self):
        data = copy.copy(self.valid_data)
        self.assertEqual(2, len(self.inst.read({})))
        self.inst.upsert(data)
        self.assertEqual(3, len(self.inst.read({})))

    def test_upsert_updates_existing_row(self):
        data = {
            **self.valid_data,
            **{'proceeding_number': (
                self.ptab2_proceeding1['proceeding_number'])},
        }
        resp = self.inst.upsert(data)
        expected_data = {
            **data,
            **{
                'accorded_filing_date': '2013-05-06T00:00:00+00:00',
                'decision_date': '2014-10-07T00:00:00+00:00',
                'institution_decision_date': '2013-10-08T00:00:00+00:00',
                'petitioner_grant_date': None,
                'proceeding_filing_date': '2013-05-06T00:00:00+00:00',
                'respondent_grant_date': '1999-10-12T00:00:00+00:00',
            }
        }
        second_equals_first(
            expected_data,
            resp,
        )
        self.assertEqual(2, len(self.inst.read({})))

    @parameterized.expand([
        ('respondent_subsidiary_id',),
        ('petitioner_subsidiary_id',),
    ])
    def test_upsert_with_empty_respondent_subsidiary_id(self, field):
        data = {
            **self.valid_data,
            **{field: None},
        }
        self.assertEqual(2, len(self.inst.read({})))
        resp = self.inst.upsert(data)
        self.assertEqual(3, len(self.inst.read({})))
        self.assertIsNone(resp[field])

    @parameterized.expand([
        ('respondent_subsidiary_id',),
        ('petitioner_subsidiary_id',),
    ])
    def test_upsert_violates_fk_for_invalid_company_id(self, field):
        invalid_subsidiary_id = 912839123
        data = {
            **self.valid_data,
            **{field: invalid_subsidiary_id},
        }
        self.assertRaises(
            IntegrityError,
            self.inst.upsert,
            data,
        )

    def test_upsert_with_valid_subsidiary_id(self):
        data = {
            **self.valid_data,
            **{
                'respondent_subsidiary_id': self.subsidiary1['id'],
                'petitioner_subsidiary_id': self.subsidiary2['id'],
            },
        }
        resp = self.inst.upsert(data)
        self.assertEqual(self.subsidiary1['id'], resp[
            'respondent_subsidiary_id'])

    def test_update_fails_when_missing_proceeding_number(self):
        self.assertRaises(
            ValidationError,
            self.inst.update,
            {
                'respondent_patent_number': (
                    self.valid_data['respondent_patent_number']),
            }
        )

    def test_partial_update(self):
        self.assertEqual(
            None,
            self.ptab2_proceeding1['proceeding_status'],
        )
        new_proceeding_status = 'INSTITUTED'
        data = {
            'proceeding_number': self.ptab2_proceeding1['proceeding_number'],
            'proceeding_status': new_proceeding_status,
        }
        response = self.inst.update(data)

        expected_result = {
            **self.ptab2_proceeding1,
            **data,
        }
        second_equals_first(
            expected_result,
            response,
            fields_to_ignore=['updated_at'],
        )
