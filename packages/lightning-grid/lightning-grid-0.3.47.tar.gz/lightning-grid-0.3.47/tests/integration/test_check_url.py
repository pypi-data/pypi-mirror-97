from tests.mock_backend import GridAIBackenedTestServer

CLIENT = GridAIBackenedTestServer()


def test_check_url():
    query = """
    query CheckURL ($url: String!) {
        checkUrl (url: $url) {
            statusCode
        }
    }
    """
    values = {'url': 'foo'}
    result = CLIENT.execute(query, values)
    assert result.get('errors') is None
    assert result.get('checkUrl')['statusCode'] == 200
