from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from database import get_db, init_db
from models import Tool, ToolDeep, Favorite

app = FastAPI(title="System Design Reference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class ToolResponse(BaseModel):
    id: int
    name: str
    category: str
    cap_leaning: Optional[str]
    consistency_model: Optional[str]
    interview_oneliner: Optional[str]
    best_for: Optional[str]
    avoid_when: Optional[str]
    tradeoffs: Optional[str]
    scaling_pattern: Optional[str]
    official_docs_url: Optional[str]
    deep_dive_url_1: Optional[str]
    deep_dive_url_2: Optional[str]
    aws_only: Optional[int]
    is_favorited: bool = False
    
    class Config:
        from_attributes = True

class ToolDeepResponse(BaseModel):
    failure_modes: Optional[str]
    multi_region_notes: Optional[str]
    tuning_gotchas: Optional[str]
    observability_signals: Optional[str]
    alternatives: Optional[str]
    interview_prompts: Optional[str]
    
    class Config:
        from_attributes = True

class ToolDetailResponse(ToolResponse):
    deep_study: Optional[ToolDeepResponse] = None
    
    class Config:
        from_attributes = True

class FavoriteResponse(BaseModel):
    id: int
    tool_id: int
    pinned_order: int
    created_at: datetime
    tool: ToolResponse
    
    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "System Design Reference API", "status": "operational"}

@app.get("/api/tools", response_model=List[ToolResponse])
def get_tools(
    category: Optional[str] = None,
    cap_leaning: Optional[str] = None,
    consistency_model: Optional[str] = None,
    aws_only: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Tool)
    
    if category:
        query = query.filter(Tool.category == category)
    if cap_leaning:
        query = query.filter(Tool.cap_leaning == cap_leaning)
    if consistency_model:
        query = query.filter(Tool.consistency_model == consistency_model)
    if aws_only is not None:
        query = query.filter(Tool.aws_only == (1 if aws_only else 0))
    
    tools = query.all()
    
    favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
    
    results = []
    for tool in tools:
        tool_dict = ToolResponse.from_orm(tool).dict()
        tool_dict["is_favorited"] = tool.id in favorite_tool_ids
        results.append(ToolResponse(**tool_dict))
    
    return results

@app.get("/api/tools/search", response_model=List[ToolResponse])
def search_tools(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    search_term = f"%{q}%"
    tools = db.query(Tool).filter(
        (Tool.name.like(search_term)) |
        (Tool.category.like(search_term)) |
        (Tool.interview_oneliner.like(search_term)) |
        (Tool.best_for.like(search_term)) |
        (Tool.tradeoffs.like(search_term))
    ).all()
    
    favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
    
    results = []
    for tool in tools:
        tool_dict = ToolResponse.from_orm(tool).dict()
        tool_dict["is_favorited"] = tool.id in favorite_tool_ids
        results.append(ToolResponse(**tool_dict))
    
    return results

@app.get("/api/tools/{tool_id}", response_model=ToolDetailResponse)
def get_tool_detail(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    favorite = db.query(Favorite).filter(Favorite.tool_id == tool_id).first()
    
    tool_dict = ToolDetailResponse.from_orm(tool).dict()
    tool_dict["is_favorited"] = favorite is not None
    
    return ToolDetailResponse(**tool_dict)

SCENARIO_MAPPINGS = {
    "payments": {
        "tools": ["DynamoDB", "PostgreSQL", "SQS", "Lambda", "Redis"],
        "reasoning": "Strong consistency for transactions, async processing for reconciliation, caching for fraud checks"
    },
    "chat": {
        "tools": ["DynamoDB", "ElastiCache", "Kinesis", "Lambda", "CloudFront"],
        "reasoning": "Low latency reads, real-time message delivery, global distribution"
    },
    "feed": {
        "tools": ["DynamoDB", "ElastiCache", "S3", "CloudFront", "Lambda"],
        "reasoning": "Fast reads with eventual consistency, CDN for media, scalable fan-out"
    },
    "analytics": {
        "tools": ["S3", "Athena", "Redshift", "Kinesis", "Lambda"],
        "reasoning": "Data lake for raw events, OLAP for aggregations, real-time streaming"
    },
    "search": {
        "tools": ["OpenSearch", "DynamoDB", "CloudFront", "Lambda"],
        "reasoning": "Full-text search, metadata storage, edge caching for popular queries"
    },
    "auth": {
        "tools": ["Cognito", "DynamoDB", "ElastiCache", "Lambda", "CloudFront"],
        "reasoning": "Identity management, session storage, token caching, global availability"
    }
}

@app.get("/api/scenarios/{scenario_type}")
def get_scenario_suggestions(scenario_type: str, db: Session = Depends(get_db)):
    if scenario_type not in SCENARIO_MAPPINGS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario = SCENARIO_MAPPINGS[scenario_type]
    tool_names = scenario["tools"]
    
    tools = db.query(Tool).filter(Tool.name.in_(tool_names)).all()
    
    favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
    
    results = []
    for tool in tools:
        tool_dict = ToolResponse.from_orm(tool).dict()
        tool_dict["is_favorited"] = tool.id in favorite_tool_ids
        results.append(tool_dict)
    
    return {
        "scenario": scenario_type,
        "reasoning": scenario["reasoning"],
        "tools": results
    }

@app.get("/api/favorites", response_model=List[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db)):
    favorites = db.query(Favorite).order_by(Favorite.pinned_order).all()
    return favorites

@app.post("/api/favorites/{tool_id}")
def add_favorite(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    existing = db.query(Favorite).filter(Favorite.tool_id == tool_id).first()
    if existing:
        return {"message": "Already favorited", "favorite_id": existing.id}
    
    max_order = db.query(Favorite).count()
    favorite = Favorite(tool_id=tool_id, pinned_order=max_order + 1)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return {"message": "Favorited", "favorite_id": favorite.id}

@app.delete("/api/favorites/{tool_id}")
def remove_favorite(tool_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.tool_id == tool_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Unfavorited"}

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Tool.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
