from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection
from pymongo.results import InsertOneResult

from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.infrastructure.database.mongo_dependency import MongoDBDependency

# TODO: Разобраться с аннотированием схем


class MongoManager:
    """
    Manages interaction with MongoDB database.
    """

    def __init__(self, mongo_dep: MongoDBDependency) -> None:
        """
        Initializes an instance of the class with a MongoDBDependency.

        :param mongo_dep: The dependency object for MongoDB operations.
        :type mongo_dep: MongoDBDependency
        """
        self._mongo_dep = mongo_dep

    @asynccontextmanager
    async def _get_session(self, session: AsyncIOMotorClientSession | None = None) -> AsyncGenerator:
        if session:
            yield session
        else:
            async with self._mongo_dep.session() as new_session:
                yield new_session

    async def _get_collection(self, collection: DBCollectionEnum | AsyncIOMotorCollection):
        if isinstance(collection, DBCollectionEnum):
            return await self._mongo_dep.get_collection(collection_name=collection)

        return collection

    async def create_user(self, collection: DBCollectionEnum, insert_data, return_schema):
        async with self._get_session() as session:
            collection = await self._get_collection(collection=collection)

            if existing_user := await self.find_one(
                collection=collection,
                schema=return_schema,
                field="telegram_id",
                value=insert_data.telegram_id,
                session=session,
            ):
                return existing_user

            result = await self.insert_one(collection=collection, data=insert_data, session=session)

            return await self.find_one(
                collection=collection, schema=return_schema, value=result.inserted_id, session=session
            )

    async def get_projects(self, offset: int, limit: int) -> tuple[list[ProjectSchema], int]:
        async with self._get_session() as session:
            collection = await self._mongo_dep.get_collection(DBCollectionEnum.PROJECT)

            result = await collection.find({}, session=session).skip(offset).limit(limit)
            projects = [ProjectSchema(**doc) async for doc in result]

            total_count = await collection.count_documents({}, session=session)

            return projects, total_count

    async def count_documents(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        filter_query: dict | None = None,
        session: AsyncIOMotorClientSession | None = None,
    ):
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            return await collection.count_documents(filter_query, session=session)

    async def find_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        value: str | bool | int,
        field: str = "_id",
        session: AsyncIOMotorClientSession | None = None,
    ):
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            document = await collection.find_one({field: value}, session=session)

            if not document:
                return None

            return schema.model_validate(document, from_attributes=True)

    async def find_with_limit(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        offset: int,
        limit: int,
        session: AsyncIOMotorClientSession | None = None,
        filter_query: dict | None = None,
    ) -> list:
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            documents = collection.find(filter_query, session=session).skip(offset).limit(limit)
            results = [schema(**doc) async for doc in documents]

            return results

    async def find(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        session: AsyncIOMotorClientSession | None = None,
        filter_query: dict | None = None,
    ) -> list:
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            documents = collection.find(filter_query, session=session)
            results = [schema(**doc) async for doc in documents]

            return results

    async def insert_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        data,
        session: AsyncIOMotorClientSession | None = None,
    ) -> InsertOneResult:
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            return await collection.insert_one(data.model_dump(mode="json"), session=session)

    async def update_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        filter_field: str,
        filter_value: str | bool | int,
        update_field: str,
        update_value: str | bool | int,
    ) -> None:
        async with self._get_session() as session:
            collection = await self._get_collection(collection=collection)

            await collection.update_one(
                {filter_field: filter_value}, {"$set": {update_field: update_value}}, session=session
            )
