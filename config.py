class Config:
    # Database configuration (you already have this)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/authors_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional: Disable modification tracking to save resources
    
    # Secret key for session management
    SECRET_KEY = 'your_secret_key_here'  # Replace with a secure random string
    
    # JWT secret key for encoding/decoding JWT tokens
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'  # This key should be used to sign JWT tokens
    
    # Optionally, set an expiration time for the access token (default is 15 minutes)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour expiration for the access token (in seconds)
