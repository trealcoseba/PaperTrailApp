import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DocumentRequest, DocumentStageLog
from apps.workflows.models import WorkflowTemplate, WorkflowTemplateStep
from apps.offices.models import Office

@login_required
def create_document_view(request):
    # Ensure default workflow template and offices exist for demo testing
    template = WorkflowTemplate.objects.first()
    if not template:
        # Seed default offices
        off_chair, _ = Office.objects.get_or_create(code="DEPT_CHAIR", name="Department Chair Office", building_location="CS Building Rm 201")
        off_dean, _ = Office.objects.get_or_create(code="DEAN_ENG", name="Dean of Engineering & Tech", building_location="Main Wing Rm 302")
        off_reg, _ = Office.objects.get_or_create(code="REGISTRAR", name="University Registrar", building_location="Admin Bldg Rm 101")
        off_vpaa, _ = Office.objects.get_or_create(code="VPAA", name="Office of Academic Affairs", building_location="Admin Bldg Rm 401")
        off_cashier, _ = Office.objects.get_or_create(code="CASHIER", name="Student Accounting & Cashier", building_location="Finance Bldg Rm 105")

        # Seed 5-stage default workflow
        template = WorkflowTemplate.objects.create(
            title="University Academic Clearance & Endorsement",
            description="5-stage sequential processing workflow across academic and administrative offices.",
            estimated_total_days=5
        )
        WorkflowTemplateStep.objects.create(template=template, step_order=1, office=off_chair, required_action="Endorsement & Evaluation", expected_duration_days=1)
        WorkflowTemplateStep.objects.create(template=template, step_order=2, office=off_dean, required_action="Dean Review & Signature", expected_duration_days=1)
        WorkflowTemplateStep.objects.create(template=template, step_order=3, office=off_reg, required_action="Record Verification", expected_duration_days=1)
        WorkflowTemplateStep.objects.create(template=template, step_order=4, office=off_cashier, required_action="Clearance Assessment", expected_duration_days=1)
        WorkflowTemplateStep.objects.create(template=template, step_order=5, office=off_vpaa, required_action="Final Approval & Release", expected_duration_days=1)

    templates = WorkflowTemplate.objects.filter(is_active=True)

    if request.method == "POST":
        template_id = request.POST.get("template_id")
        title = request.POST.get("document_title")
        purpose = request.POST.get("purpose")
        selected_template = get_object_or_404(WorkflowTemplate, id=template_id)

        # Generate unique tracking number (e.g., PT-2026-7842)
        tracking_num = f"PT-2026-{random.randint(1000, 9999)}"

        doc = DocumentRequest.objects.create(
            tracking_number=tracking_num,
            student=request.user,
            template=selected_template,
            document_title=title,
            purpose=purpose,
            current_step_order=1,
            status="Under Review"
        )

        # Create initial Stage Log for Step 1
        first_step = selected_template.steps.first()
        if first_step:
            DocumentStageLog.objects.create(
                document=doc,
                step_order=1,
                office=first_step.office,
                actor=None,
                action_taken="Submitted for Review",
                remarks="Document received into department queue.",
                entered_at=timezone.now()
            )

        return redirect("documents:track", tracking_number=doc.tracking_number)

    return render(request, "documents/create_request.html", {"templates": templates})


@login_required
def tracker_view(request, tracking_number):
    document = get_object_or_404(DocumentRequest, tracking_number=tracking_number)
    steps = document.template.steps.all().order_by("step_order")
    logs = document.stage_logs.all().order_by("-entered_at")
    
    current_step = steps.filter(step_order=document.current_step_order).first()
    next_step = steps.filter(step_order=document.current_step_order + 1).first()

    return render(request, "documents/tracker.html", {
        "document": document,
        "steps": steps,
        "logs": logs,
        "current_step": current_step,
        "next_step": next_step,
    })