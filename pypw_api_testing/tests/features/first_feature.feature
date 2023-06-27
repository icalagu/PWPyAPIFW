Feature: Test the /pokemon/{pokemon_name} endpoint of the PokeAPI

  Scenario: Verify the response to a valid GET request
    Given I send a GET request to the berry endpoint
    And the response should have a status code of 200
    When I send a GET request to the pokemon/ditto endpoint
    Then the response should have a status code of 200

    Examples:
    | test |
    | test |

  Scenario: Verify the response to an invalid GET request
    Given I send a GET request to the berry endpoint
    And the response should have a status code of 200
    When I send a GET request to the pokemon/invalid_pokemon_name endpoint
    Then the response should have a status code of 404

    Examples:
    | test |
    | test |
