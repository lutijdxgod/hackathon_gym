from fastapi import HTTPException, status


wrong_credentials = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверные данные.")
