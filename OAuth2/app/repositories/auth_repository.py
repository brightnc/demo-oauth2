from sqlalchemy.orm import Session
from app.schemas.auth import OAuth2ClientResponse, OAuth2ClientCreate
from app.models.auth_model import OAuth2Client,OAuth2Token,TokenType
from datetime import datetime,UTC

class OAuth2Repository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_client(self, client_id: str, client_secret: str, **client_data) -> OAuth2ClientResponse:
        # Convert lists to comma-separated strings
        redirect_uris = ",".join(client_data.get("redirect_uris", []))
        grant_types = ",".join(client_data.get("grant_types", []))
        response_types = ",".join(client_data.get("response_types", []))

        client = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            name=client_data.get("name"),
            description=client_data.get("description"),
            redirect_uris=redirect_uris,
            grant_types=grant_types,
            response_types=response_types,
            scope=client_data.get("scope"),
            token_endpoint_auth_method=client_data.get("token_endpoint_auth_method")
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return OAuth2ClientResponse.model_validate(client)
    
    def create_token(self, token, token_type, client_id, scope, expires_at, user_id) -> OAuth2Token:
        token = OAuth2Token(
            token=token,
            token_type=token_type,
            client_id=client_id,
            scope=scope,
            expires_at=expires_at,
            user_id=user_id
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    

    def get_client(self, client_id: str) -> OAuth2ClientResponse:
        return self.db.query(OAuth2Client).filter(OAuth2Client.client_id == client_id).first()
    
    def find_authorization_code(self, code: str) -> OAuth2Token:
        return self.db.query(OAuth2Token).filter(OAuth2Token.token == code, OAuth2Token.revoked == False).first()
    
    def revoke_token(self, token: str) -> None:
        # Find the token first
        token_obj = self.db.query(OAuth2Token).filter(OAuth2Token.token == token).first()
        if token_obj:
            token_obj.revoked = True
            token_obj.revoked_at = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(token_obj)