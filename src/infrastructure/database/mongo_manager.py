from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection
from pymongo.results import InsertManyResult, InsertOneResult

from src.entities.enums.collection_enum import DBCollectionEnum
from src.infrastructure.database.mongo_dependency import MongoDBDependency


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
        """
        Asynchronous context manager for managing MongoDB sessions.

        :param session: Existing MongoDB session to use. If None, a new session will be created.
        :type session: AsyncIOMotorClientSession | None
        :returns: An asynchronous generator that yields the session.
        :rtype: AsyncGenerator
        """
        if session:
            yield session
        else:
            async with self._mongo_dep.session() as new_session:
                yield new_session

    async def _get_collection(self, collection: DBCollectionEnum | AsyncIOMotorCollection):
        """
        Returns the appropriate MongoDB collection for the given input.

        :param collection: A DBCollectionEnum member or an AsyncIOMotorCollection object.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :returns: An instance of AsyncIOMotorCollection representing the requested collection.
        :rtype: AsyncIOMotorCollection
        """
        if isinstance(collection, DBCollectionEnum):
            return await self._mongo_dep.get_collection(collection_name=collection)

        return collection

    async def create_user(self, collection: DBCollectionEnum, insert_data, return_schema):
        """
        Creates a new user in the specified database collection.

        :param collection: The database collection to use for creating the user.
        :type collection: DBCollectionEnum
        :param insert_data: Data required to create the user, typically containing details like telegram_id, name, etc.
        :type insert_data: Any
        :param return_schema: Schema definition used to format and validate the returned user data.
        :type return_schema: Any
        :returns: The newly created user document from the database.
        :rtype: Any
        """
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

    async def find_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        value: str | bool | int | ObjectId,
        field: str = "_id",
        session: AsyncIOMotorClientSession | None = None,
    ):
        """
        Finds a single document in the specified collection based on the given value and field.

        :param collection: The database collection to query.
            Can be an instance of DBCollectionEnum or AsyncIOMotorCollection.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param schema: Pydantic schema used for validation and conversion of the document.
        :param value: Value to search for in the specified field.
            Supported types include str, bool, int, and ObjectId.
        :type value: str | bool | int | ObjectId
        :param field: Field in which to search for the value. Defaults to "_id".
        :type field: str
        :param session: Optional MongoDB client session to use during the operation.
        :type session: AsyncIOMotorClientSession | None
        :returns: The document as a Pydantic model instance, or None if no document is found.
        :rtype: schema.model_validate return type or None
        """
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            document = await collection.find_one({field: value}, session=session)

            if not document:
                return None

            return schema.model_validate(document, from_attributes=True)

    async def find_one_by_id(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        value: str,
        session: AsyncIOMotorClientSession | None = None,
    ):
        """
        Finds a document in the database collection by its unique identifier.

        :param collection: The collection to search within,
            can be either an enum value or an AsyncIOMotorCollection instance.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param schema: The schema for validation or processing the found document.
        :type schema:
        :param value: The string representation of the ObjectId to find in the database.
        :type value: str
        :param session: An optional session object for the operation.
        :type session: AsyncIOMotorClientSession | None
        :returns: The document matching the specified ObjectId, if found; otherwise, None.
        :rtype: dict | None
        """
        return await self.find_one(collection=collection, schema=schema, value=ObjectId(value), session=session)

    async def find_one_with_match_filter(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        sub_collection: str,
        search_field: str,
        search_value: str,
        filter_value: str | bool | int | ObjectId,
        filter_field: str = "_id",
        session: AsyncIOMotorClientSession | None = None,
    ):
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            document = await collection.find_one(
                {filter_field: filter_value, f"{sub_collection}.{search_field}": search_value},
                session=session,
            )

            if not document:
                return None

            return schema.model_validate(document, from_attributes=True)

    async def find(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        session: AsyncIOMotorClientSession | None = None,
        filter_query: dict | None = None,
    ) -> list:
        """
        Asynchronously finds documents in a MongoDB collection using the provided schema.

        :param collection: The collection to search within.
            This can be either a predefined enumeration or an actual `AsyncIOMotorCollection` instance.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param schema: An object used to parse and validate document structures.
        :type schema: Any (typically a Pydantic model)
        :param session: An optional session to use for the query.
            If not provided, a new session will be created automatically.
        :type session: AsyncIOMotorClientSession | None
        :param filter_query: A dictionary containing the query criteria for filtering documents.
            Defaults to an empty dictionary if not provided.
        :type filter_query: dict | None
        :return: A list of parsed and validated documents.
        :rtype: list
        """
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
        """
        Inserts a single document into a database collection asynchronously.

        :param collection: The collection into which the document will be inserted.
            It can be an instance of `DBCollectionEnum` or `AsyncIOMotorCollection`.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param data: The document data to be inserted. The data should be a model that
            supports the `model_dump(mode="json")` method.
        :type data: Any
        :param session: An optional session for the operation. If not provided, a new session will be created.
            :type session: AsyncIOMotorClientSession | None
        :returns: A result object containing information about the inserted document.
        :rtype: InsertOneResult
        """
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            return await collection.insert_one(data.model_dump(mode="json"), session=session)

    async def insert_many(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        data_list: Sequence,
        session: AsyncIOMotorClientSession | None = None,
    ) -> InsertManyResult:
        """
        Inserts multiple documents into a MongoDB collection asynchronously.

        :param collection: The MongoDB collection to insert data into.
            This can be an instance of DBCollectionEnum or AsyncIOMotorCollection.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param data_list: A sequence of document data objects that need to be inserted into the collection.
            Each object should have a model_dump method for converting it to JSON format.
        :type data_list: Sequence
        :param session: An optional asynchronous client session for transaction support.
            Defaults to None if transactions are not required.
        :type session: AsyncIOMotorClientSession | None
        :returns: A result object containing information about the successful insertion of documents,
            including the inserted IDs and the number of documents inserted.
        :rtype: InsertManyResult
        """
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)

            documents = [data.model_dump(mode="json") for data in data_list]

            return await collection.insert_many(documents, session=session)

    async def update_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        filter_field: str,
        filter_value: str | bool | int | ObjectId,
        update_field: str,
        update_value: str | bool | int,
    ) -> None:
        """
        Updates a single document in the specified collection based on the given filter criteria.

        :param collection: The collection to update,
            either as an enumeration from DBCollectionEnum or an AsyncIOMotorCollection instance.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param filter_field: The field name used for filtering the document.
        :type filter_field: str
        :param filter_value: The value associated with the filter field.
            Can be of type string, boolean, integer, or ObjectId.
        :type filter_value: str | bool | int | ObjectId
        :param update_field: The field name to update in the document.
        :type update_field: str
        :param update_value: The new value for the update field. Can be of type string, boolean, or integer.
        :type update_value: str | bool | int
        """
        async with self._get_session() as session:
            collection = await self._get_collection(collection=collection)

            await collection.update_one(
                {filter_field: filter_value}, {"$set": {update_field: update_value}}, session=session
            )

    async def update_custom(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        filter_field: str,
        filter_value: str | bool | int | ObjectId,
        update_field: dict | str,
        update_value: dict | list | str | int | bool,
        command: str,
    ) -> None:
        async with self._get_session() as session:
            collection = await self._get_collection(collection=collection)

            res = await collection.update_one(
                {filter_field: filter_value},
                {command: {update_field: update_value}},
                session=session,
            )
            print(res)

    async def delete_one(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        filter_query: dict,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        """
        Delete one document by filter.

        :param collection: Collection of documents.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param filter_query: dict with filter criteria.
        :type filter_query: dict
        :param session: An optional asynchronous client session for transaction support
        :type session: AsyncIOMotorClientSession | None
        """
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)
            await collection.delete_one(filter_query, session=session)

    async def delete_one_by_id(
        self,
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        value: str,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        """
        Delete document by uid.

        :param collection: Collection for deleting operation.
        :type collection: DBCollectionEnum | AsyncIOMotorCollection
        :param value: string representation of document's ObjectId.
        :type value: str
        :param session: An optional asynchronous client session for transaction support
        :type session: AsyncIOMotorClientSession | None
        """
        await self.delete_one(
            collection=collection,
            filter_query={"_id": ObjectId(value)},
            session=session,
        )

    async def aggregate(
        self,
        pipeline: list[dict],
        collection: DBCollectionEnum | AsyncIOMotorCollection,
        schema,
        item_key: str,
        session: AsyncIOMotorClientSession | None = None,
    ) -> tuple[list, int]:
        async with self._get_session(session=session) as session:
            collection = await self._get_collection(collection=collection)
            cursor = collection.aggregate(pipeline=pipeline, session=session)
            result = await cursor.to_list(length=1)

            if not result:
                return [], 0

            doc = result[0]

            paginated_items = [schema(**item) for item in doc.get(item_key, [])]

            if doc.get("total"):
                if isinstance(doc.get("total"), list):
                    total_count = doc.get("total", [{}])[0].get("count", 0)
                elif isinstance(doc.get("total"), int):
                    total_count = doc.get("total", 0)
            else:
                total_count = 0

            return paginated_items, total_count
