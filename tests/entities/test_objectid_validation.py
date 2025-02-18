from bson import ObjectId

from src.entities.schemas.base_data.base_schemas import IDSchema


class TestProjectIDSchema:
    def test_validate_object_id_from_mongo(self):
        obj_id = ObjectId()
        mongo_data = {"_id": obj_id}

        schema = IDSchema.model_validate(mongo_data)

        assert schema.id == str(obj_id)

    def test_model_dump_to_mongo(self):
        obj_id = "65c0428d5f9e7a8f74d3c8b9"
        schema = IDSchema(id=obj_id)

        mongo_ready_data = schema.model_dump(by_alias=True)

        assert mongo_ready_data == {"_id": obj_id}

    def test_object_id_as_string(self):
        obj_id = "65c0428d5f9e7a8f74d3c8b9"
        schema = IDSchema.model_validate({"_id": obj_id})

        assert schema.id == obj_id
