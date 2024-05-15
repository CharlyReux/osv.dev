"""impact_git_test.py: Tests for the impact module using git repositories."""

from .test_tools.test_repository import TestRepository, EventType
from osv.vulnerability_pb2 import Event

import unittest
from . import impact


class GitImpactTest(unittest.TestCase):
  """Tests for the impact module using git repositories."""

  @classmethod
  def setUpClass(cls):
    cls.__repo_analyzer = impact.RepoAnalyzer(detect_cherrypicks=True)

  ######## 1st : tests with "introduced" and "fixed"
  def test_introduced_fixed_linear(self):
    """Simple range, only two commits are vulnerable. 
    Model : A->B->C->D """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.FIXED
    }
    expected_vulnerable = {"B", "C"}
    self.template_four_linear(events, expected_vulnerable,
                              "test_introduced_fixed_linear")

  ######## 2nd : tests with "introduced" and "limit"
  def test_introduced_limit_linear(self):
    """Ensures the basic behavior of limit 
    (the limit commit is considered unaffected).
    Model : A->B->C->D """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.LIMIT
    }
    expected_vulnerable = {"B", "C"}
    self.template_four_linear(events, expected_vulnerable,
                              "test_introduced_limit_linear")

  ######## 3nd : tests with "introduced" and "last-affected"
  def test_introduced_last_affected_linear(self):
    """Ensures the basic behavior of last_affected 
    commits (the last_affected commit is considered affected).
    Model : A->B->C->D """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.LAST_AFFECTED
    }
    expected_vulnerable = {"B", "C", "D"}
    self.template_four_linear(events, expected_vulnerable,
                              "test_introduced_last_affected_linear")

  ######## 4nd : tests with "introduced", "limit", and "fixed"
  def test_introduced_limit_fixed_linear_lf(self):
    """Ensures the behaviors of limit and fixed commits are not conflicting.
    Model : A->B->C->D """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.LIMIT,
        "D": EventType.FIXED
    }
    expected_vulnerable = {"B"}
    self.template_four_linear(events, expected_vulnerable,
                              "test_introduced_limit_fixed_linear_lf")

  ######## 5nd : tests with "introduced", "limit",
  # and "fixed" in a different order
  def test_introduced_limit_fixed_linear_fl(self):
    """Ensures the behaviors of limit and fixed commits are not conflicting.
    Model : A->B->C->D """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.FIXED,
        "D": EventType.LIMIT
    }
    expected_vulnerable = {"B"}
    self.template_four_linear(events, expected_vulnerable,
                              "test_introduced_limit_fixed_linear_fl")

######## 6nd : branch tests with "introduced", "limit", and "fixed"

  def test_introduced_fixed_branch_propagation(self):
    """Simple range, checking the propagation of the 
    vulnerability in created branch. 
    Model :   A->B->C->D 
                    |->E"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.FIXED,
        "E": EventType.NONE
    }
    expected_vulnerable = {"B", "C", "E"}
    self.template_five_last_branch(events, expected_vulnerable,
                                   "test_introduced_fixed_branch_propagation")

######## 7nd : branch tests with "introduced" and "limit"

  def test_introduced_limit_branch(self):
    """ensures the basic behavior of limit commits in branches. 
    Model :   A->B->C->D 
                    |->E"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.LIMIT,
        "E": EventType.NONE
    }
    expected_vulnerable = {"B", "C"}
    self.template_five_last_branch(events, expected_vulnerable,
                                   "test_introduced_limit_branch")

######## 8nd : branch tests with "introduced" and "last-affected"

  def test_introduced_last_affected_branch_propagation(self):
    """ensures the basic behavior of last_affected commits when 
    the repository has a branch. 
    Model :   A->B->C->D 
                    |->E"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.LAST_AFFECTED,
        "E": EventType.NONE
    }
    expected_vulnerable = {"B", "C", "D", "E"}
    self.template_five_last_branch(
        events, expected_vulnerable,
        "test_introduced_last_affected_branch_propagation")

######## 9nd : merge tests with "introduced" and "fixed"

  def test_introduced_fixed_merge(self):
    """ Simple range, checking the non propagation of the 
    vulnerability in the created branch . 
    Model :      A ->B-> D->E 
                  |->C-/^"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.NONE,
        "E": EventType.FIXED
    }
    expected_vulnerable = {"B", "D"}
    self.template_five_second_branch_merge(events, expected_vulnerable,
                                           "test_introduced_fixed_merge")

