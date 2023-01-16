from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from documents_service.app.document import Document, CreateDocumentModel

documents: list[Document] = [
    Document(0, 'First doc', 'Content'),
    Document(1, 'Second doc', 'Long, very long text')
]

def add_document(content: CreateDocumentModel):
   id = len(documents)
   documents.append(Document(id, content.title, content.body))
   return id

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

###
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "docs-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

# Jaeger
###

###
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

# Prometheus
###        

###
# SQL

@app.post("/v1/docs", response_model=schemas.SQLDocument)
def add_doc(document: schemas.CreateDocumentModel, db: Session = Depends(get_db)):
    # db_document = crud.get_docs_by_id(db, document_id=document)
    # if db_document:
    #    raise HTTPException(status_code=400, detail="Title already registered")
    return crud.add_doc(db=db, document=document)


@app.get("/v1/docs", response_model=list[schemas.SQLDocument])
def get_docs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_docs(db, skip=skip, limit=limit)
    return documents


@app.get("/v1/docs/{id}", response_model=schemas.SQLDocument)
def get_docs_by_id(id: int, db: Session = Depends(get_db)):
    db_document = crud.get_docs_by_id(db, document_id=id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="SQLDocument not found")
    return db_document

# SQL
###

# @app.get("/__health")
# async def check_service():
#     return