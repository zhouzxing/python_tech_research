from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    create_engine, String, Integer, ForeignKey, DateTime, select, func
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
    Session, selectinload
)


# ============================================================
# 1. 定义 Base 和模型
# ============================================================

class Base(DeclarativeBase):
    """所有模型的基类，SQLAlchemy 2.0 推荐写法"""
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 一对多：一个用户有多个文章
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",  # 删除用户时级联删除文章
        lazy="selectin"                # 查询用户时自动预加载文章
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 多对一：多篇文章属于一个用户
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"


# ============================================================
# 2. 创建引擎和表
# ============================================================

engine = create_engine("sqlite:///users_posts.db", echo=False)
Base.metadata.create_all(engine)


# ============================================================
# 3. CRUD 操作
# ============================================================

def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)  # 刷新以获取数据库生成的 id
    return user


def create_post(session: Session, title: str, content: str, user_id: int) -> Post:
    post = Post(title=title, content=content, user_id=user_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return session.execute(stmt).scalar_one_or_none()


def get_all_users(session: Session) -> List[User]:
    stmt = select(User).order_by(User.id)
    return list(session.execute(stmt).scalars().all())


def update_user_email(session: Session, user_id: int, new_email: str) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    user.email = new_email
    session.commit()
    return True


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)  # cascade 会自动删除关联的 posts
    session.commit()
    return True


# ============================================================
# 4. 复杂查询
# ============================================================

def get_users_with_post_count(session: Session):
    """统计每个用户的文章数"""
    stmt = (
        select(User.name, func.count(Post.id).label("post_count"))
        .outerjoin(Post, User.id == Post.user_id)
        .group_by(User.id)
        .order_by(func.count(Post.id).desc())
    )
    return session.execute(stmt).all()


def get_posts_by_user(session: Session, user_id: int) -> List[Post]:
    """查询某个用户的所有文章"""
    stmt = select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())
    return list(session.execute(stmt).scalars().all())


# ============================================================
# 5. 演示
# ============================================================

def main():
    with Session(engine) as session:
        # 清理旧数据（演示用）
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

        # 创建用户
        alice = create_user(session, "Alice", "alice@example.com")
        bob = create_user(session, "Bob", "bob@example.com")
        print("创建用户:", alice, bob)

        # 创建文章
        create_post(session, "Alice 的第一篇", "Hello world", alice.id)
        create_post(session, "Alice 的第二篇", "SQLAlchemy 真香", alice.id)
        create_post(session, "Bob 的独苗", "Python ORM", bob.id)

        # 查询
        print("\n所有用户:")
        for u in get_all_users(session):
            print(f"  {u} -> 文章: {[p.title for p in u.posts]}")

        print("\n用户文章数统计:")
        for name, count in get_users_with_post_count(session):
            print(f"  {name}: {count} 篇")

        # 更新
        update_user_email(session, alice.id, "alice_new@example.com")
        print("\n更新后:", get_user_by_id(session, alice.id))

        # 删除（级联删除文章）
        delete_user(session, bob.id)
        print("\n删除 Bob 后，所有用户:")
        for u in get_all_users(session):
            print(f"  {u}")


if __name__ == "__main__":
    main()