---
code: RD19
title: "Unit, Integration, and E2E Testing API Routes"
date: 2026-02-18
due: 2026-02-20
type:  reading
threads: ["System / Backend"]
authors: ["Kris Jordan"]
---

This tutorial follows the previous tutorial on [Dependency Injection](1-dependency-injection.md) in FastAPI. Go ahead and reopen that tutorial to pick up from there.

This tutorial assumes you are versed in mocking and patching, which covered in the last unit of the course.

As a reminder, this tutorial implemented a simple RESTful game of Rock, Paper, Scissors. Our goal in this reading is to **unit test** the `/play` route handler in isolation _and_ **integration** test the routing layer (route registration and route handler) and service layers. Finally, we will look at **end-to-end** testing the backend _without_ patching over side-effects.

In good practice, go ahead and add your current changes to stage and form a commit as a checkpoint before moving on in this tutorial. Commit made? Let's get started!

## Unit Testing a Route Handler

!!! question "Practice Question"

    Consider the route definition below and identify:

    1. What is the function name we will unit test?
    2. What arguments will our unit test provide as _user input_?
    3. What arguments are dependency injected that our unit test will need to _mock_?
    4. What will the unit test prove?

    Click on the + icons below to reveal hints 

~~~python title="main.py" linenums="13"
@app.post("/play")
def play( # (1)!
    user_choice: Annotated[  # (2)!
        GamePlay,
        Body(description="User's choice of rock, paper, or scissors."),
    ],
    game_svc: GameServiceDI, # (3)!
) -> GameResult: # (4)!
    return game_svc.play(user_choice) #(5)!
~~~

1. `play` is the function name we are testing.
2. `user_choice` is a user input parameter we will need to provide.
3. `game_svc` is a dependency injected parameter we will mock.
4. `GameResult` is the type of object we expect returned back.
5. The logic of this route handler is intentionally simple and merely delegates to `game_svc`. Our test needs to prove that we successfully delegated to the injected `GameService` and that its result was faithfully returned.

### Setting up a Unit Test

Since this tutorial is for a very simple demonstration, all of our modules are defined at the top-level. In larger, real projects you would use directory structure to organize related modules together. Go ahead and create a test module in the project's top-level directory, next to the others, named `test_play_unit.py`.

~~~python title="test_play_unit.py" linenums="1" hl_lines="10 12 14"
from unittest.mock import MagicMock
from datetime import datetime

from main import play
from models import GamePlay, GameResult, Choice
from services import GameService

def test_play_returns_game_result():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...

~~~

Go ahead and try implementing this test and running it to confirm your test passes. You should be able to do so without assistance by reading and reasoning through the imports, but if you need some hints, see the box below.

!!! danger "Unit Testing Hints"

    1. In the _Arrange_ step, you'll need to setup a mock that specs `GameService` and a `GamePlay` instance. You will need to specify the `GameResult` return value of the method that you expect called on `GameService`.
    2. In the _Act_ step, you'll call the `play` function and record its result.
    3. In the _Assert_ step, you'll confirm the return value is equivalent to the `GameResult` instance you setup in the mock. You should also confirm that the service method was called once with the correct method(s).

## Integration Testing a Route

Notice in the _unit test_ you implemented above there is no notion of the `post` method nor the `/play` route handling that occurs in the FastAPI layer of the backend. Additionally, by design, we mocked a `GameService` double and avoided testing the integrated behavior of both the route handler and the `GameService`.

If you reread `GameService`'s implementation in `service.py`, you will remember that it uses randomization to decide the API's choice among rock, paper, and scissors using the `choice` function of Python's `random` library imported as `random_choice`. We will _patch_ over this behavior to control the side-effect, but otherwise test the integration of the FastAPI route registration, route handler function, and service class. 

(Note for the careful reader: there is _one other_ side-effect in `GameService`. Can you identify it? Since it is not integral to the business logic of the application, we will not worry about patching this side-effect in this tutorial. However, if you would like to practice patching, you can practice it here!)

Let's get a new test file setup:

~~~python title="test_play_integration.py" linenums="1" hl_lines="4 12 19-20 23-28"
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient  # (1)!

from main import app
from models import Choice


def test_play_integration():
    # Arrange
    client = TestClient(app)  # (2)!

    random_choice_mock = MagicMock()
    random_choice_mock.return_value = "paper"

    # Act
    with patch("_____________", random_choice_mock):  # (3)!
        response = client.post("/play", json={"user_choice": "rock"})  # (4)!

    # Assert
    random_choice_mock.assert_called_once()
    assert response.status_code == status.HTTP_200_OK  # (5)!
    response_body = response.json()
    assert response_body["user_choice"] == user_choice.user_choice
    assert response_body["api_choice"] == random_choice_mock.return_value
    assert response_body["user_wins"] == False
~~~

