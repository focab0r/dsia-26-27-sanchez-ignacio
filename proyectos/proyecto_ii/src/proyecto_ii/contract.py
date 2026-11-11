

from pydantic import BaseModel, Field




class LineModel (BaseModel):

	precipitation:		int = Field (ge=0)
	day:				int = Field (ge=0)
	month:				int = Field (ge=0)
	year:				int = Field (ge=1900, lt=2027)


	