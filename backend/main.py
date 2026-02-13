from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from database import get_db, init_db
from models import Tool, ToolDeep, Favorite
from scenario_data import SCENARIO_BLUEPRINTS
from reference_data import NUMBERS_TO_KNOW, DELIVERY_FRAMEWORK, ASSESSMENT_RUBRIC, COMMON_PATTERNS
from quiz_data import TECHNOLOGY_QUIZ_QUESTIONS
from flashcard_questions import CONCEPT_QUESTIONS, PATTERN_QUESTIONS, NUMBERS_QUESTIONS, ALL_FLASHCARD_QUESTIONS
import random

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

@app.get("/api/scenarios/{scenario_type}")
def get_scenario_suggestions(scenario_type: str, db: Session = Depends(get_db)):
    if scenario_type not in SCENARIO_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    blueprint = SCENARIO_BLUEPRINTS[scenario_type]
    tool_names = blueprint["tools"]
    
    tools = db.query(Tool).filter(Tool.name.in_(tool_names)).all()
    
    favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
    
    tool_results = []
    for tool in tools:
        tool_dict = ToolResponse.from_orm(tool).dict()
        tool_dict["is_favorited"] = tool.id in favorite_tool_ids
        tool_results.append(tool_dict)
    
    return {
        "scenario": scenario_type,
        "title": blueprint["title"],
        "description": blueprint["description"],
        "requirements": blueprint["requirements"],
        "core_entities": blueprint["core_entities"],
        "api": blueprint["api"],
        "high_level": blueprint["high_level"],
        "deep_dive": blueprint["deep_dive"],
        "reasoning": blueprint["reasoning"],
        "tools": tool_results,
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

@app.get("/api/reference/numbers")
def get_numbers_to_know():
    """Get system design numbers and metrics to memorize"""
    return NUMBERS_TO_KNOW

@app.get("/api/reference/framework")
def get_delivery_framework():
    """Get the structured interview delivery framework"""
    return DELIVERY_FRAMEWORK

@app.get("/api/reference/rubric")
def get_assessment_rubric():
    """Get the interviewer assessment rubric"""
    return ASSESSMENT_RUBRIC

@app.get("/api/reference/patterns")
def get_common_patterns():
    """Get common system design patterns"""
    return COMMON_PATTERNS

@app.get("/api/reference/patterns/{pattern_name}")
def get_pattern_detail(pattern_name: str):
    """Get details for a specific pattern"""
    pattern = COMMON_PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return pattern

@app.get("/api/quiz/question")
def get_random_quiz_question(
    question_type: Optional[str] = Query(None, regex="^(scenario|technology)$"),
    db: Session = Depends(get_db)
):
    """
    Get a random quiz question.
    question_type: 'scenario', 'technology', or None (random choice)
    """
    if question_type is None:
        question_type = random.choices(["scenario", "technology"], weights=[0.7, 0.3])[0]
    
    if question_type == "scenario":
        scenario_types = list(SCENARIO_BLUEPRINTS.keys())
        selected_scenario = random.choice(scenario_types)
        blueprint = SCENARIO_BLUEPRINTS[selected_scenario]
        tool_names = blueprint["tools"]
        tools = db.query(Tool).filter(Tool.name.in_(tool_names)).all()
        
        favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
        
        tool_results = []
        for tool in tools:
            tool_dict = ToolResponse.from_orm(tool).dict()
            tool_dict["is_favorited"] = tool.id in favorite_tool_ids
            tool_results.append(tool_dict)
        
        return {
            "id": f"scenario-{selected_scenario}",
            "type": "scenario",
            "question": f"Design a {blueprint['title']}",
            "scenario": {
                "scenario": selected_scenario,
                "title": blueprint["title"],
                "description": blueprint["description"],
                "requirements": blueprint["requirements"],
                "core_entities": blueprint["core_entities"],
                "api": blueprint["api"],
                "high_level": blueprint["high_level"],
                "deep_dive": blueprint["deep_dive"],
                "reasoning": blueprint["reasoning"],
                "tools": tool_results,
            }
        }
    else:
        tech_question = random.choice(TECHNOLOGY_QUIZ_QUESTIONS)
        return {
            "id": tech_question["id"],
            "type": "technology",
            "category": tech_question["category"],
            "question": tech_question["question"],
            "options": tech_question["options"],
            "correct_answer": tech_question["correct_answer"],
            "explanation": tech_question["explanation"],
            "key_considerations": tech_question["key_considerations"],
            "limitations": tech_question["limitations"]
        }

@app.get("/api/quiz/questions")
def get_quiz_questions(
    count: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get multiple quiz questions for a quiz session.
    count: number of questions (1-10), default 5
    Returns a mix of 70% scenario questions and 30% technology questions
    """
    questions = []
    used_scenarios = set()
    used_tech_questions = set()
    
    scenario_count = max(1, int(count * 0.7))
    tech_count = count - scenario_count
    
    scenario_types = list(SCENARIO_BLUEPRINTS.keys())
    
    for i in range(scenario_count):
        available_scenarios = [s for s in scenario_types if s not in used_scenarios]
        if not available_scenarios:
            used_scenarios.clear()
            available_scenarios = scenario_types
        
        selected_scenario = random.choice(available_scenarios)
        used_scenarios.add(selected_scenario)
        
        blueprint = SCENARIO_BLUEPRINTS[selected_scenario]
        tool_names = blueprint["tools"]
        tools = db.query(Tool).filter(Tool.name.in_(tool_names)).all()
        
        favorite_tool_ids = {f.tool_id for f in db.query(Favorite.tool_id).all()}
        
        tool_results = []
        for tool in tools:
            tool_dict = ToolResponse.from_orm(tool).dict()
            tool_dict["is_favorited"] = tool.id in favorite_tool_ids
            tool_results.append(tool_dict)
        
        questions.append({
            "id": f"scenario-{selected_scenario}",
            "type": "scenario",
            "question": f"Design a {blueprint['title']}",
            "scenario": {
                "scenario": selected_scenario,
                "title": blueprint["title"],
                "description": blueprint["description"],
                "requirements": blueprint["requirements"],
                "core_entities": blueprint["core_entities"],
                "api": blueprint["api"],
                "high_level": blueprint["high_level"],
                "deep_dive": blueprint["deep_dive"],
                "reasoning": blueprint["reasoning"],
                "tools": tool_results,
            }
        })
    
    for i in range(tech_count):
        available_tech = [q for q in TECHNOLOGY_QUIZ_QUESTIONS if q["id"] not in used_tech_questions]
        if not available_tech:
            used_tech_questions.clear()
            available_tech = TECHNOLOGY_QUIZ_QUESTIONS
        
        tech_question = random.choice(available_tech)
        used_tech_questions.add(tech_question["id"])
        
        questions.append({
            "id": tech_question["id"],
            "type": "technology",
            "category": tech_question["category"],
            "question": tech_question["question"],
            "options": tech_question["options"],
            "correct_answer": tech_question["correct_answer"],
            "explanation": tech_question["explanation"],
            "key_considerations": tech_question["key_considerations"],
            "limitations": tech_question["limitations"]
        })
    
    random.shuffle(questions)
    
    return {"questions": questions, "total": len(questions)}

@app.get("/api/flashcard/question")
def get_random_flashcard(
    category: Optional[str] = Query(None, regex="^(technology|concept|pattern|numbers)$")
):
    """
    Get a random flashcard question.
    category: 'technology', 'concept', 'pattern', 'numbers', or None (weighted random choice)
    Weights: 40% technology (reusing from quiz_data), 30% concepts, 20% patterns, 10% numbers
    """
    if category is None:
        category = random.choices(
            ["technology", "concept", "pattern", "numbers"],
            weights=[0.4, 0.3, 0.2, 0.1]
        )[0]
    
    if category == "technology":
        tech_question = random.choice(TECHNOLOGY_QUIZ_QUESTIONS)
        return {
            "id": tech_question["id"],
            "category": tech_question["category"],
            "question": tech_question["question"],
            "answer": tech_question.get("options", [{}])[ord(tech_question["correct_answer"]) - ord('a')].get("text", tech_question["correct_answer"]) if tech_question.get("options") else tech_question["correct_answer"],
            "key_points": tech_question.get("key_considerations", []),
            "explanation": tech_question.get("explanation", ""),
            "options": tech_question.get("options", []),
            "correct_answer": tech_question.get("correct_answer", "")
        }
    elif category == "concept":
        question = random.choice(CONCEPT_QUESTIONS)
        return question
    elif category == "pattern":
        question = random.choice(PATTERN_QUESTIONS)
        return question
    else:
        question = random.choice(NUMBERS_QUESTIONS)
        return question

@app.get("/api/flashcard/questions")
def get_flashcard_set(
    count: int = Query(10, ge=5, le=20),
    category: Optional[str] = Query(None, regex="^(all|technology|concept|pattern|numbers)$")
):
    """
    Get multiple flashcard questions for a quiz session.
    count: number of questions (5-20), default 10
    category: filter by category or 'all' for mixed set
    Returns a mixed set with no duplicates
    """
    if category == "technology":
        available_questions = [
            {
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "answer": q.get("options", [{}])[ord(q["correct_answer"]) - ord('a')].get("text", q["correct_answer"]) if q.get("options") else q["correct_answer"],
                "key_points": q.get("key_considerations", []),
                "explanation": q.get("explanation", ""),
                "options": q.get("options", []),
                "correct_answer": q.get("correct_answer", "")
            }
            for q in TECHNOLOGY_QUIZ_QUESTIONS
        ]
    elif category == "concept":
        available_questions = CONCEPT_QUESTIONS.copy()
    elif category == "pattern":
        available_questions = PATTERN_QUESTIONS.copy()
    elif category == "numbers":
        available_questions = NUMBERS_QUESTIONS.copy()
    else:
        tech_questions = [
            {
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "answer": q.get("options", [{}])[ord(q["correct_answer"]) - ord('a')].get("text", q["correct_answer"]) if q.get("options") else q["correct_answer"],
                "key_points": q.get("key_considerations", []),
                "explanation": q.get("explanation", ""),
                "options": q.get("options", []),
                "correct_answer": q.get("correct_answer", "")
            }
            for q in TECHNOLOGY_QUIZ_QUESTIONS
        ]
        available_questions = tech_questions + CONCEPT_QUESTIONS + PATTERN_QUESTIONS + NUMBERS_QUESTIONS
    
    if len(available_questions) < count:
        selected_questions = available_questions
    else:
        selected_questions = random.sample(available_questions, count)
    
    random.shuffle(selected_questions)
    
    return {"questions": selected_questions, "total": len(selected_questions)}

@app.get("/api/test/scenario")
def get_test_scenario(
    scenario_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get minimal scenario info for test mode.
    Returns only: title, description, scale, hints
    EXCLUDES: requirements details, entities, API, high_level, deep_dive, reasoning
    """
    if scenario_type is None:
        scenario_types = list(SCENARIO_BLUEPRINTS.keys())
        scenario_type = random.choice(scenario_types)
    
    if scenario_type not in SCENARIO_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    blueprint = SCENARIO_BLUEPRINTS[scenario_type]
    
    scale_info = {}
    if "DAU" in blueprint["description"] or "users" in blueprint["description"].lower():
        if "uber" in scenario_type.lower() or "lyft" in scenario_type.lower():
            scale_info = {
                "daily_active_users": "100M DAU",
                "requests_per_second": "Peak: 1M requests/second",
                "data_size": "100+ PB ride history"
            }
        elif "whatsapp" in scenario_type.lower() or "messenger" in scenario_type.lower():
            scale_info = {
                "daily_active_users": "2B DAU",
                "messages_per_day": "100B messages/day",
                "data_size": "Multiple PB of messages"
            }
        elif "instagram" in scenario_type.lower() or "twitter" in scenario_type.lower():
            scale_info = {
                "daily_active_users": "500M+ DAU",
                "posts_per_day": "100M+ posts/day",
                "data_size": "Multiple PB of media"
            }
    
    hints = {
        "out_of_scope": blueprint["requirements"].get("out_of_scope", []),
        "key_constraints": []
    }
    
    if blueprint["requirements"].get("non_functional", []):
        for req in blueprint["requirements"]["non_functional"]:
            if "latency" in req.lower() or "consistency" in req.lower() or "availability" in req.lower():
                hints["key_constraints"].append(req)
    
    return {
        "scenario": scenario_type,
        "title": blueprint["title"],
        "description": blueprint["description"],
        "scale": scale_info,
        "hints": hints
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