1. We are importing the `TestClient` utility class from FastAPI's library. This will help us test the actual routing layer of our API from an HTTP client's vantage point.
2. When we construct a `TestClient` we pass in a reference to our FastAPI app where our routes are registered.
3. What name are we patching over to isolate the randomization side-effect? This is your challenge in this particular code listing.
4. Notice here we are making a `post` request via the `client` to the `"/play"` route with a "JSON" dictionary object as our body.
5. Notice in our assertions, we are working with an actual HTTP response object. 

!!! question "Your task: fill in the `patch`ed target name string"

    Read through this integration test to understand its general flow. Click on the + icons for explanations of what is happening at new, important steps.

    Once you have a sense, replace the underscores in the patch string with the _name you are patching_ as it is defined _in the module you are applying the patch_ at.
    
    Hint: it is _not_ `random.choice`. Your test will pass once you target the correct name to patch.

Notice with this integration test we are testing all the way from FastAPI's route handling, to our route handler `play` function, to our `GameService`'s play method and helpers, only patching minimally over the random choice side-effect.

### Parametrizing the Integration Test

Can you identify one unsatisfying quality of this test? What if you wanted to test other choices and outcomes? There would be a lot of redundancy! 

Let's take a look at using `pytest`'s parametrization fixture to specify different combinationd of inputs to the same test:

~~~python title="test_play_integration.py" linenums="11" hl_lines="1 2 4 15 20 24 30-32"
@pytest.mark.parametrize(
    "user_choice_input,api_choice_input,user_wins_expected",
    [
        (Choice.rock, Choice.scissors, True),  # Rock beats scissors
        (Choice.rock, Choice.paper, False),  # Rock loses to paper
        (Choice.rock, Choice.rock, False),  # Rock ties rock (API wins)
        (Choice.paper, Choice.rock, True),  # Paper beats rock
        (Choice.paper, Choice.scissors, False),  # Paper loses to scissors
        (Choice.paper, Choice.paper, False),  # Paper ties paper (API wins)
        (Choice.scissors, Choice.paper, True),  # Scissors beats paper
        (Choice.scissors, Choice.rock, False),  # Scissors loses to rock
        (Choice.scissors, Choice.scissors, False),  # Scissors ties scissors (API wins)
    ],
)
def test_play_integration(user_choice_input, api_choice_input, user_wins_expected):
    # Arrange
    client = TestClient(app)

    random_choice_mock = MagicMock()
    random_choice_mock.return_value = api_choice_input

    # Act
    with patch("services.random_choice", random_choice_mock):
        response = client.post("/play", json={"user_choice": user_choice_input})

    # Assert
    random_choice_mock.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert response_body["user_choice"] == user_choice_input
    assert response_body["api_choice"] == api_choice_input
    assert response_body["user_wins"] == user_wins_expected
~~~

