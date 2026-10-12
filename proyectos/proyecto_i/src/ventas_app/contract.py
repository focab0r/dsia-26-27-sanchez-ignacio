

from typing import Literal
from pydantic import BaseModel, Field




class VentaModel (BaseModel):

	fecha:				str
	region:				Literal["Sur", "Norte", "Este", "Oeste"]
	producto:			str
	unidades:			int = Field (ge=0)
	precio_unitario:	float = Field (ge=0)
	cliente_id:			str


	