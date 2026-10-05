

from pydantic import BaseModel, Field




class YearModel (BaseModel):

	year:		int = Field (ge=1900, lt=2027)
	september:	int = Field (ge=0)
	october:	int = Field (ge=0)
	november:	int = Field (ge=0)
	december:	int = Field (ge=0)
	january:	int = Field (ge=0)
	february:	int = Field (ge=0)
	march:		int = Field (ge=0)
	april:		int = Field (ge=0)
	may:		int = Field (ge=0)
	june:		int = Field (ge=0)
	target:		int = Field (ge=0)


	