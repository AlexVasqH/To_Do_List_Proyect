from pydantic import BaseModel
class task_model(BaseModel):
    title : str
    body : str

    
    
    def __repr__(self) -> str:
        return(f" el ID es {self.id} y el mensaje es {self.title} {self.body}")
    
