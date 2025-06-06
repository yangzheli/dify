import json
from unittest import mock
from uuid import uuid4

from constants import HIDDEN_VALUE
from core.variables import FloatVariable, IntegerVariable, SecretVariable, StringVariable
from models.workflow import Workflow, WorkflowNodeExecutionModel


def test_environment_variables():
    # tenant_id context variable removed - using current_user.current_tenant_id directly

    # Create a Workflow instance
    workflow = Workflow(
        tenant_id="tenant_id",
        app_id="app_id",
        type="workflow",
        version="draft",
        graph="{}",
        features="{}",
        created_by="account_id",
        environment_variables=[],
        conversation_variables=[],
    )

    # Create some EnvironmentVariable instances
    variable1 = StringVariable.model_validate(
        {"name": "var1", "value": "value1", "id": str(uuid4()), "selector": ["env", "var1"]}
    )
    variable2 = IntegerVariable.model_validate(
        {"name": "var2", "value": 123, "id": str(uuid4()), "selector": ["env", "var2"]}
    )
    variable3 = SecretVariable.model_validate(
        {"name": "var3", "value": "secret", "id": str(uuid4()), "selector": ["env", "var3"]}
    )
    variable4 = FloatVariable.model_validate(
        {"name": "var4", "value": 3.14, "id": str(uuid4()), "selector": ["env", "var4"]}
    )

    # Mock current_user as an EndUser
    mock_user = mock.Mock()
    mock_user.tenant_id = "tenant_id"

    with (
        mock.patch("core.helper.encrypter.encrypt_token", return_value="encrypted_token"),
        mock.patch("core.helper.encrypter.decrypt_token", return_value="secret"),
        mock.patch("models.workflow.current_user", mock_user),
    ):
        # Set the environment_variables property of the Workflow instance
        variables = [variable1, variable2, variable3, variable4]
        workflow.environment_variables = variables

        # Get the environment_variables property and assert its value
        assert workflow.environment_variables == variables


def test_update_environment_variables():
    # tenant_id context variable removed - using current_user.current_tenant_id directly

    # Create a Workflow instance
    workflow = Workflow(
        tenant_id="tenant_id",
        app_id="app_id",
        type="workflow",
        version="draft",
        graph="{}",
        features="{}",
        created_by="account_id",
        environment_variables=[],
        conversation_variables=[],
    )

    # Create some EnvironmentVariable instances
    variable1 = StringVariable.model_validate(
        {"name": "var1", "value": "value1", "id": str(uuid4()), "selector": ["env", "var1"]}
    )
    variable2 = IntegerVariable.model_validate(
        {"name": "var2", "value": 123, "id": str(uuid4()), "selector": ["env", "var2"]}
    )
    variable3 = SecretVariable.model_validate(
        {"name": "var3", "value": "secret", "id": str(uuid4()), "selector": ["env", "var3"]}
    )
    variable4 = FloatVariable.model_validate(
        {"name": "var4", "value": 3.14, "id": str(uuid4()), "selector": ["env", "var4"]}
    )

    # Mock current_user as an EndUser
    mock_user = mock.Mock()
    mock_user.tenant_id = "tenant_id"

    with (
        mock.patch("core.helper.encrypter.encrypt_token", return_value="encrypted_token"),
        mock.patch("core.helper.encrypter.decrypt_token", return_value="secret"),
        mock.patch("models.workflow.current_user", mock_user),
    ):
        variables = [variable1, variable2, variable3, variable4]

        # Set the environment_variables property of the Workflow instance
        workflow.environment_variables = variables
        assert workflow.environment_variables == [variable1, variable2, variable3, variable4]

        # Update the name of variable3 and keep the value as it is
        variables[2] = variable3.model_copy(
            update={
                "name": "new name",
                "value": HIDDEN_VALUE,
            }
        )

        workflow.environment_variables = variables
        assert workflow.environment_variables[2].name == "new name"
        assert workflow.environment_variables[2].value == variable3.value


def test_to_dict():
    # tenant_id context variable removed - using current_user.current_tenant_id directly

    # Create a Workflow instance
    workflow = Workflow(
        tenant_id="tenant_id",
        app_id="app_id",
        type="workflow",
        version="draft",
        graph="{}",
        features="{}",
        created_by="account_id",
        environment_variables=[],
        conversation_variables=[],
    )

    # Create some EnvironmentVariable instances

    # Mock current_user as an EndUser
    mock_user = mock.Mock()
    mock_user.tenant_id = "tenant_id"

    with (
        mock.patch("core.helper.encrypter.encrypt_token", return_value="encrypted_token"),
        mock.patch("core.helper.encrypter.decrypt_token", return_value="secret"),
        mock.patch("models.workflow.current_user", mock_user),
    ):
        # Set the environment_variables property of the Workflow instance
        workflow.environment_variables = [
            SecretVariable.model_validate({"name": "secret", "value": "secret", "id": str(uuid4())}),
            StringVariable.model_validate({"name": "text", "value": "text", "id": str(uuid4())}),
        ]

        workflow_dict = workflow.to_dict()
        assert workflow_dict["environment_variables"][0]["value"] == ""
        assert workflow_dict["environment_variables"][1]["value"] == "text"

        workflow_dict = workflow.to_dict(include_secret=True)
        assert workflow_dict["environment_variables"][0]["value"] == "secret"
        assert workflow_dict["environment_variables"][1]["value"] == "text"


class TestWorkflowNodeExecution:
    def test_execution_metadata_dict(self):
        node_exec = WorkflowNodeExecutionModel()
        node_exec.execution_metadata = None
        assert node_exec.execution_metadata_dict == {}

        original = {"a": 1, "b": ["2"]}
        node_exec.execution_metadata = json.dumps(original)
        assert node_exec.execution_metadata_dict == original
