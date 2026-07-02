from sqlalchemy import String, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import Optional, List

class Thesis(Base):
    __tablename__ = "thesis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assignment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("thesis_supervision.id"))
    filename: Mapped[str] = mapped_column(String(255))
    file_hash: Mapped[str] = mapped_column(String(255), index=True)
    source_path: Mapped[str] = mapped_column(String(255))
    spec_code: Mapped[str] = mapped_column(String(10))
    text_path: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255), index=True)
    error_text: Mapped[str] = mapped_column(String(512))
    current_step: Mapped[int] = mapped_column(Integer)
    last_completed_step: Mapped[int] = mapped_column(Integer)
    failed_step: Mapped[int] = mapped_column(Integer) 
    
    metadata_info: Mapped[Optional["ThesisMetadata"]] = relationship(back_populates="thesis", uselist=False)
    keywords: Mapped[List["KeywordCandidates"]] = relationship(back_populates="thesis")
    final_direction: Mapped[Optional["ThesisDirection"]] = relationship(back_populates="thesis", uselist=False)
    steps: Mapped[List["ThesisSteps"]] = relationship(back_populates="thesis")
    supervision: Mapped[Optional["ThesisSupervision"]] = relationship(back_populates="thesis")

class ThesisMetadata(Base):
    __tablename__ = "thesis_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thesis_id: Mapped[int] = mapped_column(ForeignKey("thesis.id"))
    main_theme: Mapped[str] = mapped_column(String(255))
    subject_area: Mapped[str] = mapped_column(String(255))
    purpose: Mapped[str] = mapped_column(String(255))
    relevance: Mapped[str] = mapped_column(String(255))
    object_of_research: Mapped[str] = mapped_column(String(255))
    tools_and_methods: Mapped[str] = mapped_column(String(255))
    main_tasks: Mapped[str] = mapped_column(String(255))
    main_chapters: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    
    thesis: Mapped["Thesis"] = relationship(back_populates="metadata_info")

class KeywordCandidates(Base):
    __tablename__ = "thesis_keyword_candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thesis_id: Mapped[int] = mapped_column(ForeignKey("thesis.id"))
    keyword_candidate: Mapped[str] = mapped_column(String(255))
    similarity: Mapped[float] = mapped_column(Float)

    thesis: Mapped["Thesis"] = relationship(back_populates="keywords")

class ThesisDirection(Base):
    __tablename__ = "thesis_direction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thesis_id: Mapped[int] = mapped_column(ForeignKey("thesis.id"))
    reasoning: Mapped[str] = mapped_column(Text)
    direction: Mapped[str] = mapped_column(String(140))
    score: Mapped[float] = mapped_column(Float)

    thesis: Mapped["Thesis"] = relationship(back_populates="final_direction")

class ThesisSteps(Base):
    __tablename__ = "thesis_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thesis_id: Mapped[int] = mapped_column(ForeignKey("thesis.id"))
    step_number: Mapped[int] = mapped_column(Integer)
    step_name: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(25))
    error_text: Mapped[Optional[str]] = mapped_column(Text)

    thesis: Mapped["Thesis"] = relationship(back_populates="steps")

class ThesisSupervision(Base):
    __tablename__ = "thesis_supervision"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scientific_supervisor: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    student: Mapped[str] = mapped_column(String(100))
    topic: Mapped[str] = mapped_column(String(400))
    spec_code: Mapped[str] = mapped_column(String(10))
    specialization: Mapped[Optional[str]] = mapped_column(String(100))
    faculty: Mapped[Optional[str]] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)

    thesis: Mapped[Optional["Thesis"]] = relationship(
        back_populates="supervision", 
        uselist=False
    )