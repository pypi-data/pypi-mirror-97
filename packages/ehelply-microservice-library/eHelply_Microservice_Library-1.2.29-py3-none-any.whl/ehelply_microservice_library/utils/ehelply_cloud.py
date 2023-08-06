from typing import Union, Optional

from pydantic import BaseModel

from fastapi import HTTPException

from ehelply_python_sdk.services.access.auth_rules import AuthRule
from ehelply_python_sdk.services.access.sdk import AuthModel


class CloudParticipant(BaseModel):
    active_participant: str
    project_uuid: str
    is_privileged: bool = False
    entity_identifier: Optional[str] = None


def ehelply_cloud_access(
        auth: AuthModel,
        node: str,
        service_target: str,
        exception_if_unauthorized=True
) -> Union[bool, CloudParticipant]:
    # Regular eHelply Cloud access
    try:
        AuthRule(
            auth,
            exception_if_unauthorized=True
        ).participant_has_node_on_target(
            node=node,
            target_identifier=auth.project_uuid,
            partition="ehelply-cloud"
        ).customentity_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-cloud",
            entity_identifier=auth.project_uuid
        ).verify()

        return CloudParticipant(
            is_privileged=False,
            active_participant=auth.active_participant_uuid,
            project_uuid=auth.project_uuid,
            entity_identifier=auth.entity_identifier
        )
    except:
        pass

    # Admin or M2M access
    try:
        AuthRule(
            auth,
            exception_if_unauthorized=True
        ).participant_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-resources"
        ).verify()

        return CloudParticipant(
            is_privileged=True,
            active_participant=auth.active_participant_uuid,
            project_uuid=auth.project_uuid,
            entity_identifier=auth.entity_identifier
        )
    except:
        pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized - Denied by eHelply")
    else:
        return False

    #
    # return AuthRule(
    #     auth,
    #     AuthRule(auth).participant_has_node_on_target(
    #         node=node,
    #         target_identifier=service_target,
    #         partition="ehelply-resources"
    #     ),
    #     AuthRule(auth).participant_has_node_on_target(
    #         node=node,
    #         target_identifier=auth.project_uuid,
    #         partition="ehelply-cloud"
    #     ).customentity_has_node_on_target(
    #         node=node,
    #         target_identifier=service_target,
    #         partition="ehelply-cloud",
    #         entity_identifier=auth.project_uuid
    #     ),
    #     exception_if_unauthorized=exception_if_unauthorized
    # ).verify()
