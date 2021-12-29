import calendar
from datetime import datetime, timedelta
from project.exceptions import DecodeError

import jwt
from flask import current_app

class JWTTokens:
    algo= "HS256"

    def __init__(self):
        self._token_exp_minutes =current_app.config["TOKEN_EXPIRE_MINUTES"]
        self._token_exp_days = current_app.config["TOKEN_EXPIRE_DAYS"]
        self._secret_key = current_app.config["SECRET_KEY"]

    def generate_tokens(self, data:dict):
        now = datetime.now()

        min = now+ timedelta(minutes=self._token_exp_minutes)
        data["exp"] = calendar.timegm(min.timetuple())
        access_token = jwt.encode(data, self._secret_key, algorithm = self.algo)

        days = now + timedelta(days=self._token_exp_days)
        data["exp"] = calendar.timegm(min.timetuple())
        refresh_token = jwt.encode(data, self._secret_key, algorithm=self.algo)

        return {"access_token": access_token, "refresh_token":refresh_token}

    def decode_token(self, refresh_token):
        try:
            return jwt.decode(refresh_token, self._secret_key,[self.algo])
        except Exception:
            raise DecodeError