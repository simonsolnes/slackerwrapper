# slackerwrapper

slackerwrapper is a small library that wraps around [slacker](https://github.com/os/slacker). It makes for easy usage of the slack API.

## Usage

|Function			|Arguments							|Return												|
|-------------------|-----------------------------------|---------------------------------------------------|
|`test_api`			|None								|boolean											|
|`get_users`		|None								|list of users										|
|`get_channels`		|None								|list of channels									|
|`fetch_history`	|List of channels, message count	|None												|
|`get_history`		|Channel							|List of dictionaries with `'name'` and `'text'`	|

Notes:
* Both instant messages and channels are referenced to as channels

## Installing
* Put the [slacker folder](https://github.com/os/slacker/tree/master/slacker) in the same directory as your project.
* Put `slackerwrapper.py` in the same folder as your project.
* Create a document 'token' with your [slack token](https://api.slack.com/custom-integrations/legacy-tokens).
* `import slackerwrapper` and `slack = slackerwrapper.SlackerWrapper()`

