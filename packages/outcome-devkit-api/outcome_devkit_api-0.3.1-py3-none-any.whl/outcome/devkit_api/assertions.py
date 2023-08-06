"""API response assertions."""

import http
from operator import attrgetter
from typing import Mapping, Optional, Protocol, Sequence, Type, TypedDict, Union

from fastapi import status
from pydantic import BaseModel

ModelType = Type[BaseModel]
JSONResponse = Union[Mapping[str, object], Sequence[Mapping[str, object]]]


class MockResponse:  # pragma: no cover
    status_code: int
    parsed_body: JSONResponse

    def __init__(self, status_code: int, parsed_body: JSONResponse):
        self.status_code = status_code
        self.parsed_body = parsed_body

    def json(self) -> JSONResponse:
        return self.parsed_body


class ResponseLike(Protocol):  # pragma: no cover
    status_code: int

    def json(self) -> JSONResponse:
        ...


class ErrorDetailsLike(TypedDict):  # pragma: no cover
    key: str
    subject: str
    message: str


class ErrorResponseBody(TypedDict, total=False):  # pragma: no cover
    code: int
    error: str
    details: Optional[Sequence[ErrorDetailsLike]]


def resource_not_found_error() -> ErrorResponseBody:  # pragma: no cover
    return {
        'error': http.HTTPStatus(status.HTTP_404_NOT_FOUND).phrase,
        'code': status.HTTP_404_NOT_FOUND,
    }


def internal_server_error() -> ErrorResponseBody:  # pragma: no cover
    return {
        'error': http.HTTPStatus(status.HTTP_500_INTERNAL_SERVER_ERROR).phrase,
        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
    }


def invalid_request_error() -> ErrorResponseBody:  # pragma: no cover
    return {
        'error': http.HTTPStatus(status.HTTP_400_BAD_REQUEST).phrase,
        'code': status.HTTP_400_BAD_REQUEST,
    }


def unauthenticated_error() -> ErrorResponseBody:  # pragma: no cover
    return {
        'error': http.HTTPStatus(status.HTTP_401_UNAUTHORIZED).phrase,
        'code': status.HTTP_401_UNAUTHORIZED,
    }


def assert_unauthorized_response(response: ResponseLike):  # pragma: no cover
    assert_response(response, unauthenticated_error(), status.HTTP_401_UNAUTHORIZED)


def assert_empty_response(response: ResponseLike, status_code: int = status.HTTP_200_OK):  # pragma: no cover
    assert_ok_response(response, None, status_code)


def assert_ok_response(
    response: ResponseLike, expected_body: Optional[JSONResponse], status_code: int = status.HTTP_200_OK,
):  # pragma: no cover
    assert_response(response, expected_body, status_code)


def assert_response_with_model(
    response: ResponseLike, model: ModelType, status_code: int = status.HTTP_200_OK,
):  # pragma: no cover
    assert response.status_code == status_code
    data = response.json()
    assert not isinstance(data, Sequence)
    model(**data)


def assert_internal_error(response: ResponseLike):  # pragma: no cover
    assert_response(response, internal_server_error(), status.HTTP_500_INTERNAL_SERVER_ERROR)


def assert_invalid_request(
    response: ResponseLike, expected_details: Optional[Sequence[ErrorDetailsLike]] = None, ignore_details: bool = True,
):  # pragma: no cover

    if not expected_details and ignore_details:
        data = response.json()
        assert not isinstance(data, Sequence)
        response_json = dict(data)
        response_json.pop('details', None)
        response = MockResponse(response.status_code, response_json)

    expected_response = invalid_request_error()

    if expected_details:
        expected_response['details'] = expected_details

    assert_response(response, expected_response, status.HTTP_400_BAD_REQUEST)


def assert_resource_not_found(response: ResponseLike):  # pragma: no cover
    assert_response(response, resource_not_found_error(), status.HTTP_404_NOT_FOUND)


def assert_record_created(response: ResponseLike, model: ModelType):  # pragma: no cover
    assert_response_with_model(response, model, status.HTTP_201_CREATED)


def assert_record(response: ResponseLike, model: ModelType, expected_record: Optional[object] = None):  # pragma: no cover
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert not isinstance(data, Sequence)
    parsed = model(**data)

    if expected_record:
        assert parsed == expected_record


def assert_empty_list_of_records(response: ResponseLike):  # pragma: no cover
    assert_response(response, [], status.HTTP_200_OK)


def assert_list_of_records_equal(list1: Sequence[object], list2: Sequence[object], key: str = 'identifier'):  # pragma: no cover
    if key is not None:
        assert sorted(list1, key=attrgetter(key)) == sorted(list2, key=attrgetter(key))
    else:
        assert list1 == list2


def assert_list_of_records(
    response: ResponseLike, model: ModelType, expected_records: Optional[Sequence[object]] = None, sort_key: str = 'identifier',
):  # pragma: no cover
    assert response.status_code == status.HTTP_200_OK
    assert_list_of_records_raw(
        response, model, expected_records=expected_records, sort_key=sort_key,
    )


def assert_list_of_records_created(
    response: ResponseLike, model: ModelType, expected_records: Optional[Sequence[object]] = None, sort_key: str = 'identifier',
):  # pragma: no cover
    assert response.status_code == status.HTTP_201_CREATED
    assert_list_of_records_raw(
        response, model, expected_records=expected_records, sort_key=sort_key,
    )


def assert_list_of_records_raw(
    response: ResponseLike, model: ModelType, expected_records: Optional[Sequence[object]] = None, sort_key: str = 'identifier',
):  # pragma: no cover
    records = response.json()

    assert isinstance(records, Sequence)

    parsed = [model(**r) for r in records]

    if expected_records:
        assert_list_of_records_equal(parsed, expected_records, key=sort_key)


def assert_response(response: ResponseLike, expected_body: Optional[JSONResponse], expected_status_code: int):  # pragma: no cover
    assert response.status_code == expected_status_code
    assert response.json() == expected_body
