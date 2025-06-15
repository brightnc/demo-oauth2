from sqlalchemy.orm import Session
from app.models.user_model import UserCredential,UserDetail
from datetime import datetime,UTC
from app.schemas.user_schema import UserRegister
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_user(self, username: str) -> UserCredential:
        return self.db.query(UserCredential).filter(UserCredential.username == username).first()
    
    def create_user(self, user: UserRegister) -> UserCredential:
        try:
            # Create UserCredential first
            user_data = UserCredential(
                username=user.username,
                password=user.password,
                hash_type="bcrypt",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            
            # Add and flush to get the ID
            self.db.add(user_data)
            self.db.flush()
            
            # Create UserDetail with the generated user_id
            user_detail = UserDetail(
                user_id=user_data.id,
                name=user.details.name,
                email=user.details.email,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            
            # Add user_detail to session
            self.db.add(user_detail)
            
            # Commit transaction
            self.db.commit()
            
            # Refresh both objects after successful commit
            self.db.refresh(user_data)
            self.db.refresh(user_detail)
            
            return user_data
            
        except Exception as e:
            # Rollback transaction on error
            self.db.rollback()
            raise Exception(f"Failed to create user: {str(e)}")
    
    def update_user(self, user: UserCredential) -> UserCredential:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user: UserCredential) -> UserCredential:
        self.db.delete(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    