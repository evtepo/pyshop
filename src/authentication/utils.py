from datetime import datetime, timedelta, UTC

import jwt
from constance import config
from django.conf import settings

from authentication.models import CustomUser, RefreshToken


def obtain_pair_tokens(user: CustomUser) -> dict[str, str]:
    refresh_token = RefreshToken(
        user=user,
        exp_time=datetime.now() + timedelta(days=config.REFRESH_EXPIRE),
    )
    refresh_token.save()

    access_token = jwt.encode(
        {
            "sub": user.email,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(seconds=config.ACCESS_EXPIRE),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return {"access_token": access_token, "refresh_token": refresh_token.id}
