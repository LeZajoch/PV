class SchoolProfile:
    def __init__(self, first_name, last_name, username, favorite_school_subject, favorite_school, favorite_teacher):
        """
        Inicializace uživatelského profilu.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.favorite_school_subject = favorite_school_subject
        self.favorite_school = favorite_school
        self.favorite_teacher = favorite_teacher

    def toString(self):
        """
        Vrátí textovou reprezentaci profilu.
        """
        return (f"User Profile:\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Favorite School Subject: {self.favorite_school_subject}\n"
                f"Favorite School: {self.favorite_school}\n"
                f"Favorite Teacher: {self.favorite_teacher}")
