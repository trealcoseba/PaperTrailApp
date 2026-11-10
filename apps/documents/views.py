import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DocumentRequest, DocumentStageLog
from apps.workflows.models import WorkflowTemplate, WorkflowTemplateStep
from apps.offices.models import Office

def ensure_default_workflow_steps(template):
    """Guarantees that a template always has all 5 required sequential stages."""
    Office.objects.filter(code="DEAN_ENG").update(code="DEAN")

    if template.steps.count() < 5:
        # 1. Create or get standard campus offices
        off_chair, _ = Office.objects.get_or_create(code="DEPT_CHAIR", defaults={"name": "Department Chair Office", "building_location": "CS Bldg Rm 201"})
        off_dean, _ = Office.objects.get_or_create(code="DEAN", defaults={"name": "Dean's Office", "building_location": "NGE"})
        off_reg, _ = Office.objects.get_or_create(code="REGISTRAR", defaults={"name": "University Registrar", "building_location": "RTL"})
        off_cashier, _ = Office.objects.get_or_create(code="CASHIER", defaults={"name": "Accounting & Cashier", "building_location": "RTL"})
        off_vpaa, _ = Office.objects.get_or_create(code="VPAA", defaults={"name": "Office of Academic Affairs", "building_location": "Admin Bldg Rm 401"})

        # 2. Attach the 5 sequential steps to the template
        WorkflowTemplateStep.objects.get_or_create(template=template, step_order=1, defaults={"office": off_chair, "required_action": "Initial Evaluation & Endorsement", "expected_duration_days": 1})
        WorkflowTemplateStep.objects.get_or_create(template=template, step_order=2, defaults={"office": off_dean, "required_action": "Dean Review & Signature", "expected_duration_days": 1})
        WorkflowTemplateStep.objects.get_or_create(template=template, step_order=3, defaults={"office": off_reg, "required_action": "Scholastic Record Verification", "expected_duration_days": 2})
        WorkflowTemplateStep.objects.get_or_create(template=template, step_order=4, defaults={"office": off_cashier, "required_action": "Student Account Clearance", "expected_duration_days": 1})
        WorkflowTemplateStep.objects.get_or_create(template=template, step_order=5, defaults={"office": off_vpaa, "required_action": "Final Approval & Document Release", "expected_duration_days": 1})


@login_required
def create_document_view(request):
    template = WorkflowTemplate.objects.first()
    if not template:
        template = WorkflowTemplate.objects.create(
            title="University Academic Clearance & Endorsement",
            description="5-stage sequential processing workflow across academic and administrative offices.",
            estimated_total_days=5
        )
    ensure_default_workflow_steps(template)

    templates = WorkflowTemplate.objects.filter(is_active=True)

    if request.method == "POST":
        template_id = request.POST.get("template_id")
        title = request.POST.get("document_title")
        purpose = request.POST.get("purpose")
        selected_template = get_object_or_404(WorkflowTemplate, id=template_id)
        ensure_default_workflow_steps(selected_template)

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

        first_step = selected_template.steps.first()
        if first_step:
            DocumentStageLog.objects.create(
                document=doc,
                step_order=1,
                office=first_step.office,
                actor=None,
                action_taken="Submitted for Review",
                remarks="Document received into department chair queue.",
                entered_at=timezone.now()
            )

        return redirect("documents:track", tracking_number=doc.tracking_number)

    return render(request, "documents/create_request.html", {"templates": templates})


@login_required
def tracker_view(request, tracking_number):
    document = get_object_or_404(DocumentRequest, tracking_number=tracking_number)
    
    # Ensure steps exist for this document's template
    ensure_default_workflow_steps(document.template)

    steps = document.template.steps.all().order_by("step_order")
    
    # If no initial log exists, create Step 1 log automatically
    if document.stage_logs.count() == 0 and steps.exists():
        DocumentStageLog.objects.create(
            document=document,
            step_order=1,
            office=steps.first().office,
            actor=None,
            action_taken="Submitted for Review",
            remarks="Document received into department chair queue.",
            entered_at=timezone.now()
        )

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