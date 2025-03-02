from src.core.settings import get_logger, get_settings
from src.entities.schemas.profile_data.language_schema import LanguageSchema

logger = get_logger()


class ProfileService:
    def __init__(self):
        pass

    @staticmethod
    def get_allowed_lang():
        return [LanguageSchema(select_language=lang) for lang in get_settings().ALLOWED_LANGUAGES]

    async def get_languages(self, page: int) -> tuple[list[LanguageSchema], int]:
        """
        Retrieves a list of allowed languages and their total count.

        :param page: Page number to retrieve.
        :type page: int
        :return: A tuple containing a list of language codes and the total count.
        :rtype: Tuple[List[LanguageSchema], int]
        """
        all_languages = self.get_allowed_lang()
        logger.info(f"all_languages: {all_languages}")
        total_count = len(all_languages)

        limit = get_settings().ITEMS_PER_PAGE
        offset = page * limit

        paginated_languages = all_languages[offset : offset + limit]

        return paginated_languages, total_count