On line 11, you are using [`@pytest.mark.parametrize` decorator](https://docs.pytest.org/en/stable/how-to/parametrize.html) to configure the fixture parameters of the test function. On line 12, you will notice a funny string that feels a bit _off_ but represents the name matching convention used in `parametrize`. Compare line 12 with line 25, where the parameters (fixtures!) of the test function are declared and notice there is a 1-to-1 correspondence. What you are doing in the string on line 12 is declaring names for each value that will pass into the test via a parameter of the same name. 

Then, on lines 13-23 you see a list of 9 tuples declared. Each tuple contains three values, corresponding 1-to-1 with the parameter names defined on line 12. Each of these tuples represents _one test case_ worth of arguments that the test function will be called with. When you _run_ this singular test, nine individual tests will be run individually, one per each of your parametrize case tuples.

Inside of the test, rather than hard-coding a string value for the mocked return value of random choice, we substitute the parameter value in on line 30. The same strategy is used on lines 34 and 40-42.

The **big idea** of this kind of integration testing is we are now proving to ourselves that our backend layers are successfully integrated with one another and are implementing the logical outcomes we expect.

## End-to-End Testing a Route

For a final exercise, let's write a test that proves the _full system_ is working without any patching of side-effects, at all. This is an end-to-end backend test.

~~~python title="test_play_e2e.py" linenums="1" hl_lines="11 15 18"
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from models import Choice


@pytest.mark.parametrize(
    "user_choice_input",
    [(Choice.rock), (Choice.paper), (Choice.scissors)] * 100,  # (1)!
)
def test_play_e2e(user_choice_input):
    # Arrange
    client = TestClient(app) # (2)!

    # Act
    response = client.post("/play", json={"user_choice": user_choice_input}) # (3)!

    # Assert
    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert response_body["user_choice"] == user_choice_input
    assert response_body["api_choice"] in (Choice.rock, Choice.paper, Choice.scissors)

    actual_outcome: tuple[Choice, Choice, bool] = (
        response_body["user_choice"],
        response_body["api_choice"],
        response_body["user_wins"],
    )
    expected_outcomes: list[tuple[Choice, Choice, bool]] = [
        (Choice.rock, Choice.scissors, True),
        (Choice.rock, Choice.paper, False),
        (Choice.rock, Choice.rock, False),
        (Choice.paper, Choice.rock, True),
        (Choice.paper, Choice.scissors, False),
        (Choice.paper, Choice.paper, False),
        (Choice.scissors, Choice.paper, True),
        (Choice.scissors, Choice.rock, False),
        (Choice.scissors, Choice.scissors, False),
    ]
    assert actual_outcome in expected_outcomes
~~~

1. Python's `list` object has an operator overload for multiplication which produces a new list with the original list _repeated_ `N` times. Therefore, this parametrization will repeat the sequence of rock, paper, scissors 100 times over for 300 tests.
2. Notice in the arrange steps... we have no mocks or test doubles otherwise. This is a nice feature of end-to-end testing!
3. Notice in the act step... we are not patching anything! This is _also_ a nice feature of end-to-end testing. It is as real of a test of our backend system as we can write.

Expand on the notes of the highlighted lines on lines 11, 15, and 18 for some key insights on this end-to-end test. Notice how straightforward the arrange and act steps are without any mocking or patching. This is one of the benefits of end-to-end API testing: the initial setup is as about as minimal as the API's setup. (One noteworthy caveat: If we used persistence, such as files or a database, or network dependencies, we would either need to do more setup work to be sure the starting state was predictable or relax some of our specificity in assertions.)

When you run this end-to-end test you will notice that _300 tests_ are run!

!!! question "Why run more than three end-to-end tests in this scenario?"

    Why run 300? Since there is entropy in our system via the API's random `choice` of rock, paper, or scissors, there are 9 possible outcomes. This is not a resource intensive test to run. Therefore, repeating inputs over many tries gives us increasing confidence all cases are likely hit at least once. This is a common strategy and relates to the concept of a "fuzzing" test, but _fuzzing_ has broader implications around _invalid_ data we may explore later in the course. I chose the magic number 100 out of convenience sake.

    This choice is also impacted by what exactly your test is trying to prove. This end-to-end test is looking to show we are exhaustively covering the expected outcomes. That's reasonable when there are only nine outcomes. However, we _also_ proved this exhaustively in the _integration_ test. An engineer could argue for this end-to-end test, given the existence of other subsystem unit and integration tests, all we really need to convince ourselves of is the correct types of data and response code being returned. This is also a sound end-to-end testing strategy.

## What isn't tested in the `/play` route?

One aspect of the `/play` route none of our tests have addressed are exceptional cases where clients send invalid data to the API. For example, perhaps their choice is the string "bazooka". What happens then? In the version of FastAPI the tutorial uses, the validation error causes a 422 response to be produced automatically. However, this is not code we wrote yet clients of our service may depend on predictable exception behavior. If we wanted to codify this in a test, to help us catch a regression caused by a different decision in a future versions of FastAPI, we could write a test like so:

~~~python linenums="1"
def test_play_exception():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.post("/play", json={"user_choice": "bazooka"})

    # Assert
    assert response.status_code is status.HTTP_422_UNPROCESSABLE_ENTITY
~~~

In industrial strength software, it is generally a best practice to have regression tests for exceptional cases of all endpoints that clients of your API may depend upon. While this test adds 0 lines of new code coverage in our project code, it does add meaningful regression resilience for behaviors our clients rely upon.

Now that you have completed the tutorial, please submit the responses to questions on Gradescope.

## Answers

Answers to the open-ended questions posed in sections above.

### Unit Testing the `play` Route Handler

You can find one possible correct implementation of a unit test for the `play` route handler below:

~~~python title="test_play_unit.py" linenums="1"
def test_play_returns_game_result():
    # Arrange
    mock_svc: GameService = MagicMock(spec=GameService)
    user_choice = GamePlay(user_choice=Choice.rock)
    expected = GameResult(
        user_choice=Choice.rock,
        api_choice=Choice.paper,
        timestamp=datetime.now(),
        user_wins=False,
    )
    mock_svc.play.return_value = expected

    # Act
    actual: GameResult = play(user_choice, mock_svc)

    # Assert
    assert actual == expected
    mock_svc.play.assert_called_once_with(user_choice)
~~~

If you are thinking _wow_ 18 lines of code to unit test a function with one line of delegation, _that seems like a lot!_ You are not wrong. However, be sure you can reason through both the value of what this is verifying in the system _and_ the "contract" it is enforcing. 

The code could be refactored to use _fixtures_ as part of the _arrange_ steps to reduce some redundancy across multiple tests using the same service mock and choice, if needed. If there were other types of responses, such as _404 Not Found_, additional tests would need to be added that could reuse the fixtures and shorten the individual test implementations.

### Patching Target

The target you are attempting to patch is `services.random_choice`. Remember, you _patch the name where it is used._ If you look in the `services.py` imports section, you will see `from random import choice as random_choice`. Within the `services` module, this is _aliasing_ the `choice` function of the `random` package with the name `random_choice`. The `random_choice` function is called to produce the API's guess of rock, paper, or scissors, so this is the fully qualified name we are patching over to control the side-effect.