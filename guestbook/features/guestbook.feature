Feature: Guestbook BDD demo

    In order to use the guestbook,
    As a user
    I want to sign my message on guestbook

    Scenario: Sign without login
        Given user has been sign out
        When I go to "http://localhost:4567"
        Then I should see main page html
        When I sign "demo for mission control #8"
        Then I should see "demo for mission control #8" signed by "An anonymous person"

    # TODO:  Sign with login
