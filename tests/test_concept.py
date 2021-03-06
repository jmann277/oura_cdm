import pytest

from oura_cdm.concepts import (Concept, ObservationConcept, OuraConcept, PhysicalConcept,
                               ObservationTypeConcept, UnitConcept, get_ontology_dfs)
from oura_cdm.schemas import ConceptSchema, ConceptRelationshipSchema


@pytest.fixture(params=Concept.get_all_concepts())
def concept(request):
    return request.param


@pytest.fixture(params=[c for c in UnitConcept])
def unit_concept(request):
    return request.param


@pytest.fixture(params=[c for c in ObservationTypeConcept])
def observation_type_concept(request):
    return request.param


@pytest.fixture(params=[c for c in OuraConcept])
def oura_concept(request):
    return request.param


def test_rem_sleep_name(ontology):
    rem_name = ontology.get_concept_name(
        ObservationConcept.REM_SLEEP_DURATION)
    assert rem_name == 'REM sleep duration'


def test_units_are_units(ontology, unit_concept):
    domain_id = ontology.get_domain_id(unit_concept)
    assert domain_id == UnitConcept.get_domain_id()


def test_observation_concepts_domain(ontology, observation_concept):
    domain_id = ontology.get_domain_id(observation_concept)
    assert domain_id == ObservationConcept.get_domain_id()


def test_observation_type_domain(ontology, observation_type_concept):
    domain_id = ontology.get_domain_id(observation_type_concept)
    assert domain_id == ObservationTypeConcept.get_domain_id()


def test_concepts_in_concept_df(ontology, concept):
    assert ontology.is_valid(concept)


def test_get_concept_from_id(ontology, concept):
    assert concept == ontology.get_concept_from_id(concept.value)


def test_get_concept_id_from_name(ontology, concept):
    concept = ontology.get_concept_from_id(concept.value)
    expected = ontology.get_concept_name(concept)
    assert expected == ontology.get_concept_name_from_id(concept.value)


def test_concept_name_matches_enum_name(concept, ontology):
    concept_name = ontology.get_concept_name(concept)
    if ' ' in concept_name:
        actual_terms = {
            term.lower() for term in concept_name.split(' ')
        }
        expected_terms = {term.lower() for term in concept.name.split('_')}
        assert actual_terms.issubset(expected_terms)
    else:
        assert concept_name.lower() == concept.name.lower()


def test_every_oura_concept_maps_to_standard_concept(oura_concept, ontology):
    concept = ontology.maps_to(oura_concept)
    assert ontology.is_standard(concept)


def test_oura_date_keyword(ontology):
    concept = ontology.mapped_from(PhysicalConcept.DATE)
    keyword = ontology.get_concept_code(concept)
    assert 'date' in keyword.split('_')


def test_all_oura_concepts_mapping_to_observation_concepts_have_units(
        observation_concept, ontology):
    concept = ontology.mapped_from(observation_concept)
    assert isinstance(ontology.get_unit(concept), UnitConcept)


def test_ontology_dfs_fit_schemas():
    concept_df, concept_relationship_df = get_ontology_dfs()
    ConceptSchema.validate(concept_df)
    ConceptRelationshipSchema.validate(concept_relationship_df)

