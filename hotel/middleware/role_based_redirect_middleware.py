# role_based_redirect_middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class RoleBasedRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to redirect users based on roles, 
    excluding specific public views that don't require login.
    """

    # Define roles and their respective dashboard URLs
    DASHBOARD_REDIRECTS = {
        'is_pos_officer': 'dashboard:pos_user_dashboard',
        'is_supervisor': 'dashboard:supervisor_dashboard',
        'is_account_officer': 'dashboard:account_dashboard',
        'is_admin': 'dashboard:admin_dashboard',
        'is_frontdesk_officer': 'dashboard:frontdesk_dashboard',

        # Add more roles and dashboards here as needed
    }

    # Views that don't require login
    PUBLIC_VIEWS = [
        'signin',
        'signup',
        'core:index',        # Add names of public views here
        'core:about',
        'core:contact',
        'core:gallery',
        'core:gallery-filter',
        'core:all_rooms',
        'core:room_type_list',
        'core:room_type_detail',
        'core:selected_rooms',
       
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Get the current view name
        view_name = resolve(request.path_info).view_name

        # Skip checks if the view is public or the user is not authenticated
        if view_name in self.PUBLIC_VIEWS or not request.user.is_authenticated:
            return None

        # Access the view's role requirements if they exist
        required_roles = getattr(view_func, 'required_roles', [])
    
        # Check if the user has any of the required roles
        if required_roles and not any(getattr(request.user, role, False) for role in required_roles):
            # Redirect to the user's own dashboard based on their role
            for role, dashboard_url in self.DASHBOARD_REDIRECTS.items():
                if getattr(request.user, role, False):
                    return redirect(reverse(dashboard_url))
            print("No matching role found, redirecting to signin.")
            return redirect(reverse('signin'))  # Fallback URL if no matching role
        return None
