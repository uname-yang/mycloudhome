"""utils tests."""
# import mock
import pytest

import mycloudhome.utils as utils


def test_is_wd_path():
    assert utils.is_wd_path('/user/d') == False
    assert utils.is_wd_path('wd://user/d') == True
    assert utils.is_wd_path('root') == True
    assert utils.is_wd_path('wd://') == True