Feature: Test holmium freshen integration
  Scenario: Test steps are loaded
    When I access the page TestPage at url {{url}}
    Then I should see the title test

  Scenario: Test all steps
    When I access the page TestPage at url {{url}}
    Then I should see the title test
    And element el should be visible
    And element el should have text e
    And the first item in els should be visible
    And the el of the first item in sections should have text e
    And the twenty first item in els should be visible
    And element els should have 100 items
    And the el for the first item in sections should have text e
    And the first item for the els item in section should have text e
    And the e item for the elmap item in section should have text e
    And el item in section should have text e
    When I wait for 10 seconds
    And I access the url {{login_url}}
    And I wait for 1 second
    And I click the el of the 1st item in sections
    And I click the first item in els
    And I click the e item in elmap
    And I click the element el
    And I type {{text}} in element el
    And I type {{text}} in e item in elmap
    And press enter in element el
    And I press Enter in e item in elmap
    And I go back
    And go forward
    And I perform do_stuff with arguments hello, world
    And I perform do_stuff with hello, world
    And I perform do_stuff_no_args
    And I perform do_stuff_var_args with arguments 1,2,3,4,5

  Scenario: Invalid page
    When I access the page FooPage at url {{url}}

  Scenario: Valid Page invalid element
    When I access the page TestPage at url {{url}}
    Then element not_existent should be visible

  Scenario: Valid Page invalid element in map
    When I access the page TestPage at url http://www.test.com
    Then the moo item in elmap should be visible

  Scenario: Valid Page invalid element in section
    When I access the page TestPage at url {{url}}
    Then the moo item in section should be visible


  Scenario: Valid Page invalid sub element
    When I access the page TestPage at url {{url}}
    Then the moo item in missing_section should be visible

  Scenario: Valid Page invalid action
    When I access the page TestPage at url {{url}}
    And I perform noop

  Scenario: Valid Page invalid action with args
    When I access the page TestPage at url {{url}}
    And I perform noop with arguments 1,2,3

  Scenario: Valid Page invalid action args
    When I access the page TestPage at url {{url}}
    And I perform do_stuff with arguments 1,2,3

