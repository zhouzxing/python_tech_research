class Field:
    """字段描述符：记录列名和类型"""
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class IntegerField(Field):
    def __init__(self, primary_key=False):
        super().__init__("INTEGER")
        self.primary_key = primary_key


class StringField(Field):
    def __init__(self, max_length=255):
        super().__init__(f"VARCHAR({max_length})")


class ModelMeta(type):
    """元类：在类创建时收集字段，生成 SQL"""
    def __new__(mcs, name, bases, namespace):
        # 跳过基类 Model 本身
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)

        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value

        # 把收集到的字段挂到类上
        namespace["_fields"] = fields
        namespace["_table"] = name.lower() + "s"

        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class Model(metaclass=ModelMeta):
    """所有模型的基类"""

    @classmethod
    def create_table_sql(cls):
        columns = []
        for name, field in cls._fields.items():
            col = f"{name} {field.column_type}"
            if isinstance(field, IntegerField) and field.primary_key:
                col += " PRIMARY KEY AUTOINCREMENT"
            columns.append(col)
        return f"CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)});"

    @classmethod
    def insert_sql(cls, **kwargs):
        keys = ", ".join(kwargs.keys())
        values = ", ".join(
            f"'{v}'" if isinstance(v, str) else str(v)
            for v in kwargs.values()
        )
        return f"INSERT INTO {cls._table} ({keys}) VALUES ({values});"


# ===== 使用 =====
class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(50)
    email = StringField(100)


class Post(Model):
    id = IntegerField(primary_key=True)
    title = StringField(200)
    user_id = IntegerField()


print(User.create_table_sql())
# CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), email VARCHAR(100));

print(User.insert_sql(name="Alice", email="alice@example.com"))
# INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

print(Post.create_table_sql())
# CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(200), user_id INTEGER);

print(Post.insert_sql(title="orm is best", user_id=1))
print(Post.insert_sql(title="orm simple imp", user_id=1))
print(Post.insert_sql(title="mete class is the base", user_id=1))