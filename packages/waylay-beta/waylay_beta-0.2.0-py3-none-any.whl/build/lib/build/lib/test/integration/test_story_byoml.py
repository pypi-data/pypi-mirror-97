"""Integration tests that validates the BYOML story.

See https://github.com/waylayio/waylay-py/issues/3
"""
import time
import pandas as pd
from sklearn.covariance import EllipticEnvelope

from waylay import (
    WaylayClient,
    RestResponseError
)


def test_byoml_create_model(waylay_test_client: WaylayClient):
    """Create, upload, and test a model."""
    train_query = dict(
        resource='151CF',
        metric='temperature',
        freq='PT1H',
        aggregation='mean',
        until='2020-01-01T00:00:00Z',
        data=[dict(metric='temperature'), dict(metric='avgSnr')]
    )

    df_train = waylay_test_client.analytics.query.execute(body=train_query)

    # train model
    cov_model = EllipticEnvelope(random_state=0, contamination=0.05).fit(df_train)

    # test model locally
    validation_query = dict(train_query)
    validation_query['until'] = '2020-04-01'
    df_validate = waylay_test_client.analytics.query.execute(body=validation_query)
    df_prediction = pd.DataFrame(
        cov_model.predict(df_validate),
        index=df_validate.index
    )
    assert len(df_prediction.index) == len(df_validate.index)

    # upload model (delete any existing first)
    model_name = "integration-test-01"
    try:
        waylay_test_client.byoml.model.remove(model_name)
    except RestResponseError as exc:
        pass
    waylay_test_client.byoml.model.upload(
        model_name, cov_model, framework="sklearn",
        description=f"integration test {__name__}.test_byoml_create_model"
    )

    # validate that model is present
    model_repr = waylay_test_client.byoml.model.get(model_name)
    assert 'name' in model_repr
    assert f'integration test {__name__}' in model_repr['description']

    # test model on byoml, wait until ready
    predictions = None
    max_retry = 50
    retry_count = 1
    while retry_count <= 50:
        try:
            start_time = time.time()
            try:
                predictions = waylay_test_client.byoml.model.predict(model_name, df_validate)
            finally:
                elapsed_time_ms = 1000.0 * (time.time() - start_time)
                print(f'prediction request took {elapsed_time_ms} ms')
            retry_count = max_retry + 1
        except RestResponseError as exc:
            assert exc.response.status_code == 409
            print(f'waiting for the byoml model to be compiled [{retry_count}]')
            time.sleep(2)
            retry_count += 1
    assert predictions is not None
    assert len(predictions) == len(df_validate.index)

    # replace model
    waylay_test_client.byoml.model.replace(
        model_name, cov_model, framework="sklearn",
        description=f"updated integration test {__name__}.test_byoml_create_model"
    )
    model_repr = waylay_test_client.byoml.model.get(model_name)
    assert 'updated' in model_repr['description']

    # remove model
    waylay_test_client.byoml.model.remove(model_name)
