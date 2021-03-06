import pandas as pd
import pandera as pa
from pandera import Column
from pandera.typing import DateTime, Series, Index

from oura_cdm.concepts import ObservationConcept


class ObservationSchema(pa.SchemaModel):
    observation_id: Series[int] = pa.Field(unique=True)
    person_id: Series[int]
    observation_concept_id: Series[int]
    observation_date: Series[str]
    observation_datetime: Series[DateTime] = pa.Field(nullable=True)
    observation_type_concept_id: Series[int]
    value_as_number: Series[float] = pa.Field(nullable=True)
    value_as_string: Series[str] = pa.Field(nullable=True)
    value_as_concept_id: Series[int] = pa.Field(nullable=True)
    qualifier_concept_id: Series[int] = pa.Field(nullable=True)
    unit_concept_id: Series[int] = pa.Field(nullable=True)
    provider_id: Series[int] = pa.Field(nullable=True)
    visit_occurrence_id: Series[int] = pa.Field(nullable=True)
    visit_detail_id: Series[int] = pa.Field(nullable=True)
    observation_source_value: Series[str] = pa.Field(nullable=True)
    observation_source_concept_id: Series[int] = pa.Field(nullable=True)
    unit_source_value: Series[str] = pa.Field(nullable=True)
    qualifier_source_value: Series[str] = pa.Field(nullable=True)
    value_source_value: Series[str] = pa.Field(nullable=True)
    observation_event_id: Series[int] = pa.Field(nullable=True)
    obs_event_field_concept_id: Series[int] = pa.Field(nullable=True)


class ConceptSchema(pa.SchemaModel):
    concept_id: Index[int] = pa.Field(unique=True)
    concept_name: Series[str] = pa.Field(nullable=True)
    domain_id: Series[str]
    vocabulary_id: Series[str]
    standard_concept: Series[str] = pa.Field(nullable=True)
    concept_class_id:  Series[str]
    concept_code: Series[str]


class ConceptRelationshipSchema(pa.SchemaModel):
    concept_id_1: Index[int]
    concept_id_2: Series[int]
    relationship_id: Series[str]


def make_journey_schema(observation_df):
    observations = observation_df['observation_concept_id'].unique()
    columns = {
        observation: Column(
            type(ObservationConcept.get_reference_value(observation)))
        for observation in observations
    }
    schema = pa.DataFrameSchema(
        columns,
        index=pa.Index(pd.Timestamp)
    )
    return schema
