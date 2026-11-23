from helpers import GhostTextWorldExpressEnv

test_seeds = list(range(0, 20))
test_environments = [GhostTextWorldExpressEnv(envStepLimit=100)]
test_games = {
    "coin": [
        "numLocations=5,includeDoors=1,numDistractorItems=0",
        "numLocations=6,includeDoors=1,numDistractorItems=0",
        "numLocations=7,includeDoors=1,numDistractorItems=0",
        "numLocations=10,includeDoors=1,numDistractorItems=0",
        "numLocations=11,includeDoors=1,numDistractorItems=0",
    ],
    "mapreader": [
        "numLocations=5,maxDistanceApart=3,includeDoors=0,maxDistractorItemsPerLocation=0",
        "numLocations=8,maxDistanceApart=4,includeDoors=0,maxDistractorItemsPerLocation=0",
        "numLocations=11,maxDistanceApart=5,includeDoors=0,maxDistractorItemsPerLocation=0",
        "numLocations=15,maxDistanceApart=8,includeDoors=0,maxDistractorItemsPerLocation=0",
        "numLocations=20,maxDistanceApart=8,includeDoors=0,maxDistractorItemsPerLocation=0",
    ],
}


def test_agent(env, guess_x, guess_y):
    obs, _, _, _ = env.step("report " + str(guess_x) + " " + str(guess_y))
    print("Guess: (", guess_x, ", ", guess_y, ")")
    return obs == "True"


def run_all(
    run_agent: callable,
    environments=test_environments,
    games=test_games,
    seeds=test_seeds,
    alpha_param=0.90,
) -> None:
    # Results will contain a key (env type, game type, game params, seed) and values will be plans and total_reward͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁s
    num_tests_ran = 0
    num_game_params = sum([len(params) for params in games.values()])
    num_tests_ran = len(environments) * num_game_params * len(seeds)
    results = {}
    # Iterate through all environments give͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁n
    for env in environments:
        # set global environmen͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁t
        ENV = env
        # Iterate through all game types, the keys of the games dic͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁t
        for game_type in games:
            # Set the global game typ͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁e
            GAME_TYPE = game_type
            # Iterate through all game parameters for the given game type in game dic͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁t
            for params in games[game_type]:
                # set the global game param͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁s
                GAME_PARAMS = params
                # load the environmen͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁t
                ENV.load(gameName=GAME_TYPE, gameParams=GAME_PARAMS)

                # Iterate through all seed͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁s
                for seed in seeds:
                    try:
                        # set the see͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁d
                        print(GAME_TYPE, GAME_PARAMS, seed)
                        obs, infos = ENV.reset(seed)
                        x, y = run_agent(ENV, obs, infos, alpha=alpha_param)

                        # Store the score in the result͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁s
                        results[(type(env), game_type, params, seed)] = test_agent(
                            env, x, y
                        )
                    except Exception as e:
                        if str(e).startswith(
                            "An error occurred while calling o2.generateNewGameJSON."
                        ):
                            print(f"Skipping {type(ENV)} {seed} {params} {game_type}")
                            num_tests_ran -= 1
                        else:
                            print("Student code raises an error")
                            print("or you are not exporting your cells correctly")
                            print(e)
    return results, num_tests_ran


def test_all_configs(run_agent: callable, alpha_param=0.90) -> None:
    final_results, num_tests_ran = run_all(
        run_agent, test_environments, test_games, test_seeds, alpha_param
    )
    results = list(final_results.values())
    accuracy = results.count(True) / num_tests_ran

    # print(results͏󠄀͏󠄍͏︃͏︆͏︀͏︀͏︋͏󠄍͏󠄇͏󠄀͏󠄎͏󠄒͏︎͏󠄇͏︈͏︃͏︁)
    print("Number of tests ran: ", num_tests_ran)
    print("Number of tests passed: ", results.count(True))
    print("Agent accuracy: ", accuracy)
    assert accuracy >= alpha_param
    print("Passed! Accuracy greater than ", alpha_param)
