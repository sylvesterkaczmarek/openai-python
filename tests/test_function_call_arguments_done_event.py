from openai.types.beta import BetaResponseFunctionCallArgumentsDoneEvent
from openai.types.responses import ResponseFunctionCallArgumentsDoneEvent


EVENT = {
    "type": "response.function_call_arguments.done",
    "arguments": "{}",
    "item_id": "fc_test",
    "output_index": 0,
    "sequence_number": 1,
}


def test_function_call_arguments_done_allows_missing_name() -> None:
    event = ResponseFunctionCallArgumentsDoneEvent.model_validate(EVENT)

    assert event.name is None


def test_beta_function_call_arguments_done_allows_missing_name() -> None:
    event = BetaResponseFunctionCallArgumentsDoneEvent.model_validate(EVENT)

    assert event.name is None
