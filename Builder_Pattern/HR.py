from dataclasses import dataclass
from typing import Optional


# 1. The Product

@dataclass
class Employee:
    """A clean data container representing the final employee record."""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    department: str = ""
    position: str = ""
    salary: float = 0.0
    start_date: str = ""
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"



# 2. The Builder

class EmployeeBuilder:
    """Fluent Builder for constructing an Employee step-by-step."""
    
    def __init__(self):
        self.employee = Employee()

    def with_name(self, first_name: str, last_name: str) -> 'EmployeeBuilder':
        self.employee.first_name = first_name
        self.employee.last_name = last_name
        return self

    def with_email(self, email: str) -> 'EmployeeBuilder':
        self.employee.email = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> 'EmployeeBuilder':
        self.employee.department = department
        self.employee.position = position
        self.employee.salary = salary
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> 'EmployeeBuilder':
        self.employee.has_laptop = laptop
        self.employee.has_parking = parking
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> 'EmployeeBuilder':
        self.employee.has_vpn_access = vpn
        self.employee.has_admin_rights = admin
        return self
        
    def with_details(self, start_date: str, contract_type: str = "permanent") -> 'EmployeeBuilder':
        self.employee.start_date = start_date
        self.employee.contract_type = contract_type
        return self

    def build(self) -> Employee:
        """Validates the data and returns the final Employee object."""
        # Validation is now cleanly centralized at the end of the building process
        if not self.employee.first_name or not self.employee.last_name:
            raise ValueError("Name is required")
        if not self.employee.email or "@" not in self.employee.email:
            raise ValueError("Valid email is required")
        if self.employee.salary < 0:
            raise ValueError("Salary cannot be negative")
            
        return self.employee



# 3. Presets (Director / Specialized Builders)

class DeveloperBuilder(EmployeeBuilder):
    """A specialized builder that pre-fills standard Developer settings."""
    
    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        # Pre-fill the specific details requested during initialization
        self.with_name(first_name, last_name)
        self.with_email(email)
        # Pre-fill company defaults for developers
        self.with_job("Engineering", "Developer", 0.0) # Default salary to be overridden
        self.with_equipment(laptop=True, parking=False)
        self.with_access(vpn=True, admin=True)



# 4. Usage

if __name__ == "__main__":
    
    # 1. Fluent, readable creation (Custom Employee)
    try:
        custom_employee = (
            EmployeeBuilder()
            .with_name("John", "Doe")
            .with_email("john.doe@company.com")
            .with_job("Engineering", "Senior Developer", 75000)
            .with_equipment(laptop=True, parking=False)
            .with_access(vpn=True, admin=True)
            .build()
        )
        print("--- Custom Employee ---")
        print(custom_employee)
        
    except ValueError as e:
        print(f"Validation Error: {e}")

    print("\n")

    # 2. Using a preset builder (Standard Developer)
    try:
        dev = (
            DeveloperBuilder("Alice", "Smith", "alice.smith@company.com")
            .with_job("Engineering", "Backend Developer", 85000) # Override default salary/title
            .build()
        )
        print("--- Preset Developer ---")
        print(dev)
        
    except ValueError as e:
        print(f"Validation Error: {e}")