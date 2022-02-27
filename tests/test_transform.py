import pytest

from oura_cdm.concepts import SleepConcept, OuraKeywords, ObservationTypeConcept
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import SleepObservationSchema


@pytest.fixture
def observation_df(oura_data):
    observation_df = get_observation_table(oura_data)
    return observation_df


@pytest.fixture
def raw_observation(oura_data):
    return oura_data[0]


@pytest.fixture
def raw_observation_date(raw_observation):
    return raw_observation[OuraKeywords.DATE]


@pytest.fixture(params=list(SleepConcept))
def concept(request,):
    return request.param


@pytest.fixture
def observation_dict(concept, observation_df, raw_observation_date):
    expecteds = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == concept)
    ]
    assert len(expecteds) == 1
    return dict(expecteds.iloc[0, :])


def test_observation_table_schema(observation_df):
    SleepObservationSchema.validate(observation_df)


def test_n_observations(oura_data, observation_df):
    n_sleep_concepts = len(SleepConcept)
    assert len(observation_df) == n_sleep_concepts * len(oura_data)


def test_observation_date(raw_observation_date, observation_df):
    observation_dates = list(observation_df.observation_date)
    assert raw_observation_date in observation_dates


def test_observation_values(
    raw_observation_date, raw_observation, observation_df,
    concept
):
    actual = raw_observation[OuraKeywords.get_keyword_from_concept(concept)]
    expecteds = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == concept)
    ].value_as_number
    assert len(expecteds) == 1
    expected = expecteds.iloc[0]
    assert float(actual) == expected


def test_source_value(
    raw_observation_date, raw_observation, observation_df,
    concept
):
    actual = raw_observation[OuraKeywords.get_keyword_from_concept(concept)]
    expecteds = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == concept)
    ].value_source_value
    assert len(expecteds) == 1
    expected = expecteds.iloc[0]
    try:
        expected = int(expected)
    except ValueError:
        pass
    assert actual == expected


def test_units(
    observation_dict, concept
):
    assert observation_dict['unit_concept_id'] == SleepConcept.get_unit_source_id(concept)


def test_observation_type_is_valid(
    raw_observation_date, raw_observation, observation_df,
    concept
):
    actuals = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == concept)
    ].observation_type_concept_id
    assert len(actuals) == 1
    actual = actuals.iloc[0]
    assert actual in {c.value for c in ObservationTypeConcept}


@pytest.mark.skip
def test_observation_datetime(
        observation_dict
):
    assert False
