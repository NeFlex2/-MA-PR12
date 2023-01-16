from fastapi import FastAPI, HTTPException
from template import Template

templates: list[Template] = [
    Template(1000, 'First template', 'Content'),
    Template(1001, 'Second template', 'Long, very long text')
]

app = FastAPI()


@app.get("/v1/templates")
async def get_templates():
    return templates

@app.get("/v1/templates/{id}")
async def get_templates_by_id(id: int):
    result = [item for item in templates if item.id == id]
    if len(result) > 0:
        return result[0]
    
    raise HTTPException(status_code=404, detail="Template not found")