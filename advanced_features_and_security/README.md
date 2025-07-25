# Permission System Setup
## Custom Permissions:

Added to the Book model: can_view_book, can_create_book, can_edit_book, can_delete_book

Added to the CustomUser model: can_view_dashboard

Groups:

Admins: Have all permissions (automatically through is_staff=True)

Editors: Can view, create, and edit books (assigned to Librarians)

Viewers: Can only view books (assigned to Members)

Role-Based Access Control:

When a UserProfile is saved, it automatically updates the user's groups based on their role

The update_user_groups method handles group assignment and permission management