######## 10nd : merge tests with "introduced" and "limit"

  def test_introduced_limit_merge(self):
    """ Simple range, checking the non propagation of the 
    vulnerability in created branch with a limit commit. 
    Model :      A ->B-> D->E 
                  |->C-/^"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.NONE,
        "E": EventType.LIMIT
    }
    expected_vulnerable = {"B", "D"}
    self.template_five_second_branch_merge(events, expected_vulnerable,
                                           "test_introduced_limit_merge")

######## 11nd : merge tests with "introduced" and "last-affected"

  def test_introduced_last_affected_merge(self):
    """ Simple range, checking the non propagation of the vulnerability 
    in the created branch with a last-affected commit. 
    Model :      A ->B-> D->E 
                  |->C-/^"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.NONE,
        "E": EventType.LIMIT
    }
    expected_vulnerable = {"B", "D"}
    self.template_five_second_branch_merge(
        events, expected_vulnerable, "test_introduced_last_affected_merge")

######## 12nd : merge tests with "introduced", and two "fixed",
# one in the created branch and one in the main branch

  def test_introduced_fixed_merge_fix_propagation(self):
    """ Srange with two fixed, checking the propagation of the fix 
    from the created branch to the main branch. 
    Model :      A ->B-> D->E 
                  |->C-/^"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.FIXED,
        "D": EventType.NONE,
        "E": EventType.FIXED
    }
    expected_vulnerable = {"B"}
    self.template_five_second_branch_merge(
        events, expected_vulnerable,
        "test_introduced_fixed_merge_fix_propagation")

######## 13nd : linear tests with two "introduced" and two "fixed" intercalated

  def test_introduced_fixed_two_linear(self):
    """ Srange with two fixed, checking the non propagation of the 
    fix from the created branch to the main branch. 
    Model :      A->B->C->D->E """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.FIXED,
        "D": EventType.INTRODUCED,
        "E": EventType.FIXED
    }
    expected_vulnerable = {"B", "D"}
    self.template_five_linear(events, expected_vulnerable,
                              "test_introduced_fixed_two_linear")

######## 14nd : merge tests with one "introduced" in main,
# one "fixed" in the created branch, and one "fixed" in the main branch

  def test_introduced_fixed_merge_propagation(self):
    """ range with two fixed, checking the non propagation of the fix from the 
    created branch to the main branch. 
    Model :          A->B->C->E-F 
                     |-> D -/^ """
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.FIXED,
        "D": EventType.INTRODUCED,
        "E": EventType.NONE,
        "F": EventType.FIXED
    }
    expected_vulnerable = {"B", "D", "E"}
    self.template_six_second_branch_merge(
        events, expected_vulnerable, "test_introduced_fixed_merge_propagation")


######## 15nd : testing the behavior of limit with a branch

  def test_introduced_limit_branch_limit(self):
    """ range with. 
    Model :      A ->B-> C->E 
                     |-> D"""
    events = {
        "B": EventType.INTRODUCED,
        "C": EventType.NONE,
        "D": EventType.LIMIT,
        "E": EventType.FIXED
    }
    expected_vulnerable = {"B"}
    self.template_five_third_branch(events, expected_vulnerable,
                                    "test_introduced_limit_branch_limit")

  ###### Utility Template methods
  def template_four_linear(self, events, expected, name):
    """Linear template with 4 commits  
    A->B->C->D """
    repo = TestRepository(name, debug=False)
    repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])
    repo.add_commit(
        message="D", parents=[repo.get_head_hex()], event=events["D"])
    repo.create_remote_branch()

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )

  def template_five_linear(self, events, expected, name):
    """Linear template with 5 commits  
    A->B->C->D """
    repo = TestRepository(name, debug=False)
    repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])
    repo.add_commit(
        message="D", parents=[repo.get_head_hex()], event=events["D"])
    repo.add_commit(
        message="E", parents=[repo.get_head_hex()], event=events["E"])

    repo.create_remote_branch()

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )

  def template_five_last_branch(self, events, expected, name):
    """Template with 5 commits, the last one in a different branch
       
    A->B->C->D 
          |->E """
    repo = TestRepository(name, debug=False)
    repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    c = repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])
    repo.create_branch_if_needed_and_checkout("feature")
    repo.add_commit(message="E", parents=[c], event=events["E"])
    repo.checkout("main")
    repo.add_commit(
        message="D", parents=[repo.get_head_hex()], event=events["D"])
    repo.create_remote_branch()

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )

  def template_five_second_branch_merge(self, events, expected, name):
    """Template with 5 commits, the second one in a different 
    branch and merged right after 
      
    A->B->D->E 
    |->C-/^ """
    repo = TestRepository(name, debug=False)
    repo.create_branch_if_needed_and_checkout("feature")
    c = repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])
    repo.checkout("main")
    b = repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    repo.add_commit(message="D", parents=[b, c], event=events["D"])
    repo.add_commit(
        message="E", parents=[repo.get_head_hex()], event=events["E"])
    repo.create_remote_branch()

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )

  def template_six_second_branch_merge(self, events, expected, name):
    """Template with 6 commits, the second one in a different branch and 
    merged after two commits in the main branch

    A->B->C->E->F  
    |->  D -/^ """
    repo = TestRepository(name, debug=False)
    repo.create_branch_if_needed_and_checkout("feature")
    d = repo.add_commit(
        message="D", parents=[repo.get_head_hex()], event=events["D"])
    repo.checkout("main")
    repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    c = repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])

    repo.add_commit(message="E", parents=[c, d], event=events["E"])
    repo.add_commit(
        message="F", parents=[repo.get_head_hex()], event=events["E"])

    repo.create_remote_branch()

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )

  def template_five_third_branch(self, events, expected, name):
    """Template with 5 commits, the third one in a different branch, not merged
      
    A->B->C->E   
       |->D"""
    repo = TestRepository(name, debug=False)
    repo.add_commit(
        message="B", parents=[repo.get_head_hex()], event=events["B"])
    repo.create_branch_if_needed_and_checkout("feature")
    repo.add_commit(
        message="D", parents=[repo.get_head_hex()], event=events["D"])
    repo.checkout("main")
    repo.add_commit(
        message="C", parents=[repo.get_head_hex()], event=events["C"])
    repo.add_commit(
        message="E", parents=[repo.get_head_hex()], event=events["E"])

    repo.create_remote_branch()
    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()
    expected_commits = repo.get_commit_ids(expected)

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)
    result_commit_message = repo.get_message_by_commits_id(result.commits)
    repo.clean()
    self.assertEqual(
        result.commits,
        expected_commits,
        "Expected: %s, got: %s" % (expected, result_commit_message),
    )
'''
  
  ######## 2nd : tests with "introduced" and "limit"

  def test_introduced_limit_two_linear(self):
    """Ensures that multiple introduced commit in
    the same branch are correctly handled, wrt limit."""
    repo = TestRepository("test_introduced_limit_two_linear", debug=False)

    first = repo.add_empty_commit(
        vulnerability=TestRepository.VulnerabilityType.INTRODUCED)
    second = repo.add_empty_commit(
        parents=[first], vulnerability=TestRepository.VulnerabilityType.LIMIT)
    third = repo.add_empty_commit(
        parents=[second],
        vulnerability=TestRepository.VulnerabilityType.INTRODUCED)
    repo.add_empty_commit(
        parents=[third], vulnerability=TestRepository.VulnerabilityType.LIMIT)
    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)

    expected = set([first.hex, third.hex])
    repo.remove()
    self.assertEqual(
        result.commits,
        expected,
        "Expected: %s, got: %s" % (expected, result.commits),
    )

  ######## 3nd : tests with "introduced" and "last-affected"

 

    expected = set([first.hex, second.hex, third.hex])
    repo.remove()
    self.assertEqual(
        result.commits,
        expected,
        "Expected: %s, got: %s" % (expected, result.commits),
    )

  def test_introduced_last_affected_two_linear(self):
    """Ensures that multiple introduced commit in 
    the same branch are correctly handled, wrt last_affected."""
    repo = TestRepository(
        "test_introduced_last_affected_two_linear", debug=False)

    first = repo.add_empty_commit(
        vulnerability=TestRepository.VulnerabilityType.INTRODUCED)
    second = repo.add_empty_commit(
        parents=[first],
        vulnerability=TestRepository.VulnerabilityType.LAST_AFFECTED,
    )
    third = repo.add_empty_commit(
        parents=[second],
        vulnerability=TestRepository.VulnerabilityType.INTRODUCED)
    fourth = repo.add_empty_commit(
        parents=[third],
        vulnerability=TestRepository.VulnerabilityType.LAST_AFFECTED,
    )

    (all_introduced, all_fixed, all_last_affected,
     all_limit) = repo.get_ranges()

    result = self.__repo_analyzer.get_affected(repo.repo, all_introduced,
                                               all_fixed, all_limit,
                                               all_last_affected)

    expected = set([first.hex, second.hex, third.hex, fourth.hex])
    repo.remove()
    self.assertEqual(
        result.commits,
        expected,
        "Expected: %s, got: %s" % (expected, result.commits),
    )


    '''
