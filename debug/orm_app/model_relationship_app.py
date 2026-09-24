from sqlalchemy import ForeignKey,String,create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship,declarative_base


db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"
engine = create_engine(db_url, pool_size= 50, echo=True)

class Base(DeclarativeBase):
    pass

class Teacher(Base):
    __tablename__ = "mapped_teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    tname: Mapped[str] = mapped_column(String(30))

    # 反向关系：这个老师当班主任的所有班级
    head_teacher_of: Mapped[list["Class"]] = relationship(
        "Class",
        foreign_keys="Class.head_teacher_id",
        back_populates="head_teacher"
    )
    coach_teacher_of: Mapped[list["Class"]] = relationship(
        "Class",
        foreign_keys="Class.coach_teacher_id",
        back_populates="coach_teacher"
    )

class Class(Base):
    __tablename__ = "mapped_classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    class_num: Mapped[str] = mapped_column(String(30))

    head_teacher_id: Mapped[int] = mapped_column(ForeignKey("mapped_teachers.id"))
    coach_teacher_id: Mapped[int] = mapped_column(ForeignKey("mapped_teachers.id"))

    head_teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        foreign_keys=[head_teacher_id],
        back_populates="head_teacher_of"
    )
    coach_teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        foreign_keys=[coach_teacher_id],
        back_populates="coach_teacher_of"
    )

Base.metadata.create_all(engine)