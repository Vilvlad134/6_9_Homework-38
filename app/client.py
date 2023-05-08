import asyncio
import aiohttp


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.post(
#             'http://0.0.0.0:8080/users/',
#             json={
#                 'email': 'snt3@mail',
#                 'password': '1234'
#             }
#         )
#
#         data = await response.json()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.post(
#             'http://0.0.0.0:8080/login/',
#             json={
#                 'email': 'snt3@mail',
#                 'password': '1234'
#             }
#         )
#
#         data = await response.json()
#         print(data)


async def resp():
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            'http://0.0.0.0:8080/users/1'

        )

        data = await response.text()
        print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.patch(
#             'http://0.0.0.0:8080/users/5',
#             json={
#                 'email': 'snt3@mail',
#                 'password': '1234'
#             },
#             headers={
#                 'token': '395c6438-6688-4710-affe-79f2fcf858ce'
#             }
#         )
#         data = await response.text()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.delete(
#             'http://0.0.0.0:8080/users/4',
#             headers={
#                 'token': 'b0ea7d1a-2bd9-4b28-9fcc-33ca9e371212'
#             }
#         )
#
#         data = await response.text()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.post(
#             'http://0.0.0.0:8080/users/advertisments/',
#             json={'header': 'computer',
#                 'description': 'good'},
#             headers={'token': '69ad8bb1-c30c-453e-9b7a-7e5099a7fce3'}
#         )
#         data = await response.text()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(
#             'http://0.0.0.0:8080/users/advertisments/5'
#         )
#         data = await response.text()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.patch(
#             'http://0.0.0.0:8080/users/advertisments/5',
#             json={
#                 'description': 'very good comp',
#                 'header': 'computer intel'
#             },
#             headers={
#                 'token': '69ad8bb1-c30c-453e-9b7a-7e5099a7fce3'
#             }
#         )
#         data = await response.text()
#         print(data)


# async def resp():
#     async with aiohttp.ClientSession() as session:
#         response = await session.delete(
#             'http://0.0.0.0:8080/users/advertisments/5',
#             headers={
#                 'token': '69ad8bb1-c30c-453e-9b7a-7e5099a7fce3'
#             }
#         )
#         data = await response.text()
#         print(data)

asyncio.run((resp()))