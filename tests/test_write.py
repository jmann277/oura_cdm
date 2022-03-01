import os

import pytest

from oura_cdm.artifacts import Artifact
from oura_cdm.write import clean_up_run, write_artifacts


@pytest.fixture
def write_test_file(pipeline_artifacts,):
    test_target_folder_name = 'write_test_folder'
    old_files = os.listdir()
    write_artifacts(pipeline_artifacts, test_target_folder_name)
    yield test_target_folder_name
    clean_up_run(test_target_folder_name)
    assert old_files == os.listdir()


def test_write(write_test_file):
    assert os.listdir(write_test_file) == [
        Artifact.get_filename(a) for a in Artifact
    ]
