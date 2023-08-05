"""
A basic Phantom App connector implementation.

Customise the Connector class using `ActionHandler` methods, or define your
own implementation.
"""
from phantom_dev.action_handler import ActionHandler, contains, smart_connector


@contains('text')
class Text(str):
    """A string-based type that contains ['text']"""


@contains('fake count')
class Count(int):
    """A numeric-based type that contains ['fake count']"""


@contains('fake units')
class Amount(float):
    """A numeric-based type that contains ['fake units']"""


@smart_connector
class Connector:
    """
    Use a class decorated with `smart_connector` as a simple way to implement
    a Phantom App connector.

    Decorate member functions with `@ActionHandler` to register them as action
    handler methods.
    Handler methods should accept whichever parameters the action requires to
    run as keyword arguments.
    The connector's `context` member can be used to access the hidden context
    parameter passed to `phantom.act` during action execution.

    Parameter annotations can be used to infer the parameter type if they are
    subclasses of Python primitives (`int`, `float`, `str`, or `bool`).
    Handler docstrings can similarly be used to infer the description of each
    action.
    Sphinx-stype docstring parameter descriptions can also be used to infer
    the description of each parameter if not specified in the metadata.
    Parameter annotation default values are reflected in the metadata, and are
    also used to infer whether a parameter is mandatory.

    To add `contains` information, decorate a class with the `contains`
    decorator with the `contains` values as positional arguments.
    Use this class for parameter annotations (it should inherit from a Python
    primitve type).

    `contains` information can also be added to output by using the
    `ActionHandler.data_contains` decorator instead of `ActionHandler`.
    Similarly, `<handler>.summary_contains` can be used instead of
    `<handler>.summary`.
    These decorators take a mapping of relative datapaths to paramater types;
    use `contains`-mapped classes in the same manner as described above for
    action parameters.
    For action result data, the datapath keys should be relative to
    `'action_result.data.*'`;
    for summary data, the datapath keys should be relative to
    `'action_result.summary'`

    Handler methods should return iterables of result data dictionaries.
    They can return iterables as functions, or be implemented as data
    dictionary generators.
    See the `test_connectivity` and `dummy_generator` methods below for
    examples of each approach.

    Once an action handler method has been defined and decorated with
    `@ActionHandler`, the handler method has a member called `summary` that
    can be used to register another method as the action summary method.
    The action summary method should take an iterable of the results from the
    handler method and return an action result summary dict.
    See the `summarise` method for an example using the `dummy_action` handler
    method to register it as the summary method for `dummy_action`.

    As a result of using `smart_connector`, this class inherits from
    `phantom.base_connector.BaseConnector`, as well as implementing the testing
    interface when this module is run as the main script.

    See the official Phantom documentation for information about
    `phantom.base_connector.BaseConnector` and its members.
    """

    @ActionHandler
    def test_connectivity(self):
        """
        Reports simple messages to Phantom using standard Python logging.
        """
        self.logger.info(
            'Hello! By default, log messages of level INFO and above will be'
            ' displayed using save_progress regardless of Phantom debug'
            ' logging configuration.'
        )
        self.logger.info(
            'All log messages of level ERROR and above will be logged to '
            '`/var/log/spawn.log`.'
        )
        self.logger.info(
            'If debug logging is enabled, all log messages of level DEBUG and '
            'above (including these INFO calls) will also be logged.'
        )
        self.logger.debug(
            'This DEBUG message will not be displayed using save_progress, but'
            ' if system debug logging is enabled, this message will be'
            ' logged to `/var/log/spawn.log`'
        )
        self.logger.error(
            'This ERROR message will be logged regardless of Phantom logging'
            ' configuration, and also displayed using save_progress.'
        )
        return []

    @ActionHandler.data_contains(
        {'name': Text, 'value': Text, 'type': Text, 'context': Text})
    def dummy_action(
            self,
            required_number: Count,
            required_str: Text,
            required_bool: bool,
            optional_number: Amount = 42.69,
            optional_str: Text = 'spam',
            optional_bool: bool = False,
    ):
        """
        Takes a variety of parameters and reports them back to Phantom.

        The parameter type annotations are used to infer the `data_type` for
        each parameter in the generated metadata unless new values are manually
        specified.

        :param required_number: A mandatory number
        :param required_str: A mandatory string
        :param required_bool: A mandatory bool
        :param optional_number: An optional number
        :param optional_str: An optional string
        :param optional_bool: An optional bool
        """
        names = [
            'required_number',
            'required_str',
            'required_bool',
            'optional_number',
            'optional_str',
            'optional_bool',
        ]
        local_vars = locals()
        for x in names:
            value = local_vars[x]
            yield {
                'name': x,
                'value': value,
                'type': type(value).__name__,
                'context': str(self.context),
            }

    @dummy_action.summary_contains(
        {
            'message': Text,
            'results.name': Text,
            'results.value': Text,
            'results.type': Text,
            'results.context': Text,
        },
    )
    def summarise(self, results):
        """
        Create a summary object from the result of dummy_action.

        :param iterable results: The output of a call to dummy_action
        :return: A dictionary summarising the result of dummy_action
        :rtype: dict
        """
        return {'message': 'Dummy action ran', 'results': results}
