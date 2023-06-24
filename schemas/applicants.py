from beanie import Document


class ApplicantsCompany(Document):
    image_url: str | None = None
    image_file_id: str | None = None

    class Settings:
        name = "applicants_companies"


class ApplicantsEntryInfo(Document):
    entry_start_date_info: str
    documents: str
