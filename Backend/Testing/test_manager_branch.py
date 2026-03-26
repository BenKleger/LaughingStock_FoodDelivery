from ..User.user_utils import isFloat
from User.manager_branch import get_ownedRestuarants
#note to self: to use patch, import the entire module where the func you're patching comes from otherwise error

"""Tests the standalone function isFloat w/equivalence testing and edge case tests"""
def test_posFloat():
    assert isFloat("50")

def test_edge():
    assert isFloat("0.0")

"""Tests """
def test_OwnedRestaurants(mocker):
    mock_users = mocker.patch("User.manager_branch.load_users")
    
    mock_users.return_value = [{"type": 3, "restaurantId": 101},
                               {"type": 2, "restaurantId": 103}
                               ]
    result = get_ownedRestuarants()
    assert result == [101]
    