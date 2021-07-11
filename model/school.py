import pymongo


class SchoolCommandModel:
    def __init__(self, db: pymongo.database.Database):
        """
        db : pymongo.database.Database

        self.collect : pymongo.collection.Collection
        """
        self.collect: pymongo.collection.Collection = db["school"]

    async def get_school(self, server: str, channel: str) -> dict:
        """
        server : DIscord Server ID

        return : list[ATPT_OFCDC_SC_CODE, SCHOOL_CODCE]
        """
        result = list(
            self.collect.find(
                {"server": server, "channel": channel},
                {
                    "_id": False,
                    "ATPT_OFCDC_SC_CODE": True,
                    "SCHOOL_CODE": True,
                    "SCHUL_KND_SC_NM": True,
                },
            )
        )
        if result:
            self.school: dict = {
                "ATPT_OFCDC_SC_CODE": result[0]["ATPT_OFCDC_SC_CODE"],
                "SCHOOL_CODE": result[0]["SCHOOL_CODE"],
                "SCHUL_KND_SC_NM": result[0]["SCHUL_KND_SC_NM"],
            }
        else:
            self.school: dict = None
        return self.school

    async def register(
        self,
        server: str,
        channel: str,
        ATPT_OFCDC_SC_CODE: str,
        SCHOOL_CODE: str,
        SCHUL_KND_SC_NM: str,
    ) -> bool:
        self.collect.insert(
            {
                "server": server,
                "channel": channel,
                "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
                "SCHOOL_CODE": SCHOOL_CODE,
                "SCHUL_KND_SC_NM": SCHUL_KND_SC_NM,
            }
        )
        return True

    async def delete_school(self, server: str, channel: str) -> bool:
        self.collect.remove({"server": server, "channel": channel})
        return True
