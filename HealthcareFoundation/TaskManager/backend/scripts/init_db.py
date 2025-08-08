from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import Base, Task, Client, TaskAttachment
from datetime import date, time, datetime


def init_db() -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample clients
        if not db.query(Client).first():
            client1 = Client(
                name="John Doe",
                email="john@example.com",
                phone="(555) 123-4567",
                company="Acme Corp",
                notes="Primary contact for Acme Corp projects"
            )
            client2 = Client(
                name="Jane Smith",
                email="jane@example.com",
                phone="(555) 987-6543",
                company="Tech Solutions",
                notes="Lead developer at Tech Solutions"
            )
            client3 = Client(
                name="Bob Johnson",
                email="bob@startup.com",
                phone="(555) 456-7890",
                company="Startup Inc",
                notes="CEO of fast-growing startup"
            )
            
            db.add_all([client1, client2, client3])
            db.commit()
            db.refresh(client1)
            db.refresh(client2)
            db.refresh(client3)
        
        # Create sample tasks
        if not db.query(Task).first():
            tasks = [
                Task(
                    name="Complete project proposal",
                    description="Draft and finalize the Q4 project proposal for the new client engagement",
                    due_date=date(2024, 12, 25),
                    due_time=time(14, 0),
                    priority="high",
                    status="todo",
                    client_id=client1.id
                ),
                Task(
                    name="Review client feedback",
                    description="Go through all client feedback from the demo and prepare detailed response",
                    due_date=date(2024, 12, 24),
                    due_time=time(10, 0),
                    priority="medium",
                    status="in_progress",
                    client_id=client2.id
                ),
                Task(
                    name="Update documentation",
                    description="Update API documentation with new endpoints and examples",
                    due_date=date(2024, 12, 30),
                    priority="low",
                    status="todo",
                    client_id=client3.id
                ),
                Task(
                    name="Team meeting preparation",
                    description="Prepare agenda and materials for weekly team meeting",
                    due_date=date(2024, 12, 23),
                    due_time=time(9, 0),
                    priority="medium",
                    status="completed"
                ),
                Task(
                    name="Code review",
                    description="Review pull requests from team members",
                    priority="high",
                    status="todo"
                )
            ]
            
            db.add_all(tasks)
            db.commit()
        
        print("✅ Database initialized with sample data!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

