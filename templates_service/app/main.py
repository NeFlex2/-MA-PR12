from fastapi import FastAPI, HTTPException
from templates_service.app.template import Template, CreateTemplateModel

templates: list[Template] = [
    # Template(1000, 'First template', 'Content'),
    # Template(1001, 'Second template', 'Long, very long text')
]


def add_template(content: CreateTemplateModel):
    id = len(templates)
    templates.append(Template(id, content.title, content.body))
    return id


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


@app.post("/v1/templates")
async def add_temp(content: CreateTemplateModel):
    add_template(content)
    return templates[-1]


@app.get("/__health")
async def check_service():
    return