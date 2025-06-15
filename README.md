# OAuth2 Demo Project

โปรเจคสาธิตการใช้งาน OAuth2 Authorization Code Flow ประกอบด้วย 2 ส่วนหลัก:

1. Frontend (React + Vite)
2. Backend (FastAPI)

## โครงสร้างโปรเจค

```
demo-oauth2/
├── oauth2-frontend-demo/     # Frontend React application
└── OAuth2/                  # Backend FastAPI application
```

## การติดตั้ง

### Backend (FastAPI)

1. สร้าง virtual environment:

```bash
cd OAuth2
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
.\venv\Scripts\activate  # Windows
```

2. ติดตั้ง dependencies:

```bash
pip install -r requirements.txt
```

3. สร้างไฟล์ .env:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./sql_app.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

4. รัน server:

```bash
uvicorn app.main:app --reload
```

### Frontend (React)

1. ติดตั้ง dependencies:

```bash
cd oauth2-frontend-demo
npm install
```

2. สร้างไฟล์ .env:

```env
VITE_AUTH_SERVER=http://localhost:8000
VITE_CLIENT_ID=your-client-id
VITE_CLIENT_SECRET=your-client-secret
VITE_REDIRECT_URI=http://localhost:5173/callback
```

3. รัน development server:

```bash
npm run dev
```

## การใช้งาน

1. เปิดเบราว์เซอร์ไปที่ http://localhost:5173
2. คลิกปุ่ม "Login with OAuth"
3. กรอก username และ password
4. ระบบจะ redirect กลับมาที่ frontend พร้อม access token

## API Endpoints

### Authorization Server

- `GET /api/v1/auth/authorize` - Authorization endpoint
- `POST /api/v1/auth/token` - Token endpoint
- `GET /api/v1/auth/login` - Login page
- `POST /api/v1/auth/login` - Login endpoint
- `POST /api/v1/auth/register` - Register endpoint

### Resource Server

- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users` - Get all users (admin only)

## การพัฒนา

### Backend

- FastAPI framework
- SQLAlchemy ORM
- Pydantic models
- JWT tokens
- Session-based authentication

### Frontend

- React 18
- React Router v6
- Vite
- Modern JavaScript (ES6+)

## Security Features

- CSRF protection using state parameter
- Secure session handling
- Token-based authentication
- Password hashing
- CORS configuration

## License

MIT
