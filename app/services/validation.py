from pydantic import BaseModel, field_validator, model_validator
from requests import get, head
import ipaddress, sys
from socket import gethostbyname
from typing import Optional
from logs import logger


size = (1024**2)*3
timeOUT = 3


class validate_request(BaseModel):
    url: str

    @field_validator('url', mode='before')
    def validate_url_before(cls, val):
        if not (val.startswith("http://") or val.startswith("https://")): val = "http://" + val
        try:
            ip = gethostbyname(val.split("//")[-1])
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                logger.warning(f"URL resolves to internal IP: {ip}")
                raise ValueError(f"URL resolves to internal IP: {ip}")
            return val
        except Exception as e:
            logger.error(f"Invalid URL : {val} | {e}")
            raise ValueError("Invalid URL format or DNS error")

    @field_validator('url', mode='after')
    def validate_url_after(cls, val):
        try:
            resp = head(val, allow_redirects=True, timeout=timeOUT)
            if resp.status_code in [200, 201, 203]:
                return val
            else:
                logger.warning(f"Unreachable URL : {val}")
                raise ValueError("Unreachable or invalid response")
        except Exception as e:
            logger.warning(f"Invalid URL : {val} | {e}")
            raise ValueError("Unreachable URL")

    method: str

    @field_validator('method', mode='before')
    def validate_method_before(cls, val): return val.upper()

    @field_validator('method', mode='after')
    def validate_method_after(cls, val):
        if val.upper() in ["GET", "POST", "PUT", "DELETE"]: return val.upper()
        else:
            logger.warning(f"Invalid Method / Method Not Allowed : {val}")
            raise ValueError(f"Invalid HTTP Method: {val}")

    # --------------------
    data: Optional[dict] = None
    @model_validator(mode="after")
    def validate_data_based_on_method(self):

        if self.method in ["POST", "PUT"]:
            if not isinstance(self.data, dict):
                logger.warning("POST/PUT require a dict data body")
                raise ValueError("POST/PUT require data as dict")

            if sys.getsizeof(self.data) > size:
                logger.warning(f"Data size exceeds {size} bytes : {self.data}")
                raise ValueError(f"Data size exceeds {size} bytes")
        else:
            if self.data not in (None, {}):
                logger.warning("GET/DELETE must not contain data")
                raise ValueError("GET/DELETE must not contain a body")
        return self