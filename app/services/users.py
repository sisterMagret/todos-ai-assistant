from typing import List
from app.database.models.users import User
from sqlalchemy.orm import Session

from app.utils.exceptions import UserAlreadyExistsError


class UserService:
    
    @classmethod
    async def get_users(
        cls,
        db: Session
    ) -> List[User]:
        """Get all users.

        Args:
            db: Database session.

        Returns:
            List[User]: List of users.
        """
        return db.query(User).all()
    
    
    @classmethod
    def create_user(
        cls, db: Session, user_data: dict
    ) -> User:
        """Create a new user.

        Args:
            db: Database session.
            user_data: User creation data.

        Returns:
            User: The created user.

        Raises:
            UserAlreadyExistsError: If user with email already exists.
        """
        existing_user = db.query(User).filter(
            (User.phone_number == user_data["phone_number"])
            ).first()
        if existing_user:
            raise UserAlreadyExistsError(
                "User with this email already exists"
            )

        user = User(**user_data)
        db.add(user)
        db.commit()
        return user

    
    
        

        
        