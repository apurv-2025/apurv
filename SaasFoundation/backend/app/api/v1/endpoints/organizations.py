import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.models import User, OrganizationMember, Invitation
from app.schemas.organization import (
    OrganizationWithRole, OrganizationUpdate, OrganizationResponse,
    MemberResponse, MemberUpdate, InvitationCreate, InvitationResponse, InvitationDetailsResponse
)
from app.services.organization import organization_service
from app.utils.datetime_utils import utcnow
from app.services.email import email_service

router = APIRouter()

@router.get("/current", response_model=OrganizationWithRole)
async def get_current_organization(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get current user's organization"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    print(role)

    return OrganizationWithRole(
        organization=organization,
        current_user_role=role
    )

@router.put("/current", response_model=OrganizationResponse)
async def update_organization(
    org_data: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update organization (owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role != "owner":
        raise HTTPException(status_code=403, detail="Only organization owners can update organization details")
    
    if org_data.name:
        organization.name = org_data.name
    if org_data.description is not None:
        organization.description = org_data.description
    
    organization.updated_at = utcnow()
    db.commit()
    db.refresh(organization)
    
    return organization

@router.get("/current/members", response_model=List[MemberResponse])
async def get_organization_members(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get organization members"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    members = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization.id,
        OrganizationMember.status == "active"
    ).all()
    
    return members

@router.put("/current/members/{member_id}", response_model=MemberResponse)
async def update_member_role(
    member_id: str,
    member_data: MemberUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update member role (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    member = db.query(OrganizationMember).filter(
        OrganizationMember.id == member_id,
        OrganizationMember.organization_id == organization.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Prevent non-owners from changing owner role
    if member.role == "owner" and role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can change owner roles")
    
    # Prevent members from being promoted to owner by non-owners
    if member_data.role == "owner" and role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can promote to owner")
    
    member.role = member_data.role
    db.commit()
    db.refresh(member)
    
    return member

@router.delete("/current/members/{member_id}")
async def remove_member(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove member (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    member = db.query(OrganizationMember).filter(
        OrganizationMember.id == member_id,
        OrganizationMember.organization_id == organization.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Prevent removing owner
    if member.role == "owner":
        raise HTTPException(status_code=403, detail="Cannot remove organization owner")
    
    db.delete(member)
    db.commit()
    
    return {"message": "Member removed successfully"}

@router.post("/current/invite", response_model=InvitationResponse)
async def invite_user(
    invitation_data: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invite user to organization (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    

    # Check if user is already a member
    existing_member = db.query(OrganizationMember).join(
        User, OrganizationMember.user_id == User.id  # Explicitly specify the join condition
        ).filter(
            OrganizationMember.organization_id == organization.id,
            User.email == invitation_data.email,
            OrganizationMember.status == "active"
    ).first()  
    
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this organization")
    
    # Check if invitation already exists
    existing_invitation = db.query(Invitation).filter(
        Invitation.organization_id == organization.id,
        Invitation.email == invitation_data.email,
        Invitation.status == "pending"
    ).first()
    
    if existing_invitation:
        raise HTTPException(status_code=400, detail="Invitation already sent to this email")
    
    # Only owners can invite other owners
    if invitation_data.role == "owner" and role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can invite other owners")
    
    # Create invitation
    invitation_token = secrets.token_urlsafe(32)
    invitation = Invitation(
        organization_id=organization.id,
        email=invitation_data.email,
        role=invitation_data.role,
        invited_by=current_user.id,
        token=invitation_token,
        expires_at=utcnow() + timedelta(days=7),
        status="pending"
    )
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    # Send invitation email
    email_service.send_invitation_email(invitation, organization, current_user)
    
    invitationResponse = InvitationResponse(
        id=organization.id,
        email=invitation_data.email,
        role=invitation_data.role,
        invited_by=current_user.id,
        token=invitation_token,
        expires_at=utcnow() + timedelta(days=7),
        status="pending")

    return invitationResponse

@router.get("/current/invitations", response_model=List[InvitationResponse])
async def get_invitations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get pending invitations (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invitations = db.query(Invitation).filter(
        Invitation.organization_id == organization.id,
        Invitation.status == "pending"
    ).all()
    
    return invitations

@router.delete("/current/invitations/{invitation_id}")
async def cancel_invitation(
    invitation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel invitation (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invitation = db.query(Invitation).filter(
        Invitation.id == invitation_id,
        Invitation.organization_id == organization.id,
        Invitation.status == "pending"
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    db.delete(invitation)
    db.commit()
    
    return {"message": "Invitation cancelled"}

@router.post("/current/invitations/{invitation_id}/resend")
async def resend_invitation(
    invitation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resend invitation (admin/owner only)"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invitation = db.query(Invitation).filter(
        Invitation.id == invitation_id,
        Invitation.organization_id == organization.id,
        Invitation.status == "pending"
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Update expiration date
    invitation.expires_at = utcnow() + timedelta(days=7)
    db.commit()
    
    # Resend invitation email
    email_service.send_invitation_email(invitation, organization, current_user)
    
    return {"message": "Invitation resent successfully"}

# Invitation acceptance endpoints
@router.get("/invitations/{token}", response_model=InvitationDetailsResponse)
async def get_invitation_details(token: str, db: Session = Depends(get_db)):
    """Get invitation details by token"""
    invitation = db.query(Invitation).filter(
        Invitation.token == token,
        Invitation.status == "pending",
        Invitation.expires_at > utcnow()
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invalid or expired invitation")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == invitation.email).first()
    
    return InvitationDetailsResponse(
        id=invitation.id,
        email=invitation.email,
        role=invitation.role,
        status=invitation.status,
        organization=invitation.organization,
        invited_by=invitation.invited_by_user,
        expires_at=invitation.expires_at,
        created_at=invitation.created_at,
        user_exists=existing_user is not None
    )

@router.post("/invitations/{token}/accept")
async def accept_invitation(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept invitation"""
    invitation = db.query(Invitation).filter(
        Invitation.token == token,
        Invitation.status == "pending",
        Invitation.expires_at > utcnow()
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invalid or expired invitation")
    
    # Verify email matches
    if current_user.email != invitation.email:
        raise HTTPException(status_code=403, detail="Email address does not match invitation")
    
    # Check if user is already a member
    existing_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == invitation.organization_id,
        OrganizationMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="You are already a member of this organization")
    
    # Create organization membership
    member = OrganizationMember(
        organization_id=invitation.organization_id,
        user_id=current_user.id,
        role=invitation.role,
        status="active",
        invited_by=invitation.invited_by
    )
    
    db.add(member)
    
    # Mark invitation as accepted
    invitation.status = "accepted"
    invitation.accepted_at = utcnow()
    
    db.commit()
    
    return {"message": "Invitation accepted successfully"}
