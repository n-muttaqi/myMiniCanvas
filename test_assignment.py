import pytest


@pytest.fixture
def assignment():
    from assignment import Assignment

    my_assignment = Assignment(1, 1, 1)
    return my_assignment


@pytest.fixture
def submission():
    from assignment import Submission

    my_submission = Submission(1, "HW1")
    return my_submission


def test_submit(assignment, submission):
    # arrange
    new_index = len(assignment.submission_list)

    # act
    assignment.submit(submission)

    # assert
    assert len(assignment.submission_list) == (new_index + 1)
    assert assignment.submission_list[0].submission == "HW1"
    assert assignment.submission_list[0].student_id == 1


def test_submit_behavior(mocker, assignment, submission):
    # arrange
    new_index = len(assignment.submission_list)
    mocked_submit = mocker.patch("assignment.Assignment.submit")

    # act
    assignment.submit(submission)

    # assert
    mocked_submit.assert_called_with(submission)