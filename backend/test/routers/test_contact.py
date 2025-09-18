import pytest
from httpx import AsyncClient


async def create_contact(body: dict, async_client: AsyncClient) -> dict:
    response = await async_client.post("/contacts", json=body)
    return response.json()

@pytest.fixture()
async def created_complete_contact(async_client: AsyncClient):
    return await create_contact({
        "name": "TestName",
        "primary_surname": "TestPrimarySurname",
        "secondary_surname": "TestSecondarySurname",
        "phone": "+56911222333",
        "email": "test@email.com",
        "notes": "Test notes"
    }, async_client)


@pytest.mark.anyio
async def test_create_contact(async_client: AsyncClient):
    body = {
        "name": "TestName",
        "primary_surname": "TestPrimarySurname",
        "secondary_surname": "TestSecondarySurname",
        "phone": "+56911222333",
        "email": "test@email.com",
        "notes": "Test notes"
    }

    response = await async_client.post("/contacts/", json=body)

    assert response.status_code == 201
    assert body.items() <= response.json().items()
