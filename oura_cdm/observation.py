from dataclasses import dataclass
from functools import partial
from typing import Dict, List

import pandas as pd

from oura_cdm.concepts import (ObservationConcept, ObservationTypeConcept, Ontology,
                               OuraConcept, PhysicalConcept)
from oura_cdm.logs import log_info, log_warning

log_info_o = partial(log_info, **{'name': __name__})
log_warning_o = partial(log_warning, **{'name': __name__})


def get_mock_row() -> pd.DataFrame:
    row = pd.DataFrame({
        "observation_id": [123124],
        "person_id": [1234151],
        "observation_concept_id": [ObservationConcept.REM_SLEEP_DURATION.value],
        "observation_date": ['20220206'],
        "observation_datetime": [pd.Timestamp('2017-01-01T12')],
        "observation_type_concept_id": [1234152],
        "value_as_number": [None],
        "value_as_string": [None],
        "value_as_concept_id": [None],
        "qualifier_concept_id": [None],
        "unit_concept_id": [None],
        "provider_id": [None],
        "visit_occurrence_id": [None],
        "visit_detail_id": [None],
        "observation_source_value": [None],
        "observation_source_concept_id": [None],
        "unit_source_value": [None],
        "qualifier_source_value": [None],
        "value_source_value": [None],
        "observation_event_id": [None],
        "obs_event_field_concept_id": [None]
    }).astype({
        "value_as_number": 'float',
        "value_as_concept_id": 'Int64',
        "qualifier_concept_id": 'Int64',
        "unit_concept_id": 'Int64',
        "provider_id": 'Int64',
        "visit_occurrence_id": 'Int64',
        "visit_detail_id": 'Int64',
        "observation_source_value": 'str',
        "observation_source_concept_id": 'Int64',
        "unit_source_value": 'str',
        "qualifier_source_value": 'str',
        "value_source_value": 'str',
        "observation_event_id": 'Int64',
        "obs_event_field_concept_id": 'Int64'
    })
    return row


def get_observation_table(raw_oura_data: List[Dict]) -> pd.DataFrame:
    log_info_o('Creating observation table')
    transformer = ObservationTransformer(raw_oura_data)
    transformed_data = transformer.get_transformed_data()
    log_info_o('Observation table successfully created')
    return transformed_data


@dataclass
class ObservationTransformer():
    # TODO: make the parameters the source data, ontology, and the vocabulary
    # id of the source vocabulary.
    raw_oura_data: List[Dict]
    ontology: Ontology = Ontology()

    def get_transformed_data(self,) -> pd.DataFrame:
        mock_row = get_mock_row()
        rows = []
        for i, day in enumerate(self.raw_oura_data):
            for j, concept in enumerate(ObservationConcept):
                new_row = mock_row.copy()
                new_row.loc[:, 'observation_id'] = self.get_observation_id(
                    concept, i)
                new_row.loc[:, 'observation_date'] = self.get_observation_date(
                    i)
                new_row.loc[:, 'observation_concept_id'] = concept.value
                new_row.loc[:, 'value_as_number'] = self.get_observation_value(
                    i, concept)
                new_row.loc[:, 'value_source_value'] = self.get_value_source_value(
                    i, concept)
                new_row.loc[:, 'observation_type_concept_id'] = self.get_observation_type_id(
                    i, concept)
                new_row.loc[:, 'unit_concept_id'] = self.get_unit_concept_id(
                    i, concept)
                rows.append(new_row)
        if len(rows) == 0:
            return mock_row.iloc[:0, :]
        ans = pd.concat(rows)
        return ans

    def get_observation_date(self, index: int) -> str:
        oura_date_concept = self.ontology.mapped_from(PhysicalConcept.DATE)
        keyword = self.ontology.get_concept_code(oura_date_concept)
        return self.raw_oura_data[index][keyword]

    def get_observation_id(
        self, sleep_concept: ObservationConcept, index: int
    ) -> int:
        return sleep_concept.value * (1 + index)

    def get_observation_value(self, index: int, concept: ObservationConcept) -> float:
        return float(self.get_value_source_value(index, concept))

    def get_value_source_value(self, index: int, concept: ObservationConcept) -> str:
        oura_concept = self.ontology.mapped_from(concept)
        return str(self.raw_oura_data[index][
            self.ontology.get_concept_code(oura_concept)
        ])

    def get_observation_type_id(self, index: int, concept: ObservationConcept) -> int:
        # Use oura concept to get the observation type
        return ObservationTypeConcept.LAB.value

    def get_unit_concept_id(self, index: int, concept: ObservationConcept) -> int:
        oura_concept = self.ontology.mapped_from(concept)
        return self.ontology.get_unit(oura_concept).value
