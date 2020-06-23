# python Final Project on Requests and Flask

>This service contains the covid information of India with states and district.
### '/getStateData' methods=['POST']
* It pulls the data from third party service and filters with the state code.
#### Request
---
{
	"scode":"ALL",
	"total": "Y"
	}
---

### '/writeData' methods=['POST']
* It pulls the data from json file update the request details in the file.
#### Request
---
{
   "active": 7803,
   "confirmed": 7803,
   "county": "Newyark",
   "state" : "New york",
   "recovered": 200
}
---

#### Header Info:
---

---
