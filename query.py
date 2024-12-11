from sqlalchemy.orm import sessionmaker
from database import engine
from models.company_user import CompanyUser  # Certifique-se de substituir 'your_model_file' pelo nome do arquivo onde a classe CompanyUser está definida
from models.ornamental_block import OrnamentalBlock
Session = sessionmaker(bind=engine)
session = Session()

email = "adm@123"
# Query para buscar todos os registros da classe CompanyUser
company_users = session.query(OrnamentalBlock).all()

user = session.query(CompanyUser).filter(CompanyUser.email == email).first()

# Exibindo os resultados
for u in company_users:
    print(u.to_dict())
    
print(user.email)