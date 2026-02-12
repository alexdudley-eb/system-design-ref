from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    cap_leaning = Column(String, index=True)
    consistency_model = Column(String, index=True)
    interview_oneliner = Column(Text)
    best_for = Column(Text)
    avoid_when = Column(Text)
    tradeoffs = Column(Text)
    scaling_pattern = Column(Text)
    official_docs_url = Column(String)
    deep_dive_url_1 = Column(String)
    deep_dive_url_2 = Column(String)
    aws_only = Column(Integer, default=1)
    
    deep_study = relationship("ToolDeep", back_populates="tool", uselist=False)
    favorites = relationship("Favorite", back_populates="tool")

class ToolDeep(Base):
    __tablename__ = "tools_deep"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), unique=True, nullable=False)
    failure_modes = Column(Text)
    multi_region_notes = Column(Text)
    tuning_gotchas = Column(Text)
    observability_signals = Column(Text)
    alternatives = Column(Text)
    interview_prompts = Column(Text)
    
    tool = relationship("Tool", back_populates="deep_study")

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    pinned_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tool = relationship("Tool", back_populates="favorites")
