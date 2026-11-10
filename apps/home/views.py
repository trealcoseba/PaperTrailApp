from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from apps.documents.models import DocumentRequest

@login_required
def home_view(request):
    # Fetch student's real document requests from Supabase
    user_documents = DocumentRequest.objects.filter(student=request.user).order_by("-submitted_at")
    total_docs = user_documents.count()
    active_docs = user_documents.exclude(status="Released").count()

    return render(request, "home/home.html", {
        "documents": user_documents,
        "total_docs": total_docs,
        "active_docs": active_docs,
    })

def logout_view(request):
    logout(request)
    return redirect("login:login")