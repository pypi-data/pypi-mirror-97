Installing the Curia Python SDK
===============================
The Curia Python SDK is built to PyPi and can be installed with pip as follows:

.. code:: bash

    pip install curia

You can install from source by cloning this repository and running a pip install command in the root directory of the repository:

.. code:: bash

    git clone https://github.com/FoundryAI/curia-python-sdk.git
    cd curia-python-sdk
    pip install .

Curia API Token
==========================
To use the Curia Python SDK you will need a Curia API Token. To access your API Token visit https://app.curia.ai/settings.

Using the Curia Python SDK
==========================
.. code:: python

    from curia.session import Session
    from curia.risk import RiskModel
    from curia.synthetic_data import generate_data

    # Create synthetic data (demo/testing purposes only)
    (X_train, X_test, _, _, y_train, y_test, _, _, _, _) = generate_data(binary_outcome=True)

    # Create a session
    curia_session = Session(api_token="YOUR_API_TOKEN")

    # Instantiate a model
    model = RiskModel(
        session=curia_session,
        name="your-model-name",
        project_id="YOUR_PROJECT_ID"
    )

    # Train a model on the Curia Platform
    model.train(features=X_train, label=y_train)

    # Get predictions from your model on the Curia Platform
    predictions = model.predict(features=X_test)
