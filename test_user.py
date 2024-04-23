import pytest

@pytest.fixture
def user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager

@pytest.fixture
def user_ids(user_manager):
    user_manager.create_a_user("Teacher1", "pwd1", "teacher")
    user_manager.create_a_user("Student1", "pwd2", "student")
    user_manager.create_a_user("Student2", "pwd3", "student")
    user_manager.create_a_user("Student3", "pwd4", "student")
    ids = (1, 2, 3)
    return ids


def test_generate_id(user_manager):
    # arrange
    new_count = user_manager.counter

    # act
    result = user_manager.generate_id()

    # assert
    assert(result == (new_count + 1))


def test_create_a_user(user_manager):
    # arrange
    new_index = len(user_manager.user_list)
    new_count = user_manager.counter

    # act 
    user_manager.create_a_user("Teacher1", "pwd1", "teacher")

    # assert
    assert((len(user_manager.user_list)) == (new_index + 1))
    assert(user_manager.user_list[new_index].name == "Teacher1")
    assert(user_manager.user_list[new_index].password == "pwd1")
    assert(user_manager.user_list[new_index].type == "teacher")
    assert(user_manager.counter == (new_count + 1))


def test_find_users_empty(user_manager):

    # act
    ids = (1, 2, 3)
    result = user_manager.find_users(ids)

    # assert
    assert(result == "Users not found")


def test_find_users(user_manager, user_ids):

    # act
    result = user_manager.find_users(user_ids)

    # assert
    assert(result[0].name == "Teacher1")
    assert(result[1].name == "Student1")
    assert(result[2].name == "Student2")
    assert(result[0].type == "teacher")
    assert(result[1].type == "student")


def test_find_users_behavior(mocker, user_manager, user_ids):
    # arrange
    find_users = mocker.patch('user.UserManager.find_users')
   
    # act
    result = user_manager.find_users(user_ids)

    # assert
    find_users.assert_called_with(user_ids)



def test_create_a_user_behavior(mocker, user_manager):
    # arrange
    new_index = len(user_manager.user_list)
    new_count = user_manager.counter
    create_a_user = mocker.patch('user.UserManager.create_a_user')

    # act 
    user_manager.create_a_user("Teacher1", "pwd1", "teacher")

    # assert
    create_a_user.assert_called_with("Teacher1", "pwd1", "teacher")