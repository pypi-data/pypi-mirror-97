import os
import pytest
import shutil
import tempfile


def _copy_data(target_path='.'):
    dirname = os.path.dirname(__file__)
    shutil.copytree(os.path.join(dirname, '../../data/classification_data/multilabel'),
                    os.path.join(target_path, 'multilabel'))


@pytest.fixture(scope="session")
def get_nlp_data():
    oldpath = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    _copy_data()
    yield
    os.chdir(oldpath)
    shutil.rmtree(newpath)
