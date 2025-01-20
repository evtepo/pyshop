from datetime import datetime, UTC

import jwt
from django.conf import settings

from authentication.models import CustomUser, RefreshToken


def obtain_pair_tokens(user: CustomUser) -> dict[str, str]:
    refresh_token = RefreshToken(user=user, exp_time=datetime.now() + settings.REFRESH_EXPIRE)
    refresh_token.save()

    access_token = jwt.encode(
        {
            "sub": user.email,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + settings.ACCESS_EXPIRE,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return {"access_token": access_token, "refresh_token": refresh_token.id}
