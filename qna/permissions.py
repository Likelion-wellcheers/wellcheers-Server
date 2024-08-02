from rest_framework import permissions

class IsWriterOrReadOnly(permissions.BasePermission):
    # 작성자이면 모든 기능 허용, 작성자가 아니라면 읽기만 가능

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 수정 기능은 인증된 사용자만 가능
        return request.user.is_authenticated # 인증된 사용자인지 여부 검증
    
    def has_object_permission(self, request, view, obj):	
        if request.method in permissions.SAFE_METHODS:
            return True

        # 수정 기능은 작성자만 허용
        return obj.q_user_id == request.user