# decorators.py
def required_roles(*roles):
    def decorator(view_func):
        view_func.required_roles = roles
        print(f"Assigned required roles {roles} to {view_func.__name__}")
        return view_func
    return decorator
