from datasette_test import Datasette
import pytest


@pytest.mark.asyncio
async def test_proxy_plugin(httpx_mock):
    httpx_mock.add_response(
        url="http://example.com/",
        text="Hello from example.com",
    )
    datasette = Datasette(
        plugin_config={
            "datasette-proxy-url": {
                "paths": [
                    {"path": "/proxy", "backend": "http://example.com/"},
                ]
            }
        }
    )
    response = await datasette.client.get("/proxy")
    assert response.status_code == 200
    assert response.text == "Hello from example.com"
    request = httpx_mock.get_request()
    assert request.url == "http://example.com/"
