from typing import List, Any

from plugitin import PackageNameFinder
from plugitin.metas.module import PythonModuleMeta
from tests.fsutils import use_path
from tests import config as conf


def test_name_finder_match():
    with use_path(conf.PROJECT_1_PATH):
        finder = PackageNameFinder("impl")
        results: List[PythonModuleMeta] = []
        for res in finder.find():
            results.append(res)
        results_direct = finder.find_all()
        for res_list in [results, results_direct]:
            assert len(res_list) == 1
            assert res_list[0].import_path == "impl"
            assert res_list[0].plugin_name == "impl"


def test_name_finder_no_match():
    with use_path(conf.PROJECT_1_PATH):
        finder = PackageNameFinder("sfgsrthysfhgfgh")
        results: List[PythonModuleMeta] = []
        for res in finder.find():
            results.append(res)
        results_direct = finder.find_all()
        for res_list in [results, results_direct]:
            assert len(res_list) == 0
