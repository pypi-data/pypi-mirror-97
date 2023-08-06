from curia.model import _Model


def test_model_class_is_abstract(curia_session):
    try:
        _Model(
            session=curia_session,
            name='test-model'
        )
    except TypeError as err:
        assert err


def test_model_methods_defined():
    assert _Model.model_dataset_upload
    assert _Model.start
    assert _Model.set_name
    assert _Model.set_job_type
    assert _Model.set_description
    assert _Model.set_model_id
    assert _Model.set_project_id
    assert _Model.set_environment_id
    assert _Model.set_model_dataset_id
