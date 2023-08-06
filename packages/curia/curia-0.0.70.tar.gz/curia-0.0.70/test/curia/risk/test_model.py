from curia.model import _Model
from curia.risk import RiskModel


def test_risk_model_inherits_model(curia_session):
    model = RiskModel(session=curia_session, name='test-model')

    assert isinstance(model, _Model)


def test_risk_model_optional_params(curia_session):
    model = RiskModel(
        session=curia_session,
        name='test-model',
        description='test model description',
        project_id='project',
        environment_id='environment'
    )
    assert model.name == 'test-model'
    assert model.description == 'test model description'
    assert model.project_id == 'project'
    assert model.environment_id == 'environment'

# @freeze_time("Jan 1st, 2020")
# def test_risk_model_dataset_upload(curia_session, mocker, monkeypatch):
#     (X_train, _, _, _, y_train, _, _, _, _, _) = generate_data(
#         binary_outcome=True)
#
#     df = X_train.copy()
#     df['label'] = y_train
#
#     model = RiskModel(
#         session=curia_session,
#         name='test-model',
#         description='test-model-description',
#         project_id='project-id'
#     )
#     model.set_job_type('train')
#
#     def mock_model():
#         return model.session.api_client.Model(
#             id='model-id',
#             name=model.name,
#             description=model.description,
#             type=model.model_type,
#             project_id=model.project_id,
#             feature_store=model.feature_store
#         )
#
#     def mock_dataset():
#         return model.session.api_client.Dataset(
#             id='dataset-id',
#             name=f'{model.model_id}-{model._job_type}-{datetime.now()}',
#             description='BYOD train dataset uploaded via curia-python-sdk',
#             file_size=df.memory_usage(index=False).sum(),
#             type='train',
#             dataset_results={},
#         )
#
#     def mock_dataset_upload():
#         return True
#
#     def mock_model_dataset():
#         return model.session.api_client.ModelDataset(
#             id='model-dataset-id',
#             dataset_id=mock_dataset().id,
#             model_id=mock_model().id,
#         )
#
#     monkeypatch.setattr(model.session.api_instance, 'create_one_base_model_controller_model',
#                         mock_model)
#     monkeypatch.setattr(model.session.api_instance, 'create_one_base_dataset_controller_dataset',
#                         mock_dataset)
#     monkeypatch.setattr(model.session.api_instance, 'dataset_controller_upload',
#                         mock_dataset_upload)
#     monkeypatch.setattr(model.session.api_instance,
#                         'create_one_base_model_dataset_controller_model_dataset',
#                         mock_model_dataset)
#
#     create_model_spy = mocker.spy(model.session.api_instance,
#                                   'create_one_base_model_controller_model')
#     create_dataset_spy = mocker.spy(model.session.api_instance,
#                                     'create_one_base_dataset_controller_dataset')
#     dataset_upload_spy = mocker.spy(model.session.api_instance, 'dataset_controller_upload')
#     create_model_dataset_spy = mocker.spy(model.session.api_instance,
#                                           'create_one_base_model_dataset_controller_model_dataset')
#
#     model.model_dataset_upload(data=df)
#
#     mock_model_request = mock_model()
#     mock_model_request.id = None
#     create_model_spy.assert_called_once_with(mock_model_request)
#
#     mock_dataset_request = mock_dataset()
#     mock_dataset_request.id = None
#     create_dataset_spy.assert_called_once_with(mock_dataset_request)
#
#     dataset_upload_spy.assert_called_once()
#
#     mock_model_dataset_request = mock_model_dataset()
#     mock_model_dataset_request.id = None
#     create_model_dataset_spy.assert_called_once_with(mock_model_dataset_request)

# @freeze_time("Jan 1st, 2020")
# def test_risk_model_start(curia_session, mocker, monkeypatch):
#     model = RiskModel(
#         session=curia_session,
#         name='test-model',
#         description='test-model-description',
#         project_id='project-id'
#     )
#     model.set_job_type('train')
#
#     monkeypatch.setattr(model.session.api_instance, 'create_one_base_model_controller_model',
#                         mock_model)
