import os
import sys
import importlib
import inspect
from sqlalchemy.orm import class_mapper, RelationshipProperty

# --- Path Setup ---
# This allows the script to be run from the root directory (e.g., `python backend/relationship_audit.py`)
# and still correctly import modules from the `app` package.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# --- End Path Setup ---

from backend.app.database import Base

def find_and_import_models():
    """
    Dynamically finds and imports all modules in the 'backend/app/models' directory
    to ensure SQLAlchemy's declarative base registers them.
    """
    models_dir = os.path.join(project_root, 'backend', 'app', 'models')
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"backend.app.models.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
                # print(f"Successfully imported {module_name}")
            except Exception as e:
                print(f"Failed to import {module_name}: {e}")

def audit_relationships():
    """
    Audits all registered SQLAlchemy models for relationship integrity.
    Checks if each `relationship` has a corresponding `back_populates` on the target model.
    """
    print("--- Starting SQLAlchemy Relationship Audit ---")
    
    # Import all models to ensure they are registered with the Base
    find_and_import_models()

    errors_found = []
    
    # Get all classes mapped by SQLAlchemy
    all_mappers = list(Base.registry.mappers)
    
    if not all_mappers:
        print("Error: No SQLAlchemy models found. Ensure models inherit from Base and are imported.")
        return

    print(f"Found {len(all_mappers)} models to audit...")

    for mapper in all_mappers:
        model_class = mapper.class_
        model_name = model_class.__name__
        # print(f"\nAuditing Model: {model_name}")

        for prop in mapper.iterate_properties:
            if isinstance(prop, RelationshipProperty):
                relationship_name = prop.key
                back_populates_name = prop.back_populates

                if not back_populates_name:
                    # This relationship does not have a back_populates argument.
                    # This is not always an error, but worth noting.
                    # For our case, we enforce it.
                    error_msg = (
                        f"-[INCOMPLETE] In Model '{model_name}', Relationship '{relationship_name}' "
                        f"is missing the 'back_populates' argument. This is required for our project."
                    )
                    errors_found.append(error_msg)
                    continue

                # Find the target model class
                target_model_class = prop.mapper.class_
                target_model_name = target_model_class.__name__

                # Check if the back-populating relationship exists on the target model
                if not hasattr(target_model_class, back_populates_name):
                    error_msg = (
                        f"-[MISMATCH] In Model '{model_name}', Relationship '{relationship_name}' "
                        f"points to '{target_model_name}.{back_populates_name}', but that relationship does NOT exist."
                    )
                    errors_found.append(error_msg)
                    continue

                # Get the relationship object from the target model
                target_prop = getattr(target_model_class, back_populates_name).property
                
                if not isinstance(target_prop, RelationshipProperty):
                    error_msg = (
                        f"-[WRONG_TYPE] In Model '{target_model_name}', the attribute '{back_populates_name}' is not a relationship, "
                        f"but '{model_name}.{relationship_name}' tries to back-populate to it."
                    )
                    errors_found.append(error_msg)
                    continue

                # Check if the target's back_populates points back to the original relationship
                if target_prop.back_populates != relationship_name:
                    error_msg = (
                        f"-[MISMATCH] In Model '{model_name}', Relationship '{relationship_name}' uses back_populates='{back_populates_name}'. "
                        f"However, '{target_model_name}.{back_populates_name}' points back to '{target_prop.back_populates}', "
                        f"NOT '{relationship_name}'."
                    )
                    errors_found.append(error_msg)

    print("\n--- Audit Complete ---")
    if errors_found:
        print(f"\nFound {len(errors_found)} relationship errors:\n")
        for error in sorted(errors_found):
            print(error)
    else:
        print("\nSuccess! All model relationships are correctly configured.")
        
if __name__ == "__main__":
    audit_relationships()