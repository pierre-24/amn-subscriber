from amn_subscriber import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Request(BaseModel):
    surname = db.Column(db.VARCHAR(length=150), nullable=False)
    name = db.Column(db.VARCHAR(length=150), nullable=False)
    email = db.Column(db.VARCHAR(length=150), nullable=False)
    note = db.Column(db.Text, nullable=False)

    @classmethod
    def create(cls, surname: str, name: str, email: str, note: str = ''):
        o = cls()

        o.surname = surname
        o.name = name
        o.email = email
        o.note = note

        return o

    def get_scrambled_email(self):
        n = len(self.name) % 3
        s = self.email.split('@')
        return s[0][:1 + n] + '***' + (s[0][n - 3:] if len(s[0]) >= 4 else '') + '@{}'.format(s[1])
