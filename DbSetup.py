class DbSetup:
    Uri = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="notoms",
        password="",
        hostname="notoms.mysql.pythonanywhere-services.com",
        databasename="notoms$default",
    )
    @staticmethod
    def getUri():
        return DbSetup.Uri
