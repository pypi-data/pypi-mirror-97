"""resource action method decorators specific for the 'analytics' service."""

from functools import wraps
from enum import Enum
from typing import (
    Union, List
)
import pandas as pd
from simple_rest_client.exceptions import ErrorWithResponse

from ._util import (
    parse_df,
    RENDER_MODE_COMPACT_WS
)
from ._exceptions import (
    AnalyticsActionError,
    AnalyticsActionParseError
)

DEFAULT_RENDER_MODE = RENDER_MODE_COMPACT_WS


def analytics_exception_decorator(action_method):
    """Decorate an analytics action with an error response parser."""
    @wraps(action_method)
    def wrapped(*args, **kwargs):
        try:
            return action_method(*args, **kwargs)
        except ErrorWithResponse as exc:
            raise AnalyticsActionError.from_cause(exc) from exc
    return wrapped


class MultiFrameHandling(Enum):
    """Strategies to handle list of data frames as returned by the the analytics api."""

    FIRST = 'return the first dataframe'
    LIST = 'return a list of dataframes'
    SINGLE = 'assert that the response contains a single dataframe'
    SINGLE_OR_LIST = 'return a dataframe or a list of dataframes'
    JOIN = 'join all dataframes, using table attributes'


def analytics_return_dataframe_decorator(
    data_key: str = 'data',
    default_render_mode: str = DEFAULT_RENDER_MODE,
    default_frames_handling: MultiFrameHandling = MultiFrameHandling.SINGLE
):
    """Decorate an analytics action with dataframe representation handling."""

    def decorator(action_method):
        @wraps(action_method)
        def wrapped(*args, **kwargs):
            raw = kwargs.pop('raw', False)
            constructor = kwargs.pop('response_constructor', 'tsa_dataframe') or (lambda x: x)
            frames_handling = kwargs.pop('multi_frame', default_frames_handling)
            # 'render.mode' call argument has precendence on 'render.mode' url param
            render_mode = kwargs.pop('render_mode', None)
            if not render_mode and 'params' in kwargs:
                render_mode = kwargs['params'].get('render.mode', None)
            if 'params' not in kwargs:
                kwargs['params'] = {}
            render_mode = render_mode or default_render_mode
            # set render mode
            kwargs['params']['render.mode'] = render_mode
            try:
                resp = action_method(*args, **kwargs)
            except ErrorWithResponse as exc:
                raise AnalyticsActionError.from_cause(exc) from exc
            if raw:
                return resp
            try:
                if constructor == 'tsa_dataframe':
                    return parse_data_frame_response(
                        resp.body.get(data_key), render_mode, frames_handling
                    )
                return constructor(resp.body.get(data_key))
            except (ValueError, AttributeError, TypeError) as exc:
                raise AnalyticsActionParseError(exc.args[0], resp) from exc
        return wrapped
    return decorator


def parse_data_frame_response(
    data_response, render_mode, frames_handling
) -> Union[None, pd.DataFrame, List[pd.DataFrame]]:
    """Parse a json reponse to a dataframe.

    Handles a list of dataframes as specified in `frames_handling`.
    """
    if isinstance(data_response, list):
        if len(data_response) == 0:
            return None

        has_multiple = len(data_response) > 1

        if frames_handling == MultiFrameHandling.SINGLE and has_multiple:
            raise ValueError(
                'multiple dataframes returned while one expected'
            )

        df_list = [parse_df(resp_df, render_mode=render_mode) for resp_df in data_response]

        if frames_handling == MultiFrameHandling.LIST:
            return df_list

        if not has_multiple:
            return df_list[0]

        if frames_handling == MultiFrameHandling.FIRST:
            return df_list[0]

        if frames_handling == MultiFrameHandling.JOIN:
            # TODO
            # * unroll table attributes into column attributes
            # * join tables
            # * move 'single level' attributes back to table attributes (except for levels)
            #   that were in the columns originally
            # what follows is a hack that for our common 'role' case works
            return pd.concat({
                df.tsa.table_attributes['role']: df for df in df_list
            }, axis=1, names=['role'])

        if frames_handling == MultiFrameHandling.SINGLE_OR_LIST:
            return df_list
        raise ValueError(
            f'could not handle multipe dataframes with {frames_handling}'
        )
    else:
        return parse_df(data_response)
