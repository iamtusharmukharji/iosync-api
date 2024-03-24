from fastapi import APIRouter
import schemas

router = APIRouter(prefix='/automation',tags=["Automation"])

@router.post('/')
def automate(payload:schemas.Automate):
    """
    **This endpoint can be used to automate any mqtt message publish based on input source**


    Email is an optional parameter if used a notification will be sent on the mail
    """
    return {"detail":"sucess", "payload":payload}